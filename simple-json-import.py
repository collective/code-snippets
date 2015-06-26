# Very simple JSON import of a folder on plone site
#
# Assumptions:
#   - set-site.py
#   - login-as-admin.py
#   - Archetypes

from Products.CMFCore.interfaces import ISiteRoot
from zope.component import getUtility
site = getUtility(ISiteRoot)

import json
from dateutil.parser import parse
from plone.namedfile.file import NamedBlobImage
from base64 import b64decode
from plone.app.textfield.value import RichTextValue

folder = site.restrictedTraverse('path/to/folder')

fi = open('export.json')
export = json.loads(fi.read())
fi.close()

for item in export:
    if item['id'] in folder.objectIds():
        folder.manage_delObjects([item['id']])
    fields = {}
    for field_name, val in item['fields'].items():
        if isinstance(val, basestring) and val.startswith('datetime:'):
            val = parse(val.replace('datetime:', ''))
        elif isinstance(val, dict) and 'filename' in val:
            val = NamedBlobImage(data=b64decode(val['data']), contentType=val['content_type'], filename=val['filename'])  # noqa
        elif field_name in ('creators',):
            val = tuple(val)
        elif field_name == 'text':
            val = RichTextValue(raw=val, outputMimeType='text/html')
        fields[field_name] = val
    if not fields['image']:
        del fields['image']
    folder.invokeFactory('News Item', **fields)
