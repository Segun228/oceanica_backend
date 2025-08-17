from rest_framework.views import APIView
from rest_framework.response import Response

class StatusView(APIView):
    def get(self, request):
        return Response(data={"status": "ok"})
