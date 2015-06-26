# Very simple JSON export of a folder on plone site
#
# Assumptions:
#   - set-site.py
#   - login-as-admin.py
#   - Archetypes

from Products.CMFCore.interfaces import ISiteRoot
from zope.component import getUtility
site = getUtility(ISiteRoot)

import json
from Acquisition import aq_base
from Products.Archetypes.Field import Image
from DateTime import DateTime
from base64 import b64encode
from plone.app.blob.field import BlobWrapper

folder = site.restrictedTraverse('path/to/folder')

export = []
for item in folder.values():
    if item.portal_type != 'News Item':
        continue
    data = {
        'portal_type': item.portal_type,
        'id': item.getId()
    }
    field_data = {}
    for field in item.Schema().fields():
        val = aq_base(field.get(item))
        if isinstance(val, tuple):
            val = list(val)
        elif isinstance(val, Image):
            val = {
                'filename': val.filename,
                'data': b64encode(str(val.data)),
                'content_type': val.getContentType()
            }
        elif isinstance(val, DateTime):
            val = 'datetime:' + val.ISO()
        elif isinstance(val, BlobWrapper):
            val = {
                'filename': val.filename,
                'data': b64encode(str(val.data)),
                'content_type': val.getContentType()
            }
        field_data[field.__name__] = val
    data['fields'] = field_data
    export.append(data)


fi = open('export.json', 'w')
fi.write(json.dumps(export))
fi.close()
