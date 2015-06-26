# Get redirects for object
#
# Assumptions:
#   - set-site.py

from plone.app.redirector.interfaces import IRedirectionStorage
from zope.component import getUtility

storage = getUtility(IRedirectionStorage)
print storage.redirects('/front-page')