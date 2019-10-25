from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from api.utils.ansible_api import ANSRunner



class ServiceAction(APIView):

    def get(self, request, format=None):
        pass


    def post(self,request, format=None):
        print (request.data)
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


        if hasattr(self, data['target']):
            func = getattr(self, data['target'])
            return func(data)
        else:
            return Response({'target':'error'},status.HTTP_400_BAD_REQUEST)


    def started(self,data):
        res = self.ansibleadhoc(data['ip'],data['target'],data['servicename'])
        print (res,type(res))
        return Response(res,status.HTTP_200_OK)

    def stopped(self,data):
        res = self.ansibleadhoc(data['ip'],data['target'],data['servicename'])
        print (res,type(res))
        return Response(res,status.HTTP_200_OK)


    def restarted(self,data):
        res = self.ansibleadhoc(data['ip'],data['target'],data['servicename'])
        print (res,type(res))
        return Response(res,status.HTTP_200_OK)


    def ansibleadhoc(self,ip,target,servicename):
        rbt = ANSRunner([], redisKey='1')
        # Ansible Adhoc
        rbt.run_model(host_list=[ip], module_name='script',
                      module_args='/opt/DOM/server.sh {} {}'.format(target,servicename))

        data = rbt.get_model_result()


        return data