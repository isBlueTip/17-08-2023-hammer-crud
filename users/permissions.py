from rest_framework.permissions import BasePermission

SAFE_METHODS = ("GET", "HEAD", "OPTIONS")


class IsAuthenticatedOrCreateOrReadOnly(BasePermission):
    """
    The request is creating or authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or request.method == "POST" or request.user and request.user.is_authenticated
        )
