import os
from rest_framework import permissions
from dotenv import load_dotenv

load_dotenv()

admins = (os.getenv("ADMINS"))
if not admins:
    raise ValueError("Empty admin list given")
else:
    admins = list(map(str.strip, admins.split("_")))

debug = os.getenv("DEBUG", "False").lower() == "true"


class PhotoIsAdminOrDebugOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method.upper() != "PATCH":
            return False

        auth = request.headers.get("Authorization")
        if not auth:
            return False
        parts = auth.split(" ")
        if len(parts) != 2 or parts[0] != "Bot":
            return False
        token = parts[1]

        if token not in admins and not debug:
            return False

        allowed_fields = {"photos"}
        incoming_fields = set(request.data.keys())
        return incoming_fields.issubset(allowed_fields)