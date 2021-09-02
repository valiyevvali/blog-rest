from rest_framework.permissions import BasePermission

class Isowner(BasePermission):

    message='You cannot delete or edit this message...'
    def has_object_permission(self, request, view, obj):
        return obj.author==request.user