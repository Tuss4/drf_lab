from rest_framework import permissions

admin_methods = ['POST', 'PUT', 'PATCH', 'DELETE']

class AdminOnlyPost(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in admin_methods:
            return request.user.is_authenticated() and request.user.is_staff
        elif request.method == 'GET':
            return True
