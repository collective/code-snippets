# Find text on site. This will search all fields and  content of portlets
#
# Assumptions:
#   - "site" object
#   - set-site.py
#   - login-as-admin.py

from Products.CMFCore.interfaces import ISiteRoot
from zope.component import getUtility
site = getUtility(ISiteRoot)

from zope.component import getUtility, getMultiAdapter
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignmentMapping
from zope.component.interfaces import ComponentLookupError


portlet_managers = (
    "plone.leftcolumn", "plone.rightcolumn",
    'ContentWellPortlets.InHeaderPortletManager1',
    'ContentWellPortlets.InHeaderPortletManager2',
    'ContentWellPortlets.InHeaderPortletManager3',
    'ContentWellPortlets.InHeaderPortletManager4',
    'ContentWellPortlets.InHeaderPortletManager5',
    'ContentWellPortlets.InHeaderPortletManager6',
    'ContentWellPortlets.AbovePortletManager1',
    'ContentWellPortlets.AbovePortletManager2',
    'ContentWellPortlets.AbovePortletManager3',
    'ContentWellPortlets.AbovePortletManager4',
    'ContentWellPortlets.AbovePortletManager5',
    'ContentWellPortlets.AbovePortletManager6',
    'ContentWellPortlets.BelowPortletManager1',
    'ContentWellPortlets.BelowPortletManager2',
    'ContentWellPortlets.BelowPortletManager3',
    'ContentWellPortlets.BelowPortletManager4',
    'ContentWellPortlets.BelowPortletManager5',
    'ContentWellPortlets.BelowPortletManager6',
    'ContentWellPortlets.FooterPortletManager1',
    'ContentWellPortlets.FooterPortletManager2',
    'ContentWellPortlets.FooterPortletManager3',
    'ContentWellPortlets.FooterPortletManager4',
    'ContentWellPortlets.FooterPortletManager5',
    'ContentWellPortlets.FooterPortletManager6',
    'ContentWellPortlets.BelowTitlePortletManager1',
    'ContentWellPortlets.BelowTitlePortletManager2',
    'ContentWellPortlets.BelowTitlePortletManager3',
    'ContentWellPortlets.BelowTitlePortletManager4',
    'ContentWellPortlets.BelowTitlePortletManager5',
    'ContentWellPortlets.BelowTitlePortletManager6',
)


all_content = site.portal_catalog(show_inactive=True)  # noqa

# The name “Reading Room” should be changed to “FOIA Library” in all instances
what_to_find = 'PUT YOUR TEXT HERE'.lower()


def checkText(text):
    if not isinstance(text, basestring):
        return False
    return what_to_find in text.lower()

has_warned_about = []
skip = 0
count = skip
for brain in all_content[skip:]:
    content = brain.getObject()
    path = '/'.join(content.getPhysicalPath())
    for manager_name in portlet_managers:
        try:
            manager = getUtility(IPortletManager, name=manager_name, context=content)
        except ComponentLookupError:
            if manager_name not in has_warned_about:
                print('invalid portlet manager: %s' % manager_name)
                has_warned_about.append(manager_name)
            continue
        try:
            mapping = getMultiAdapter((content, manager), IPortletAssignmentMapping)
        except ComponentLookupError:
            continue
        # id is portlet assignment id
        # and automatically generated
        for id, assignment in mapping.items():
            # check attributes
            for attr in ('text', 'portlet_title', 'custom_header', 'more_text', 'header'):
                if checkText(getattr(assignment, attr, '')):
                    print('found on context: %s and portlet assignment: %s' % (path, id))
                    continue
    # now check content
    for field_name in ('title', 'text', 'description'):
        try:
            schema = content.Schema()
        except AttributeError:
            print('skipping: %s' % path)
            continue
        field = schema.getField(field_name)
        if field is None:
            continue
        val = field.get(content)
        if checkText(val):
            print('found on context: %s' % path)
            continue
    count += 1
    if count % 1000 == 0:
        print('checked %i' % count)