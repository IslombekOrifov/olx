from rest_framework.permissions import BasePermission

class IsDeleted(BasePermission):
    def has_perm(self, request, view):
        return request.user.is_deleted