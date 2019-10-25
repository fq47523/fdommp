from django.shortcuts import render,HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core import serializers
from logger import models
from hosts.models import Host
from utils._fmt_date import DateFmt
from utils._BT_pagination import BtPaging
from api.utils import es_api
import json
# Create your views here.

@login_required
def platform_log(request):
    if request.method == 'GET':
        change_action = request.GET.get('change_action', None)
        menu = {'menu_one':{'host':'主机','user':'用户'},
                'menu_two':{'host':{'add':'新增','modify':'修改','delete':'删除'},
                            'user':{'login':'登入'},
                            'default':{'reseting':'all'}
                        }}

        if change_action in menu['menu_two']:
            menu_two_callback = menu['menu_two'][change_action]

            return JsonResponse(menu_two_callback)

        return render(request, 'logger/platform_log.html', {'menu': menu})

    if request.method == 'POST':

        try:
            page_json = json.loads(request.body)
        except json.decoder.JSONDecodeError:
            pass


        if page_json['action']:
            ops_log_action_json = json.loads(page_json['action'])
            bttable_init = BtPaging(PageJsonDate=page_json)

            if ops_log_action_json['log_type'] != 'default' and ops_log_action_json['start_date'] and ops_log_action_json['end_date']:
                start_date = DateFmt(ops_log_action_json['start_date'])
                start_date_res = start_date.date_fmt_1()
                end_date = DateFmt(ops_log_action_json['end_date'])
                end_date_res = end_date.date_fmt_1()

                ops_log_date_filter = models.PlatformLog.objects.filter(log_type = ops_log_action_json['log_type'],
                                                                        module =  ops_log_action_json['log_module'],
                                                                        create_time__range=(start_date_res, end_date_res)).order_by('-create_time')

                table_paging_data = bttable_init.log_paging(ops_log_date_filter)

                return JsonResponse(table_paging_data)



            elif ops_log_action_json['log_type'] == 'default' and ops_log_action_json['start_date'] and ops_log_action_json['end_date']:
                start_date = DateFmt(ops_log_action_json['start_date'])
                start_date_res = start_date.date_fmt_1()
                end_date = DateFmt(ops_log_action_json['end_date'])
                end_date_res = end_date.date_fmt_1()

                ops_log_date_filter = models.PlatformLog.objects.filter(create_time__range=(start_date_res, end_date_res)).order_by('-create_time')


                table_paging_data = bttable_init.log_paging(ops_log_date_filter)

                return JsonResponse(table_paging_data)


            elif ops_log_action_json['log_type'] != 'default':
                ops_log_action_ret = models.PlatformLog.objects.filter(
                                                                    log_type = ops_log_action_json['log_type'],
                                                                    module =  ops_log_action_json['log_module']
                                                                    ).order_by('-create_time')


                table_paging_data = bttable_init.log_paging(ops_log_action_ret)
                return JsonResponse(table_paging_data)
            else:
                return JsonResponse({'sts': '200'})




@login_required
def application_log(request):
    if request.method == 'GET':
        host_obj = Host.objects.all().values('h_ip')
        host_obj_ip_list = [i['h_ip'] for i in host_obj]

        menu = {'menu_one': {'iplist': host_obj_ip_list},
                'menu_two': {'servicename': {'sn':None},
                             'default': {'reseting': 'all'}
                             }}

        change_action = request.GET.get('change_action', None)

        if change_action:
            if change_action == 'default':
                return JsonResponse(menu['menu_two']['default'])
            else:
                host_qobj = Host.objects.filter(h_ip=change_action).values('service__s_name')
                menu['menu_two']['servicename']['sn'] = [i['service__s_name'] for i in host_qobj]
                return JsonResponse(menu['menu_two']['servicename'])

        return render(request, 'logger/application_log.html', {'menu': menu})

    if request.method == 'POST':



        rows = [{'ip': '192.168.79.141', 'logdate': '2018-10-09 00:02:02.091', 'level': 'ERROR',
          'message': '2018-10-09 00:02:02.091 [ERROR]\n\n'},
         {'ip': '192.168.79.141', 'logdate': '2018-10-09 00:02:02.091', 'level': 'ERROR',
          'message': '2018-10-09 00:02:02.091 [ERROR] [HDFSCollector_model_yzdj] com.cy.plugin.collector.hdfs.HdfsCollectorPlugin$HdfsCollector - list files in current partition error. curPartition: opt_date=201810070200, alreadyReadFileName: 000001_0\norg.apache.hadoop.ipc.RemoteException: Operation category READ is not supported in state standby. Visit https://s.apache.org/sbnn-error\n\tat org.apache.hadoop.hdfs.server.namenode.ha.StandbyState.checkOperation(StandbyState.java:88)\n\tat org.apache.hadoop.hdfs.server.namenode.NameNode$NameNodeHAContext.checkOperation(NameNode.java:1835)\n\tat org.apache.hadoop.hdfs.server.namenode.FSNamesystem.checkOperation(FSNamesystem.java:1479)\n\tat org.apache.hadoop.hdfs.server.namenode.FSNamesystem.getListingInt(FSNamesystem.java:5108)\n\tat org.apache.hadoop.hdfs.server.namenode.FSNamesystem.getListing(FSNamesystem.java:5095)\n\tat org.apache.hadoop.hdfs.server.namenode.NameNodeRpcServer.getListing(NameNodeRpcServer.java:888)\n\tat org.apache.hadoop.hdfs.server.namenode.AuthorizationProviderProxyClientProtocol.getListing(AuthorizationProviderProxyClientProtocol.java:336)\n\tat org.apache.hadoop.hdfs.protocolPB.ClientNamenodeProtocolServerSideTranslatorPB.getListing(ClientNamenodeProtocolServerSideTranslatorPB.java:630)\n\tat org.apache.hadoop.hdfs.protocol.proto.ClientNamenodeProtocolProtos$ClientNamenodeProtocol$2.callBlockingMethod(ClientNamenodeProtocolProtos.java)\n\tat org.apache.hadoop.ipc.ProtobufRpcEngine$Server$ProtoBufRpcInvoker.call(ProtobufRpcEngine.java:617)\n\tat org.apache.hadoop.ipc.RPC$Server.call(RPC.java:1073)\n\tat org.apache.hadoop.ipc.Server$Handler$1.run(Server.java:2217)\n\tat org.apache.hadoop.ipc.Server$Handler$1.run(Server.java:2213)\n\tat java.security.AccessController.doPrivileged(Native Method)\n\tat javax.security.auth.Subject.doAs(Subject.java:422)\n\tat org.apache.hadoop.security.UserGroupInformation.doAs(UserGroupInformation.java:1917)\n\tat org.apache.hadoop.ipc.Server$Handler.run(Server.java:2211)\nCaused by: java.net.SocketException: Broken pipe (Write failed)\n\tat org.apache.hadoop.ipc.Client.call(Client.java:1475)\n\tat org.apache.hadoop.ipc.Client.call(Client.java:1412)\n\tat org.apache.hadoop.ipc.ProtobufRpcEngine$Invoker.invoke(ProtobufRpcEngine.java:229)\n\tat com.sun.proxy.$Proxy73.getListing(Unknown Source)\n\tat org.apache.hadoop.hdfs.protocolPB.ClientNamenodeProtocolTranslatorPB.getListing(ClientNamenodeProtocolTranslatorPB.java:573)\n\tat sun.reflect.GeneratedMethodAccessor60.invoke(Unknown Source)\n\tat sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)\n\tat java.lang.reflect.Method.invoke(Method.java:498)\n\tat org.apache.hadoop.io.retry.RetryInvocationHandler.invokeMethod(RetryInvocationHandler.java:191)\n\tat org.apache.hadoop.io.retry.RetryInvocationHandler.invoke(RetryInvocationHandler.java:102)\n\tat com.sun.proxy.$Proxy74.getListing(Unknown Source)\n\tat org.apache.hadoop.hdfs.DFSClient.listPaths(DFSClient.java:2086)\n\tat org.apache.hadoop.hdfs.DFSClient.listPaths(DFSClient.java:2069)\n\tat org.apache.hadoop.hdfs.DistributedFileSystem.listStatusInternal(DistributedFileSystem.java:791)\n\tat org.apache.hadoop.hdfs.DistributedFileSystem.access$700(DistributedFileSystem.java:106)\n\tat org.apache.hadoop.hdfs.DistributedFileSystem$18.doCall(DistributedFileSystem.java:853)\n\tat org.apache.hadoop.hdfs.DistributedFileSystem$18.doCall(DistributedFileSystem.java:849)\n\tat org.apache.hadoop.fs.FileSystemLinkResolver.resolve(FileSystemLinkResolver.java:81)\n\tat org.apache.hadoop.hdfs.DistributedFileSystem.listStatus(DistributedFileSystem.java:860)\n\tat org.apache.hadoop.fs.FileSystem.listStatus(FileSystem.java:1517)\n\tat org.apache.hadoop.fs.FileSystem.listStatus(FileSystem.java:1557)\n\tat com.cy.plugin.collector.hdfs.HdfsCollectorPlugin$HdfsCollector.readCurPartition(HdfsCollectorPlugin.java:200)\n\tat com.cy.plugin.collector.hdfs.HdfsCollectorPlugin$HdfsCollector.collect(HdfsCollectorPlugin.java:111)\n\tat com.cy.bifrost.core.runner.TimingCollectorRunner$CollectorProcess.run(TimingCollectorRunner.java:130)\n\tat java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511)\n\tat java.util.concurrent.FutureTask.runAndReset(FutureTask.java:308)\n\tat java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.access$301(ScheduledThreadPoolExecutor.java:180)\n\tat java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.run(ScheduledThreadPoolExecutor.java:294)\n\tat java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1142)\n\tat java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:617)\n\tat java.lang.Thread.run(Thread.java:745)'}
                ,{'ip': '192.168.79.141', 'logdate': '2018-10-09 00:03:02.091', 'level': 'ERROR',
          'message': '2018-10-09 00:02:02.091 [ERROR]\n\n'},{'ip': '192.168.79.141', 'logdate': '2018-10-09 00:03:02.091', 'level': 'ERROR',
          'message': '2018-10-09 00:02:02.091 [ERROR]\n\n'}]

        page_date_list = []
        try:
            page_json = json.loads(request.body)
            print(page_json)
            ops_log_action_json = json.loads(page_json['action'])

        except json.decoder.JSONDecodeError:
            pass



        if ops_log_action_json['log_type'] != 'default':

            return JsonResponse({'total': len(rows), 'rows': rows})

        return HttpResponse(200)

        # if ops_log_action_json['log_type'] != 'default' and ops_log_action_json['start_date'] and ops_log_action_json['end_date']:
        #     start_date = DateFmt(ops_log_action_json['start_date'])
        #     start_date_res = start_date.date_fmt_1()
        #     end_date = DateFmt(ops_log_action_json['end_date'])
        #     end_date_res = end_date.date_fmt_1()
        #     ops_log_date_filter = models.PlatformLog.objects.filter(log_type=ops_log_action_json['log_type'],
        #                                                             module=ops_log_action_json['log_module'],
        #                                                             create_time__range=(
        #                                                             start_date_res, end_date_res)).order_by(
        #         '-create_time')
        #
        #     page_data = ops_log_date_filter[
        #                 (page_json['page'] - 1) * page_json['rows']:page_json['rows'] * page_json['page']]
        #     print(page_data)
        #
        #     return JsonResponse(200)
        #
        #
        #
        # elif ops_log_action_json['log_type'] == 'default' and ops_log_action_json['start_date'] and ops_log_action_json['end_date']:
        #     start_date = DateFmt(ops_log_action_json['start_date'])
        #     start_date_res = start_date.date_fmt_1()
        #     end_date = DateFmt(ops_log_action_json['end_date'])
        #     end_date_res = end_date.date_fmt_1()
        #
        #     ops_log_date_filter = models.PlatformLog.objects.filter(
        #         create_time__range=(start_date_res, end_date_res)).order_by('-create_time')
        #
        #     return JsonResponse(200)
        #
        #
        # elif ops_log_action_json['log_type'] != 'default':
        #     print(ops_log_action_json['log_type'])
        #     # ops_log_action_ret = models.PlatformLog.objects.filter(
        #     #     log_type=ops_log_action_json['log_type'],
        #     #     module=ops_log_action_json['log_module']
        #     # ).order_by('-create_time')
        #     #
        #     # page_data = ops_log_action_ret[
        #     #             (page_json['page'] - 1) * page_json['rows']:page_json['rows'] * page_json['page']]
        #     #
        #     # for i in page_data:
        #     #     structure = {}
        #     #     structure['create_time'] = i.create_time
        #     #     structure['log_type'] = i.log_type
        #     #     structure['module'] = i.module
        #     #     structure['user'] = i.user
        #     #     structure['status'] = i.status
        #     #     structure['description'] = i.description
        #     #     page_date_list.append(structure)
        #     #
        #     # table_paging_data = {'total': int(ops_log_action_ret.count()), 'rows': page_date_list}
        #     return JsonResponse({'sts': '200'})
        # else:
        #     return JsonResponse({'sts': '200'})

