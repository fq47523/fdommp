from databases.models import Soar_Config
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
from rest_framework.decorators import api_view


class SoarList(APIView):
    def get(self,request):
        datalist = []
        for i in Soar_Config.objects.all():
            datalist.append(i.to_json())

        return Response(datalist)

    def post(self,request):
        req = request.data
        Soar_Config.objects.create(
            name=req.get('name'),
            onlinedsn=req.get('online-dsn'),
            testdsn=req.get('test-dsn'),
            allowonlineastest=req.get('allow-online-as-test').capitalize(),
            blacklist=req.get('blacklist'),
            sampling=req.get('sampling').capitalize(),
            tableallowengines=req.get('tableallowengines', ),
        )

        return Response({'status':status.HTTP_201_CREATED,'msg':'创建成功'})