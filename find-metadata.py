# Find files with metadata
#
# Assumptions:
#   - set-site.py
#   - "exiftool" system binary installed
#   - Archetypes
#   - login-as-admin.py

from Products.CMFCore.interfaces import ISiteRoot
from zope.component import getUtility
site = getUtility(ISiteRoot)

from tempfile import mkdtemp
from shutil import rmtree
import subprocess
import os
from ZODB.POSException import POSKeyError
import csv

writer = csv.writer(open('found.csv', 'w'), dialect='excel')

_ignored_values = [
    'created by accusoft corp.',
    'unknown',
    'apache fop version 1.1rc1',
    'apache fop version 1.0',
    'adobe pdf library 9.90',
    'file written by adobe photoshop<a8> 5.0',
    'file written by adobe photoshop<a8> 4.0'
]


class ExifToolSubProcess(object):
    default_paths = ['/bin', '/usr/bin', '/usr/local/bin']
    bin_name = 'exiftool'
    def __init__(self):
        binary = self._findbinary()
        self.binary = binary
        if binary is None:
            raise IOError("Unable to find %s binary" % self.bin_name)
    def _findbinary(self):
        if 'PATH' in os.environ:
            path = os.environ['PATH']
            path = path.split(os.pathsep)
        else:
            path = self.default_paths
        for dir in path:
            fullname = os.path.join(dir, self.bin_name)
            if os.path.exists(fullname):
                return fullname
        return None
    def _run_command(self, cmd):
        if isinstance(cmd, basestring):
            cmd = cmd.split()
        cmdformatted = ' '.join(cmd)
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, close_fds=True)
        output, error = process.communicate()
        process.stdout.close()
        process.stderr.close()
        if process.returncode != 0:
            error = """Command
%s
finished with return code
%i
and output:
%s
%s""" % (cmdformatted, process.returncode, output, error)
            raise Exception(error)
        return output
    def get_meta(self, filepath):
        cmd = [self.binary, filepath]
        txt = self._run_command(cmd)
        result = {}
        for line in txt.splitlines():
            name, value = line.split(':', 1)
            name = name.strip().lower()
            value = value.strip().lower()
            if not name or not value or value in _ignored_values:
                continue
            result[name] = value
        return result

exiftool = ExifToolSubProcess()

catalog = site.portal_catalog  # noqa

keys_to_watch = [
    'Last Modified By',
    'Author',
    'Creator',
    'History',
    'Author Email',
    'Author Email Display Name',
    'Last Saved By',
    'Artist',
    'By-line',
    'By-line Title',
    'Caption Writer',
    'Comment',
    'Creator Address',
    'Creator City',
    'Creator Work Email',
    'Creator Work Telephone',
    'Creator Work URL',
    'Owner Name',
    'Producer'
]

_sitepath = '/'.join(site.getPhysicalPath())  # noqa
def getPath(obj):
    path = '/'.join(obj.getPhysicalPath())
    return path[len(_sitepath):]


count = 0
for brain in catalog():
    obj = brain.getObject()
    print 'checking ', '/'.join(obj.getPhysicalPath()), ' ', str(count)
    count += 1
    for field in obj.Schema().fields():
        if field.type in ('image', 'file'):
            try:
                value = field.get(obj)
                if isinstance(value, basestring):
                    if len(value) == 0:
                        continue
                    else:
                        data = value
                elif value is None:
                    continue
                else:
                    data = str(value.data)
                filename = field.getFilename(obj)
                if not filename:
                    filename = 'placeholder'
                _, ext = os.path.splitext(filename)
                # write out file to tmp
                _dir = mkdtemp()
                filepath = os.path.join(_dir, filename)
                fi = open(filepath, 'w')
                fi.write(data)
                fi.close()
            except POSKeyError:
                continue
            meta = exiftool.get_meta(filepath)
            found_keys = []
            for key in keys_to_watch:
                if key.lower() in meta:
                    found_keys.append(key.lower())
            if len(found_keys):
                writer.writerow([
                    getPath(obj),
                    field.__name__,
                    ', '.join(
                        ['%s:%s' % (k, meta[k]) for k in found_keys])
                ])
            rmtree(_dir)
    obj._p_deactivate()
