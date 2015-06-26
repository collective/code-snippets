# Rename a file
#
# Assumptions:
#   - set-site.py
#   - Access to object

from Products.CMFCore.interfaces import ISiteRoot
from zope.component import getUtility
site = getUtility(ISiteRoot)

obj = site.restrictedTraverse('path/to/file')
obj.setFilename('my-new-filename.jpg')

import transaction
transaction.commit()
