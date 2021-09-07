from rest_framework.permissions import BasePermission

class NotAuthenticated(BasePermission):

    message='You have already account...'
    def has_permission(self, request, view):
        return not request.user.is_authenticated