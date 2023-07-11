from rest_framework.permissions import SAFE_METHODS, IsAuthenticated, BasePermission
import logging

logger = logging.getLogger(__name__)


class IsAccountOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_superuser


class IsObjectOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.owner == request.user or request.user.is_superuser


class IsCreator(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return request.user.role == 'creator' or request.user.is_superuser


class IsBusiness(IsAuthenticated):
    def has_permissions(self, request, view):
        return request.user.role == 'BUSINESS' or request.user.is_superuser


class IsCampaignOwner(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        logger.info(f"Checking if {request.user} is owner of {obj}")
        return obj.owner == request.user and request.user.role == 'BUSINESS'
