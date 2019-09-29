from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from api import  serializers
from assets.models import *

class AssetsList(APIView):
    def get(self, request, format=None):
        snippets = Asset.objects.all()
        serializer = serializers.AssetsSerializer(snippets, many=True)
        return Response(serializer.data)