# Find objects that are linked to an objects
#
# Assumptions:
#   - set-site.py
#   - login-as-admin.py

from Products.CMFCore.interfaces import ISiteRoot
from zope.component import getUtility
site = getUtility(ISiteRoot)

refcat = site.reference_catalog
item = site.restrictedTraverse('some/page')
refs = item.getBackReferences(relationship="isReferencing")
