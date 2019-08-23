from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrAdmin(BasePermission):
    """
    Restricts editing to owners and admins
    """

    def has_object_permission(self, request, view, obj):
        if (
            request.method in SAFE_METHODS
            or request.user.is_superuser
            or request.user.is_staff
        ):
            return True
        return obj.owner == request.user
