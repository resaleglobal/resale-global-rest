from rest_framework import permissions
from pprint import pprint

class ResellerAdminPermission(permissions.BasePermission):
    """
    Global permission check admin APIss
    """

    def has_permission(self, request, view):

        # account_id = request.META['accountId']
        pprint(request)
        return True