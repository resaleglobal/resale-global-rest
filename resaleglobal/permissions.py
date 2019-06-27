from rest_framework import permissions

from resaleglobal.account.models import UserResellerAssignment, Reseller

class ResellerAdminPermission(permissions.BasePermission):
    """
    Global permission check admin APIss
    """

    message = "User does not have admin access."

    def has_permission(self, request, view):

        account_id = view.kwargs['accountId']

        if account_id is None:
          return False

        reseller = Reseller.objects.filter(pk=account_id).first()

        if reseller is None:
          return False

        assignment = UserResellerAssignment.objects.filter(reseller=reseller, user=request.user).first()

        if assignment is None:
          return False
        
        return assignment.is_admin

class ResellerPermission(permissions.BasePermission):
    """
    Global permission check reseller APIss
    """

    message = "User does not have admin access."

    def has_permission(self, request, view):

        account_id = view.kwargs['accountId']

        if account_id is None:
          return False

        reseller = Reseller.objects.filter(pk=account_id).first()

        if reseller is None:
          return False

        assignment = UserResellerAssignment.objects.filter(reseller=reseller, user=request.user).first()

        if assignment is None:
          return False
        
        return True

