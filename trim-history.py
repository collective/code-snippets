# remove history of object
#
# Assumption:
#   - set-site.py
#   - login-as-admin.py

from Products.CMFCore.interfaces import ISiteRoot
from zope.component import getUtility
site = getUtility(ISiteRoot)

uidcatalog = site.uid_catalog
hstore = site.portal_historiesstorage
shadowStore = hstore._getShadowStorage(autoAdd=False)

historyIds = shadowStore._storage
repo = hstore.zvc_repo

for historyId in list(historyIds.keys()):
    history = hstore._getShadowHistory(historyId)
    zv_hist_id = history._full[0]['vc_info'].history_id
    found = False
    if zv_hist_id in repo._histories:
        zv_history = repo._histories[zv_hist_id]
        version = zv_history._versions[zv_history._versions.keys()[0]]
        try:
            obj = version._data._object.object
            uid = obj.UID()
            brains = uidcatalog.searchResults(UID=uid)
            if len(brains) > 0:
                found = True
        except:
            pass
    if not found:
        print 'deleting', str(historyId), zv_hist_id
        del historyIds[historyId]
        try:
            del repo._histories[zv_hist_id]
        except KeyError:
            pass
