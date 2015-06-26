#
# Get info on the objects in the system.
#
# - Total Objects
# - Number of objects created
#   - by week for past 4 weeks
#   - by month for past 6 months
#   - last year
# - Average objs created
#   - Each month for the previous 12 months, daily average
# - by type
#
#
# Assumptions:
#   - set-site.py
#   - login-as-admin.py

from Products.CMFCore.interfaces import ISiteRoot
from zope.component import getUtility
site = getUtility(ISiteRoot)

from DateTime import DateTime
import locale

bsep = "==================================="
sep = "-----------------------------------"

now = DateTime()
catalog = site.portal_catalog
pts = site.portal_types.objectIds()

by_type = {}
objs_created = {}
average_objs_created = {}


def print_results(results, start, end):
    count = len(results)
    print 'Created between %s and %s: %s, Averaging: %.2f/day' % (
        start.Date(),
        end.Date(),
        locale.format("%d", count, grouping=True),
        float(count) / float(end - start)
    )


def handle_period(number, step, query=None, before=None):
    for num in reversed(range(1, number + 1)):
        start = now - (num * step)
        end = now - ((num - 1) * step)
        if query is None:
            query = {}
        query['created'] = {'query': (start, end), 'range': 'min:max'}
        results = catalog(**query)
        if results:
            if before is not None:
                print before
            print_results(results, start, end)

print 'Total Objects: %s' % len(catalog())

print "\nStats on objects created in periods"
print bsep
print sep
print "Last 4 weeks"
print sep
# get number of objects created in last 4 weeks
handle_period(4, 7)

print sep
print "Last 6 months"
print sep
handle_period(12, 30)

print sep
print "Last 3 Years"
print sep
handle_period(3, 365)


print bsep
print 'By content type'
print bsep
for pt in pts:
    print '-- %s' % pt
    handle_period(12, 30, {'portal_type': pt})
