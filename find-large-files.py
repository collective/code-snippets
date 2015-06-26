# Find large files on the site
#
# Assumptions
#   - You are using Archetypes
#   - login-as-admin.py
#   - set-site.py

from Products.CMFCore.interfaces import ISiteRoot
from zope.component import getUtility
site = getUtility(ISiteRoot)

SIZE = 5
catalog = site.portal_catalog  # noqa
total = 0

thresholds = {
    'image': 5,
    'psd': 5,
    'video': 40,
    'audio': 30,
    'pdf': 3
}

txt = ''
for brain in catalog(portal_type=("Image", "File"),
                     review_state="published"):
    obj = brain.getObject()
    if brain.portal_type == 'File':
        fi = obj.getFile()
    else:
        fi = obj.getImage()
    size = fi.get_size() / 1024 / 1024
    full_ct = fi.getContentType()
    ctsplit = full_ct.split('/')
    ct = ctsplit[0]
    ct2 = None
    if len(ctsplit) > 1:
        ct2 = ctsplit[1]
    path = '/'.join(obj.getPhysicalPath())
    found_ct = 'unknown: ' + full_ct
    if ct in thresholds:
        found_ct = ct
        compare = thresholds[ct]
    elif ct2 in thresholds:
        found_ct = ct2
        compare = thresholds[ct2]
    else:
        compare = SIZE
    if size > compare:
        total += size
        print 'ct: ', found_ct, ' path: ', path, ' size: ', str(size)
