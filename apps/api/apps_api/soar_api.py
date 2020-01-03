from databases.models import Soar_Config
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import json,pymysql


from databases.soar.common import runcmd
from databases.soar.common import req_parse2cmd_parse
from databases.soar.common import parse_dsn
from databases.soar.argcrypto import decrypt


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

class SoarDetail(APIView):
    def put(self,request):
        req = request.data

        Soar_Config.objects.filter(id=req.get('id')).update(
            name=req.get('name'),
            onlinedsn=req.get('online-dsn'),
            testdsn=req.get('test-dsn'),
            allowonlineastest= req.get('allow-online-as-test') if isinstance(req.get('allow-online-as-test'),bool) else req.get('allow-online-as-test').capitalize(),
            blacklist=req.get('blacklist'),
            sampling=req.get('sampling') if isinstance(req.get('sampling'),bool) else req.get('sampling').capitalize(),
            tableallowengines=req.get('tableallowengines'),
        )
        return Response({'status':status.HTTP_200_OK,'msg':'修改成功'})

    def delete(self,request):
        req = request.data
        print (req)
        Soar_Config.objects.filter(id=req.get('id')).delete()
        return Response({'status': status.HTTP_200_OK, 'msg': '删除成功'})

@api_view(['GET'])
def soarcmd(request):
    result = runcmd(req_parse2cmd_parse({'version' : 'true'}))
    return Response({'result': result, 'status': True})

@api_view(['POST'])
def testconnect(request):
    arg = request.data
    if  'data' not in arg or 'key' not in arg:
        return json.dumps({
            "result": 'data or key is None',
            "status": False
        })

    try:
        dsn = json.loads(decrypt(arg['data'],arg['key']))['dsn']
    except Exception as e:
        return json.dumps({
            "result": str(e),
            "status": False
        })
    try:
        res = parse_dsn(dsn)
        pymysql.connect(
            host = res['host'],
            port = int(res['port']),
            user = res['user'],
            passwd = res['pwd'],
            db = res['db'],
        )
        status = True
        result = '连接成功'
    except Exception as e:
        status = False
        result = str(e)
    return Response({'result':result, 'status':status})


@api_view(['POST'])
def importConfig(request):
    req = request.data
    DataList = []
    print (req,type(req))
    try:
        if 'cover' in req:
            del req[0]
            Soar_Config.objects.all().delete()
            for i in req:
                DataList.append(Soar_Config(
                    name=i.get('name'),
                    onlinedsn=i.get('online-dsn'),
                    testdsn=i.get('test-dsn'),
                    allowonlineastest=i.get('allow-online-as-test'),
                    sampling=i.get('sampling'),
                    blacklist=i.get('blacklist')
                ))
            Soar_Config.objects.bulk_create(DataList)
        else:
            for i in req:
                DataList.append(Soar_Config(
                    name=i.get('name'),
                    onlinedsn=i.get('online-dsn'),
                    testdsn=i.get('test-dsn'),
                    allowonlineastest=i.get('allow-online-as-test'),
                    sampling=i.get('sampling'),
                    blacklist=i.get('blacklist')
                ))
            Soar_Config.objects.bulk_create(DataList)
    except Exception as e:
        return Response({'status': status.HTTP_401_UNAUTHORIZED, 'msg': str(e)})

    return Response({'status':status.HTTP_200_OK,'msg':'导入成功'})


