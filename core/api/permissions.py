from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """
    Docstring for IsOwner
    Object - level permission.
    """

    def has_object_permission(self, request, view, obj):
        return getattr(obj, "created_by", None) == request.user