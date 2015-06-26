# get annotations for an object
#
# Assumptions:
#   - set-site.py

from Products.CMFCore.interfaces import ISiteRoot
from zope.component import getUtility
site = getUtility(ISiteRoot)

from zope.annotation.interface import IAnnotations

obj = site.restrictedTraverse('my/object')
ann = IAnnotations(obj)
