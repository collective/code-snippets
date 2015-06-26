# Set the zope component site
#
# Assumptions:
#   You have an "app" object.

site = app['mysiteid']  # noqa
from zope.component.hooks import setSite
setSite(site)
