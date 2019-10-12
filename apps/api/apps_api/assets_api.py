from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from api import  serializers
from assets.models import *

class AssetsAction(APIView):
    def get(self, request, format=None):
        snippets = Server.objects.all()
        serializer = serializers.AssetsServerSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self,request, format=None):

        if(request.data.get('data')):
            data = request.data.get('data')
        else:
            data = request.data
        print (data)
        serializer = serializers.AssetsServerSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({'code':201}, status=status.HTTP_201_CREATED)
        return Response(404)

    def put(self, request, id,format=None):
        data = request.data

        try:
            snippet = Server.objects.get(id=id)
        except Server.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)



        if (data.get('asset')):
            assets_data = data.pop('asset')
            try:
                assets_snippet = Asset.objects.get(id=snippet.asset.id)
                assets = serializers.AssetsSerializer(assets_snippet, data=assets_data)
            except Asset.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            if assets.is_valid():
                assets.save()

        serializer = serializers.AssetsServerSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request, id,format=None):


        try:
            snippet = Asset.objects.get(id=id)
        except Asset.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        Asset.objects.filter(id=snippet.id).delete()

        return Response({'code':202},status.HTTP_202_ACCEPTED)