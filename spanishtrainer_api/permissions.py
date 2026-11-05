from rest_framework.permissions import BasePermission

class IsContentUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='ContentUser').exists()

class IsContentAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='ContentAdmin').exists()