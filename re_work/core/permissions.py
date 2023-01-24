from rest_framework import permissions


class IsAdminStaff(permissions.BasePermission):
    basic_methods = ("POST", "PUT", "PATCH", "DELETE")

    def has_permission(self, request, view):
        if request.user.is_authenticated and (
                request.user.is_staff or request.user.is_admin or request.user.is_staff_admin):
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if request.method in self.basic_methods or request.method in permissions.SAFE_METHODS:
            return True

        return False


class IsClientProduct(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if obj.client == request.user:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        return False


class hasDeveloperAccess(permissions.BasePermission):
    basic_methods = ("PUT", "PATCH", "DELETE")

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if (
                request.user.is_video_editor or request.user.is_full_stack) and obj.video_editor == request.user and request.method not in self.basic_methods:
            return True

        if (
                request.user.is_script_writer or request.user.is_full_stack) and obj.script_writer == request.user and request.method not in self.basic_methods:
            return True

        return False
