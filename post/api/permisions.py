from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    message='You must be owner of this object'
    def has_object_permission(self, request, view, obj):
        return obj.author==request.user or request.user.is_superuser