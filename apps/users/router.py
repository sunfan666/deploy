from rest_framework.routers import DefaultRouter
from .views import UsersViewset, UserInfoViewset, GroupsViewset, UserGroupsViewset, GroupMembersViewset
from .views import PermissionsViewset, GroupsPermViewset

users_router = DefaultRouter()
users_router.register(r'user', UsersViewset, base_name="user")
users_router.register(r'userinfo', UserInfoViewset, base_name="userinfo")
users_router.register(r'group', GroupsViewset, base_name="group")
users_router.register(r'usergroup', UserGroupsViewset, base_name="usergroup")
users_router.register(r'groupmembers', GroupMembersViewset, base_name="groupmembers")

users_router.register(r'permission', PermissionsViewset, base_name="permission")
users_router.register(r'grouppower', GroupsPermViewset, base_name="grouppower")