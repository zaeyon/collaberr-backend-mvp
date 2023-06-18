from rest_framework import permissions


class IsAccountOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_superuser


class IsObjectOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user or request.user.is_superuser


class IsCreator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.role == 'creator' or request.user.is_superuser


class IsBusiness(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.role == 'business' or request.user.is_superuser
