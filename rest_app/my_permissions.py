from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # return bool(
        #     request.method in SAFE_METHODS or
        #     request.user and
        #     request.user.is_authenticated
        # )
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user