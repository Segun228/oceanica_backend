from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.views import APIView
from api.models import Post, Category
from api.serializers import PostSerializer, CategorySerializer, CategoryReadSerializer
from backend.authentication import TelegramAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from . import handlers

class AddPostsFile(APIView):
    authentication_classes = [TelegramAuthentication]
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        pass


class ReplacePostsFile(APIView):
    authentication_classes = [TelegramAuthentication]
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        pass


class GetPostsFile(APIView):
    authentication_classes = [TelegramAuthentication]
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all().values()
        categories = Category.objects.all().values()
        return handlers.get_xlsx_report(
            posts = posts,
            categories = categories
        )

