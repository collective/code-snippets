# ZIP up files in a folder on site
#
# Assumption:
#   - login-as-admin.py
#   - set-site.py

from Products.CMFCore.interfaces import ISiteRoot
from zope.component import getUtility
site = getUtility(ISiteRoot)

import zipfile

path = 'some/path/to/folder'
folder = site.restrictedTraverse(path)

zip = zipfile.ZipFile("archive.zip", "w")

for image in folder.values():
    if hasattr(folder, 'getImage'):
        zip.writestr(image.getFilename(), str(image.getImage().data))

zip.close()
