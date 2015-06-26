# Purge object history. This script should trigger
# old history storage purging
#
# Assumptions:
#   - set-site.py
#   - login-as-admin.py
#   - set history lower or to 0 in ZMI

from Products.CMFCore.interfaces import ISiteRoot
from zope.component import getUtility
site = getUtility(ISiteRoot)

from Products.CMFEditions.utilities import dereference
from Products.CMFCore.utils import getToolByName
policy = getToolByName(site, 'portal_purgepolicy')
catalog = getToolByName(site, 'portal_catalog')

for count, brain in enumerate(catalog()):
    obj = brain.getObject()
    obj, history_id = dereference(obj)
    policy.beforeSaveHook(history_id, obj)
    print str(count) + ' purged object ' + obj.absolute_url_path()

import transaction
transaction.commit()