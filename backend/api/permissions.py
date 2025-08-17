import os

from rest_framework import permissions
from dotenv import load_dotenv
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
import logging

load_dotenv()


admin_one = os.getenv("ADMIN_1")
admin_two = os.getenv("ADMIN_2")
debug = os.getenv("DEBUG", "False").lower() == "true"

admins = [admin_one, admin_two]

class IsAdminOrDebugOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        User = get_user_model()
        if request.method in permissions.SAFE_METHODS:
            return True
        auth = request.headers.get("Authorization")
        if not auth:
            return False
        header = auth.split(" ")
        if header[0] != "Bot":
            return False
        try:
            user = User.objects.get(telegram_id=header[1])
            if (user.is_staff and header[1] in admins) or debug:
                return True
        except User.DoesNotExist:
            logging.error("Пользователь с таким Telegram ID не найден.")
            return False

