# Login as zope admin user
#
# Assumptions:
#   - "app" object

from AccessControl.SecurityManagement import newSecurityManager
user = app.acl_users.getUser('admin')  # noqa
newSecurityManager(None, user.__of__(app.acl_users))  # noqa