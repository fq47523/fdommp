from databases.models import Soar_Config
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view


class SoarList(APIView):
    def get(self,request):
        datalist = []
        for i in Soar_Config.objects.all():
            datalist.append(i.to_json())

        return Response(datalist)