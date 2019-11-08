import json,os
import subprocess
from assets import models
from django.shortcuts import get_object_or_404
from django.core import serializers


class AssetManage(object):


    def query_parm(self,request):
        query_str = request.META.get('QUERY_STRING')
        query_dict = {} #{action:gailan,name:6}
        for i in query_str.split('&'): query_dict[i.split("=")[0]] = i.split("=")[1]
        return query_dict


    def select_all_asset(self):
        return models.Asset.objects.all()

    def select_obj_asset(self,asset_id):
        return get_object_or_404(models.Asset,id=asset_id)

    def meun(self):
        asset = models.Asset()
        server = models.Server()
        bu = models.BusinessUnit.objects.all()
        mf = models.Manufacturer.objects.all()
        idc = models.IDC.objects.all()
        tags = models.Tag.objects.all()
        return {'asset_type':asset.asset_type_choice,
                'asset_status':asset.asset_status,
                'bu':bu,
                'mf': mf,
                'idc':idc,
                'tag':tags,
                'server_type':server.sub_asset_type_choice,
                }

    def api_meun(self):
        asset = models.Asset()
        server = models.Server()

        mfs =  [{'pk':i.id,'name':i.name} for i in models.Manufacturer.objects.all() ]
        idcs =  [{'pk':i.id,'name':i.name} for i in models.IDC.objects.all()]
        tags = [{'pk':i.id,'name':i.name} for i in models.Tag.objects.all()]
        return {
                'asset_type': asset.asset_type_choice,
                'asset_status': asset.asset_status,

                'mf': mfs,
                'idc': idcs,
                'tag': tags,
                'server_type': server.sub_asset_type_choice,
                }




    # def update_server_gailan_a(self,request, *args, **kwagrs):
    #     # print(request.POST,args[0])
    #     asset_type_data = request.POST.get('asset_type',None)
    #     business_unit_id = request.POST.get('business_unit',None)
    #     manufacturer_id = request.POST.get('manufacturer',None)
    #     manage_ip = request.POST.get('manage_ip',None)
    #     idc_id = request.POST.get('idc',None)
    #
    #     asset_obj = models.Asset.objects.filter(id=args[0]).first()
    #     asset_obj.asset_type = asset_type_data
    #     asset_obj.business_unit = models.BusinessUnit.objects.get(id=business_unit_id) if business_unit_id else None
    #     asset_obj.manufacturer = models.Manufacturer.objects.get(id=manufacturer_id) if manufacturer_id else None
    #     asset_obj.manage_ip = manage_ip
    #     asset_obj.idc = models.IDC.objects.get(id=idc_id) if idc_id else None
    #     asset_obj.save()
    #
    #
    #     # print (c.values())
    #     return True
    #
    #
    # def update_server_gailan_b(self,request, *args, **kwagrs):
    #     # print ('r:',request.POST,'args:',args[0])
    #     username = request.POST.get('username')
    #     passwd = request.POST.get('passwd',None)
    #     sshport = request.POST.get('sshport',None)
    #     sudo_passwd = request.POST.get('sudo_passwd',None)
    #     keyfile = request.POST.get('keyfile',None)
    #     # print (username,passwd,sudo_passwd)
    #     asset_obj = models.Asset.objects.filter(id=args[0]).first()
    #     server_obj = models.Server.objects.filter(asset=asset_obj).first()
    #     server_obj.username = username
    #     server_obj.passwd = passwd
    #     server_obj.sshport = sshport
    #     server_obj.sudo_passwd = sudo_passwd
    #     server_obj.keyfile = keyfile if keyfile else  None
    #     server_obj.save()
    #     # print (server_obj.sshport)



        return  True



class AnsibleAssetsSetup(object):
    def ansible_assets_collect(self,request):

        p = os.path.dirname(os.path.realpath(__file__)) + '/assetsdetail/'
        cmd = 'ansible -i /home/fuqing/hosts -m setup --tree {} all'.format(p)
        r = subprocess.getstatusoutput(cmd)
        # print (p)
        # print (os.listdir(p))
        asset = []

        for i in os.listdir(p):
            asset_dict = dict()
            print (p,i)
            with open(p+i,'r') as f:
                c = f.read()
                b = json.loads(c)
                f.close()
                try:
                # ubuntu
                    if b["ansible_facts"].get('ansible_lsb'):

                        asset_dict['asset_type'] = 'server'
                        asset_dict['manufacturer'] = b["ansible_facts"]['ansible_system_vendor']
                        asset_dict['sn'] = b["ansible_facts"]['ansible_hostname']
                        asset_dict['model'] = b["ansible_facts"]['ansible_product_name']
                        asset_dict['uuid'] = b["ansible_facts"]['ansible_product_uuid']
                        asset_dict['os_distribution'] = b["ansible_facts"]['ansible_lsb']['id']
                        asset_dict['os_release'] = b["ansible_facts"]['ansible_lsb']['description']
                        asset_dict['os_type'] = b["ansible_facts"]['ansible_system']

                        asset_dict['cpu_count'] = b["ansible_facts"]['ansible_processor_count']
                        asset_dict['cpu_core_count'] = b["ansible_facts"]['ansible_processor_vcpus']
                        asset_dict['cpu_model'] = b["ansible_facts"]['ansible_processor'][1]

                        asset_dict['ram_size'] = round(int(b["ansible_facts"]['ansible_memtotal_mb']) / 1024)
                        asset_dict['ram'] =  [{"capacity": asset_dict['ram_size'], "slot": "RAM slot #0", "model": "DRAM", "manufacturer": "Not Specified", "sn": "Not Specified", "asset_tag": "Not Specified"}]


                        nic_list = [b["ansible_facts"]['ansible_' + i.replace('-','_')] for i in b["ansible_facts"]['ansible_interfaces']]
                        nic_list_refactor = []

                        for nic_obj in nic_list:
                            nic_dict = {}
                            ipv4 = nic_obj.get('ipv4', None)
                            nic_dict['name'] = nic_obj.get('device', None)
                            nic_dict['mac'] = nic_obj.get('macaddress') or nic_obj['device']
                            nic_dict['net_mask'] = ipv4['netmask'] if ipv4 else None
                            nic_dict['network'] = ipv4['network'] if ipv4 else None
                            nic_dict['model'] = nic_obj.get('module') or nic_obj['device']
                            nic_dict['ip_address'] = ipv4['address'] if ipv4 else None
                            nic_dict['active'] = nic_obj['active']
                            nic_list_refactor.append(nic_dict)

                        asset_dict['nic'] = nic_list_refactor
                        asset_dict['physical_disk_driver'] = [{'model': b["ansible_facts"]['ansible_devices']['sda']['model'],
                                                               'capacity': float(b["ansible_facts"]['ansible_devices']['sda']['size'].split()[0]),
                                                               'sn': 'sda-'+b["ansible_facts"]['ansible_hostname'],
                                                               'manufacturer':b["ansible_facts"]['ansible_devices']['sda']['vendor'],
                                                               }
                                                              ]
                        #print(asset_dict)
                        asset.append(asset_dict)


                    # Centos
                    elif b["ansible_facts"].get('ansible_distribution'):

                        asset_dict['asset_type'] = 'server'
                        asset_dict['manufacturer'] = b["ansible_facts"]['ansible_system_vendor']
                        asset_dict['sn'] = b["ansible_facts"]['ansible_hostname']
                        asset_dict['model'] = b["ansible_facts"]['ansible_product_name']
                        asset_dict['uuid'] = b["ansible_facts"]['ansible_product_uuid']
                        asset_dict['os_distribution'] = b["ansible_facts"]['ansible_distribution']
                        asset_dict['os_release'] = b["ansible_facts"]['ansible_distribution_version']
                        asset_dict['os_type'] = b["ansible_facts"]['ansible_system']

                        asset_dict['cpu_count'] = b["ansible_facts"]['ansible_processor_count']
                        asset_dict['cpu_core_count'] = b["ansible_facts"]['ansible_processor_vcpus']
                        asset_dict['cpu_model'] = b["ansible_facts"]['ansible_processor'][1]

                        asset_dict['ram_size'] = round(int(b["ansible_facts"]['ansible_memtotal_mb']) / 1024)
                        asset_dict['ram'] =  [{"capacity": asset_dict['ram_size'], "slot": "RAM slot #0", "model": "DRAM", "manufacturer": "Not Specified", "sn": "Not Specified", "asset_tag": "Not Specified"}]


                        nic_list = [b["ansible_facts"]['ansible_' + i.replace('-','_')] for i in b["ansible_facts"]['ansible_interfaces']]
                        nic_list_refactor = []

                        for nic_obj in nic_list:
                            nic_dict = {}
                            ipv4 = nic_obj.get('ipv4', None)
                            nic_dict['name'] = nic_obj.get('device', None)
                            nic_dict['mac'] = nic_obj.get('macaddress') or nic_obj['device']
                            nic_dict['net_mask'] = ipv4['netmask'] if ipv4 else None
                            nic_dict['network'] = ipv4['network'] if ipv4 else None
                            nic_dict['model'] = nic_obj.get('module') or nic_obj['device']
                            nic_dict['ip_address'] = ipv4['address'] if ipv4 else None
                            nic_dict['active'] = nic_obj['active']
                            nic_list_refactor.append(nic_dict)

                        asset_dict['nic'] = nic_list_refactor
                        asset_dict['physical_disk_driver'] = [{'model': b["ansible_facts"]['ansible_devices']['sda']['model'],
                                                               'capacity': float(b["ansible_facts"]['ansible_devices']['sda']['size'].split()[0]),
                                                               'sn': 'sda-'+b["ansible_facts"]['ansible_hostname'],
                                                               'manufacturer':b["ansible_facts"]['ansible_devices']['sda']['vendor'],
                                                               }
                                                              ]

                        #print(asset_dict)
                        asset.append(asset_dict)
                except KeyError as e:
                    msg = {'error':e,'msg':b}
                    log('indatabase',msg=msg,new_asset=i)
                    # print (e)
                    # print ('keyerror:',b,i)

        for data in asset:
            sn = data.get('sn', None)

            if sn:
                asset_obj = models.Asset.objects.filter(sn=sn)  # [obj]
                if asset_obj:  # 资产更新
                    AutoUpdateAsset(request, asset_obj[0], data)
                    print('r:', request, 'asset:', asset_obj[0], 'data:', data)

                else:  # 资产新增
                    obj = AutoNewAsset(request, data)
                    obj.add_to_new_assets_zone()


        return True

class AutoNewAsset(object):
    '''
    新收集的资产进入待审批表
    '''
    def __init__(self, request, data):
        self.request = request
        self.data = data

    def add_to_new_assets_zone(self):
        defaults = {
            'data': json.dumps(self.data),
            'asset_type': self.data.get('asset_type'),
            'manufacturer': self.data.get('manufacturer'),
            'model': self.data.get('model'),
            'ram_size': self.data.get('ram_size'),
            'cpu_model': self.data.get('cpu_model'),
            'cpu_count': self.data.get('cpu_count'),
            'cpu_core_count': self.data.get('cpu_core_count'),
            'os_distribution': self.data.get('os_distribution'),
            'os_release': self.data.get('os_release'),
            'os_type': self.data.get('os_type'),
        }
        models.NewAssetApprovalZone.objects.update_or_create(sn=self.data['sn'], defaults=defaults)
        return '资产已经加入或者更新待审批区域！'


def log(log_type, msg=None, asset=None, new_asset=None, request=None):
    """
    记录日志
    """
    event = models.EventLog()
    if log_type == "upline":
        event.name = "%s <%s> ：  上线" % (asset.name, asset.sn)
        event.asset = asset
        event.detail = "资产成功上线！"
        event.user = request.user
    elif log_type == "approve_failed":
        event.name = "%s <%s> ：  审批失败" % (new_asset.asset_type, new_asset.sn)
        event.new_asset = new_asset
        event.detail = "审批失败！\n%s" % msg
        event.user = request.user
        # 更多日志类型.....
    elif log_type == "update":
        event.name = "%s <%s> ：  数据更新！" % (asset.asset_type, asset.sn)
        event.asset = asset
        event.detail = "更新成功！"
    elif log_type == "update_failed":
        event.name = "%s <%s> ：  更新失败" % (asset.asset_type, asset.sn)
        event.asset = asset
        event.detail = "更新失败！\n%s" % msg
    elif log_type == 'indatabase':
        event.name = "%s  ：  扫描进入审批区失败" % (new_asset)
        event.detail = "扫描进入审批区失败！\n%s" % msg
    event.save()


class ApproveAsset:
    """
    审批资产并上线。
    """
    def __init__(self, request, asset_id):
        self.request = request
        self.new_asset = models.NewAssetApprovalZone.objects.get(id=asset_id)
        self.data = json.loads(self.new_asset.data)

    def asset_upline(self):
        # 为以后的其它类型资产扩展留下接口
        func = getattr(self, '_%s_upline' % self.new_asset.asset_type)   # _server_upline
        ret = func()
        return ret

    def _server_upline(self):
        # 在实际的生产环境中，下面的操作应该是原子性的整体事务，任何一步出现异常，所有操作都要回滚。
        asset = self._create_asset()
        try:
            self._create_server(asset)  # 创建服务器
            self._create_CPU(asset)  # 创建CPU
            self._create_RAM(asset)  # 创建内存
            self._create_disk(asset)  # 创建硬盘
            self._create_nic(asset)  # 创建网卡
            self._create_manufacturer(asset)  # 创建厂商
            self._delete_original_asset()  # 从待审批资产区删除已审批上线的资产
        except Exception as e:
            asset.delete()
            log('approve_failed', msg=str(e), new_asset=self.new_asset, request=self.request)
            print(e)
            return False
        else:
            # 添加日志
            log("upline", asset=asset, request=self.request)
            print("新服务器上线!")
            return True

    def _create_asset(self):
        """
        创建资产并上线
        :return:
        """
        # 利用request.user自动获取当前管理人员的信息，作为审批人添加到资产数据中。
        asset = models.Asset.objects.create(asset_type=self.new_asset.asset_type,
                                            name="%s: %s" % (self.new_asset.asset_type, self.new_asset.sn),
                                            sn=self.new_asset.sn,
                                            approved_by=self.request.user,
                                            )
        return asset

    def _create_server(self, asset):
        """
       创建服务器
       :param asset:
       :return:
       """
        models.Server.objects.create(asset=asset,
                                     model=self.new_asset.model,
                                     os_type=self.new_asset.os_type,
                                     os_distribution=self.new_asset.os_distribution,
                                     os_release=self.new_asset.os_release,
                                     )

    def _create_manufacturer(self, asset):
        """
        创建厂商
        :param asset:
        :return:
        """
        # 判断厂商数据是否存在。如果存在，看看数据库里是否已经有该厂商，再决定是获取还是创建。
        m = self.new_asset.manufacturer
        if m:
            manufacturer_obj, _ = models.Manufacturer.objects.get_or_create(name=m)
            asset.manufacturer = manufacturer_obj
            asset.save()

    def _create_CPU(self, asset):
        """
        创建CPU.
        教程这里对发送过来的数据采取了最大限度的容忍，
        实际情况下你可能还要对数据的完整性、合法性、数据类型进行检测，
        根据不同的检测情况，是被动接收，还是打回去要求重新收集，请自行决定。
        这里的业务逻辑非常复杂，不可能面面俱到。
        :param asset:
        :return:
        """
        cpu = models.CPU.objects.create(asset=asset)
        cpu.cpu_model = self.new_asset.cpu_model
        cpu.cpu_count = self.new_asset.cpu_count
        cpu.cpu_core_count = self.new_asset.cpu_core_count
        cpu.save()

    def _create_RAM(self, asset):
        """
        创建内存。通常有多条内存
        :param asset:
        :return:
        """
        ram_list = self.data.get('ram')  # [ram1,ram2,ram3...]
        if not ram_list:  # 万一一条内存数据都没有
            return
        for ram_dict in ram_list:  # {...}
            if not ram_dict.get('slot'):
                raise ValueError("未知的内存插槽！")  # 使用虚拟机的时候，可能无法获取内存插槽，需要你修改此处的逻辑。
            ram = models.RAM()
            ram.asset = asset
            ram.slot = ram_dict.get('slot')
            ram.sn = ram_dict.get('sn')
            ram.model = ram_dict.get('model')
            ram.manufacturer = ram_dict.get('manufacturer')
            ram.capacity = ram_dict.get('capacity', 0)
            ram.save()

    def _create_disk(self, asset):
        """
        存储设备种类多，还有Raid情况，需要根据实际情况具体解决。
        这里只以简单的SATA硬盘为例子。可能有多块硬盘。
        :param asset:
        :return:
        """
        disk_list = self.data.get('physical_disk_driver')
        if not disk_list:  # 一条硬盘数据都没有
            return
        for disk_dict in disk_list:
            if not disk_dict.get('sn'):
                raise ValueError("未知sn的硬盘！")  # 根据sn确定具体某块硬盘。
            disk = models.Disk()
            disk.asset = asset
            disk.sn = disk_dict.get('sn')
            disk.model = disk_dict.get('model')
            disk.manufacturer = disk_dict.get('manufacturer'),
            disk.slot = disk_dict.get('slot')
            disk.capacity = disk_dict.get('capacity', 0)
            iface = disk_dict.get('interface_type')
            if iface in ['SATA', 'SAS', 'SCSI', 'SSD', 'unknown']:
                disk.interface_type = iface

            disk.save()

    def _create_nic(self, asset):
        """
        创建网卡。可能有多个网卡，甚至虚拟网卡。
        :param asset:
        :return:
        """
        nic_list = self.data.get("nic")
        if not nic_list:
            return

        for nic_dict in nic_list:
            if not nic_dict.get('mac'):
                raise ValueError("网卡缺少mac地址！")
            if not nic_dict.get('model'):
                raise ValueError("网卡型号未知！")

            nic = models.NIC()
            nic.asset = asset
            nic.name = nic_dict.get('name')
            nic.model = nic_dict.get('model')
            nic.mac = nic_dict.get('mac')
            nic.ip_address = nic_dict.get('ip_address')
            if nic_dict.get('net_mask'):
                if len(nic_dict.get('net_mask')) > 0:
                    nic.net_mask = nic_dict.get('net_mask')[0]
            nic.save()

    def _delete_original_asset(self):
        """
        这里的逻辑是已经审批上线的资产，就从待审批区删除。
        也可以设置为修改成已审批状态但不删除，只是在管理界面特别处理，不让再次审批，灰色显示。
        不过这样可能导致待审批区越来越大。
        :return:
        """
        self.new_asset.delete()


class AutoUpdateAsset:
    """
    自动更新已上线的资产。
    如果想让记录的日志更详细，可以逐条对比数据项，将更新过的项目记录到log信息中。
    """

    def __init__(self, request, asset, report_data):
        self.request = request
        self.asset = asset
        self.report_data = report_data            # 此处的数据是由客户端发送过来的整个数据字符串
        self.asset_update()

    def asset_update(self):
        # 为以后的其它类型资产扩展留下接口
        func = getattr(self, "_%s_update" % self.report_data['asset_type'])
        ret = func()
        return ret

    def _server_update(self):
        try:
            self._update_manufacturer()   # 更新厂商
            self._update_server()         # 更新服务器
            self._update_CPU()            # 更新CPU
            self._update_RAM()            # 更新内存
            self._update_disk()           # 更新硬盘
            self._update_nic()            # 更新网卡
            self.asset.save()
        except Exception as e:
            log('update_failed', msg=e, asset=self.asset, request=self.request)
            print(e)
            return False
        else:
            # 添加日志
            log("update", asset=self.asset)
            print("资产数据被更新!")
            return True

    def _update_manufacturer(self):
        """
        更新厂商
        """
        m = self.report_data.get('manufacturer')
        if m:
            manufacturer_obj, _ = models.Manufacturer.objects.get_or_create(name=m)
            self.asset.manufacturer = manufacturer_obj
        else:
            self.asset.manufacturer = None
        self.asset.manufacturer.save()

    def _update_server(self):
        """
        更新服务器
        """
        self.asset.server.model = self.report_data.get('model')
        self.asset.server.os_type = self.report_data.get('os_type')
        self.asset.server.os_distribution = self.report_data.get('os_distribution')
        self.asset.server.os_release = self.report_data.get('os_release')
        self.asset.server.save()

    def _update_CPU(self):
        """
        更新CPU信息
        :return:
        """
        self.asset.cpu.cpu_model = self.report_data.get('cpu_model')
        self.asset.cpu.cpu_count = self.report_data.get('cpu_count')
        self.asset.cpu.cpu_core_count = self.report_data.get('cpu_core_count')
        self.asset.cpu.save()

    def _update_RAM(self):
        """
        更新内存信息。
        使用集合数据类型中差的概念，处理不同的情况。
        如果新数据有，但原数据没有，则新增；
        如果新数据没有，但原数据有，则删除原来多余的部分；
        如果新的和原数据都有，则更新。
        在原则上，下面的代码应该写成一个复用的函数，
        但是由于内存、硬盘、网卡在某些方面的差别，导致很难提取出重用的代码。
        :return:
        """
        # 获取已有内存信息，并转成字典格式
        old_rams = models.RAM.objects.filter(asset=self.asset)
        old_rams_dict = dict()
        if old_rams:
            for ram in old_rams:
                old_rams_dict[ram.slot] = ram   # {'slot1':'...','slot2':'..'}
        # 获取新数据中的内存信息，并转成字典格式
        new_rams_list = self.report_data['ram']
        new_rams_dict = dict()
        if new_rams_list:
            for item in new_rams_list:
                new_rams_dict[item['slot']] = item  # {'slot2':'...','slot4':'..'}

        # 利用set类型的差集功能，获得需要删除的内存数据对象
        need_deleted_keys = set(old_rams_dict.keys()) - set(new_rams_dict.keys())
        if need_deleted_keys:
            for key in need_deleted_keys:
                old_rams_dict[key].delete()

        # 需要新增或更新的
        if new_rams_dict:
            for key in new_rams_dict:
                defaults = {
                            'sn': new_rams_dict[key].get('sn'),
                            'model': new_rams_dict[key].get('model'),
                            'manufacturer': new_rams_dict[key].get('manufacturer'),
                            'capacity': new_rams_dict[key].get('capacity', 0),
                            }
                models.RAM.objects.update_or_create(asset=self.asset, slot=key, defaults=defaults)

    def _update_disk(self):
        """
        更新硬盘信息。类似更新内存。
        """
        old_disks = models.Disk.objects.filter(asset=self.asset)
        old_disks_dict = dict()
        if old_disks:
            for disk in old_disks:
                old_disks_dict[disk.sn] = disk

        new_disks_list = self.report_data['physical_disk_driver']
        new_disks_dict = dict()
        if new_disks_list:
            for item in new_disks_list:
                new_disks_dict[item['sn']] = item

        # 需要删除的
        need_deleted_keys = set(old_disks_dict.keys()) - set(new_disks_dict.keys())
        if need_deleted_keys:
            for key in need_deleted_keys:
                old_disks_dict[key].delete()

        # 需要新增或更新的
        if new_disks_dict:
            for key in new_disks_dict:
                interface_type = new_disks_dict[key].get('interface_type', 'unknown')
                if interface_type not in ['SATA', 'SAS', 'SCSI', 'SSD', 'unknown']:
                    interface_type = 'unknown'
                defaults = {
                    'slot': new_disks_dict[key].get('slot'),
                    'model': new_disks_dict[key].get('model'),
                    'manufacturer': new_disks_dict[key].get('manufacturer'),
                    'capacity': new_disks_dict[key].get('capacity', 0),
                    'interface_type': interface_type,
                }
                models.Disk.objects.update_or_create(asset=self.asset, sn=key, defaults=defaults)

    def _update_nic(self):
        """
        更新网卡信息。类似更新内存。
        """
        old_nics = models.NIC.objects.filter(asset=self.asset)
        old_nics_dict = dict()
        if old_nics:
            for nic in old_nics:
                old_nics_dict[nic.model+nic.mac] = nic

        new_nics_list = self.report_data['nic']
        new_nics_dict = dict()
        if new_nics_list:
            for item in new_nics_list:
                new_nics_dict[item['model']+item['mac']] = item

        # 需要删除的
        need_deleted_keys = set(old_nics_dict.keys()) - set(new_nics_dict.keys())
        if need_deleted_keys:
            for key in need_deleted_keys:
                old_nics_dict[key].delete()

        # 需要新增或更新的
        if new_nics_dict:
            for key in new_nics_dict:
                if new_nics_dict[key].get('net_mask') and len(new_nics_dict[key].get('net_mask')) > 0:
                    net_mask = new_nics_dict[key].get('net_mask')[0]
                else:
                    net_mask = ""
                defaults = {
                    'name': new_nics_dict[key].get('name'),
                    'ip_address': new_nics_dict[key].get('ip_address'),
                    'net_mask': net_mask,
                }
                models.NIC.objects.update_or_create(asset=self.asset, model=new_nics_dict[key]['model'],
                                                    mac=new_nics_dict[key]['mac'], defaults=defaults)

        print('更新成功！')



