# Remove a site utility
#
# Assumptions:
#   - set-site.py

from Products.CMFCore.interfaces import ISiteRoot
from zope.component import getUtility
site = getUtility(ISiteRoot)

sm = site.getSiteManager()
from vice.outbound.interfaces import IFeedSettings  # or whatever the utility is
from vice.outbound.feedsettings import FeedSettings
if sm.queryUtility(IFeedSettings):
    sm.unregisterUtility(sm.queryUtility(IFeedSettings), factory=FeedSettings)

import transaction
transaction.commit()