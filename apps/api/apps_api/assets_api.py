from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from assets.dao import AssetManage
from api import  serializers
from assets.models import *

class AssetsMeun(APIView,AssetManage):
    def get(self,request):
        meun = self.api_meun()
        print (type(meun))
        return Response(meun,status=status.HTTP_200_OK)




class AssetsServerList(APIView):
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



class AssetsServerDetail(APIView):


    def get(self,request,id):
        try:
            snippet = Server.objects.get(id=id)
        except Server.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


        serializer = serializers.AssetsServerSerializer(snippet)
        return Response(serializer.data)


    def put(self, request, id,format=None):
        if (request.data.get('data')):
            data = request.data.get('data')
        else:
            data = request.data
        print( data )
        try:
            snippet = Server.objects.get(id=id)
        except Server.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if (data.get('asset')):
            asset_data = data.pop('asset')

            try:

                asset_snippet = Asset.objects.get(id=snippet.asset.id)

                assets = serializers.AssetsSerializer(asset_snippet, data=asset_data)
            except Asset.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            if assets.is_valid():
                assets.save()

        serializer = serializers.AssetsServerSerializer(snippet, data=data)
        if serializer.is_valid():

            serializer.save()
            print (serializer.data)
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self,request, id,format=None):


        try:
            snippet = Asset.objects.get(id=id)
        except Asset.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        Asset.objects.filter(id=snippet.id).delete()

        return Response({'code':202},status.HTTP_202_ACCEPTED)