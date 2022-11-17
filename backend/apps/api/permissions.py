from rest_framework.permissions import BasePermission


class MailingUpdating(BasePermission):
    """Permission: запрещает изменение всех Mailing, где STATUS != CREATED"""

    def has_object_permission(self, request, view, obj):
        return obj.status == 'C'

    def has_permission(self, request, view):
        return request.user.is_staff