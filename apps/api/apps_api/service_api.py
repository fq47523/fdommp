from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
import json
from hosts.models import Service,Service_Status


class ServiceAction(APIView):

    def get(self, request, format=None):
        pass


    def post(self,request, format=None):
        print ('1',request.POST)
        print('2', request.data)
        print('3', request.body)

        if(request.data.get('action')):
            data = request.data.get('action')

            required = ['servicename','ip','target']
            for i in required:

                try:
                    if len(data[i]) == 0:

                        return Response({"key":i},status.HTTP_400_BAD_REQUEST)
                except KeyError as  e:

                    return Response({'key':str(e)},status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status.HTTP_404_NOT_FOUND)



        return Response(status.HTTP_200_OK)