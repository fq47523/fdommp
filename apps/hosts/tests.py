import sys
import os
from django.conf import settings
pwd = os.path.dirname(os.path.realpath(__file__))



sys.path.append(pwd + "../../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fdommp.settings")

import django
django.setup()

# git
# from git import  Repo
#
# url = 'https://github.com/fq47523/fdommp-dockerfile.git'
# gitpath = '/tmp/testgit'
#
#
# # Repo.clone_from(url, gitpath,multi_options=['--depth=1'])
# git_repo = Repo(gitpath)
# print (git_repo.branches)
# print (git_repo.tags)
from rest_framework_jwt.utils import  jwt_payload_handler
# from django.contrib.auth.models import User
# from rest_framework_jwt.settings import api_settings
# userobj = User.objects.get(username='fuqing')
# jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
# jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
#
# payload = jwt_payload_handler(userobj)
# token = jwt_encode_handler(payload)
# print (token)
import json
b = {'ansible_facts': {'ansible_all_ipv4_addresses': ['192.168.79.134', '172.17.0.1', '172.19.0.1', '172.18.0.1'], 'ansible_all_ipv6_addresses': ['fe80::9852:91ff:fe83:74a0', 'fe80::20c:29ff:fec2:14ab', 'fe80::885e:70ff:fe17:1fbf', 'fe80::42:3aff:fe0e:ad5b'], 'ansible_architecture': 'x86_64', 'ansible_bios_date': '07/02/2015', 'ansible_bios_version': '6.00', 'ansible_br_5eb40caf2429': {'active': False, 'device': 'br-5eb40caf2429', 'id': '8000.024228fed5b5', 'interfaces': [], 'ipv4': {'address': '172.18.0.1', 'broadcast': '172.18.255.255', 'netmask': '255.255.0.0', 'network': '172.18.0.0'}, 'macaddress': '02:42:28:fe:d5:b5', 'mtu': 1500, 'promisc': False, 'stp': False, 'type': 'bridge'}, 'ansible_br_98c78b3a9494': {'active': True, 'device': 'br-98c78b3a9494', 'id': '8000.02423a0ead5b', 'interfaces': ['vethb9a4f78', 'veth7f6ad9f'], 'ipv4': {'address': '172.19.0.1', 'broadcast': '172.19.255.255', 'netmask': '255.255.0.0', 'network': '172.19.0.0'}, 'ipv6': [{'address': 'fe80::42:3aff:fe0e:ad5b', 'prefix': '64', 'scope': 'link'}], 'macaddress': '02:42:3a:0e:ad:5b', 'mtu': 1500, 'promisc': False, 'stp': False, 'type': 'bridge'}, 'ansible_cmdline': {'BOOT_IMAGE': '/boot/vmlinuz-4.4.0-87-generic', 'find_preseed': '/preseed.cfg', 'noprompt': True, 'quiet': True, 'ro': True, 'root': 'UUID=a495a7cd-deb0-417f-95e7-c23a933c1f43'}, 'ansible_date_time': {'date': '2019-10-30', 'day': '30', 'epoch': '1572423418', 'hour': '16', 'iso8601': '2019-10-30T08:16:58Z', 'iso8601_basic': '20191030T161658310434', 'iso8601_basic_short': '20191030T161658', 'iso8601_micro': '2019-10-30T08:16:58.310568Z', 'minute': '16', 'month': '10', 'second': '58', 'time': '16:16:58', 'tz': 'CST', 'tz_offset': '+0800', 'weekday': 'Wednesday', 'weekday_number': '3', 'weeknumber': '43', 'year': '2019'}, 'ansible_default_ipv4': {'address': '192.168.79.134', 'alias': 'ens33', 'broadcast': '192.168.79.255', 'gateway': '192.168.79.2', 'interface': 'ens33', 'macaddress': '00:0c:29:c2:14:ab', 'mtu': 1500, 'netmask': '255.255.255.0', 'network': '192.168.79.0', 'type': 'ether'}, 'ansible_default_ipv6': {}, 'ansible_devices': {'sda': {'holders': [], 'host': 'SCSI storage controller: LSI Logic / Symbios Logic 53c1030 PCI-X Fusion-MPT Dual Ultra320 SCSI (rev 01)', 'model': 'VMware Virtual S', 'partitions': {'sda1': {'sectors': '37748736', 'sectorsize': 512, 'size': '18.00 GB', 'start': '2048'}, 'sda2': {'sectors': '2', 'sectorsize': 512, 'size': '1.00 KB', 'start': '37752830'}, 'sda5': {'sectors': '4188160', 'sectorsize': 512, 'size': '2.00 GB', 'start': '37752832'}}, 'removable': '0', 'rotational': '1', 'scheduler_mode': 'deadline', 'sectors': '41943040', 'sectorsize': '512', 'size': '20.00 GB', 'support_discard': '0', 'vendor': 'VMware,'}, 'sr0': {'holders': [], 'host': 'SATA controller: VMware SATA AHCI controller', 'model': 'VMware SATA CD01', 'partitions': {}, 'removable': '1', 'rotational': '1', 'scheduler_mode': 'deadline', 'sectors': '1689600', 'sectorsize': '2048', 'size': '3.22 GB', 'support_discard': '0', 'vendor': 'NECVMWar'}}, 'ansible_distribution': 'Ubuntu', 'ansible_distribution_major_version': '16', 'ansible_distribution_release': 'xenial', 'ansible_distribution_version': '16.04', 'ansible_dns': {'nameservers': ['192.168.79.2'], 'search': ['localdomain']}, 'ansible_docker0': {'active': False, 'device': 'docker0', 'id': '8000.0242323e58a9', 'interfaces': [], 'ipv4': {'address': '172.17.0.1', 'broadcast': '172.17.255.255', 'netmask': '255.255.0.0', 'network': '172.17.0.0'}, 'macaddress': '02:42:32:3e:58:a9', 'mtu': 1500, 'promisc': False, 'stp': False, 'type': 'bridge'}, 'ansible_domain': '', 'ansible_ens33': {'active': True, 'device': 'ens33', 'ipv4': {'address': '192.168.79.134', 'broadcast': '192.168.79.255', 'netmask': '255.255.255.0', 'network': '192.168.79.0'}, 'ipv6': [{'address': 'fe80::20c:29ff:fec2:14ab', 'prefix': '64', 'scope': 'link'}], 'macaddress': '00:0c:29:c2:14:ab', 'module': 'e1000', 'mtu': 1500, 'pciid': '0000:02:01.0', 'promisc': False, 'type': 'ether'}, 'ansible_env': {'HOME': '/root', 'LANG': 'en_US.UTF-8', 'LANGUAGE': 'en_US:', 'LC_ALL': 'en_US.UTF-8', 'LC_MESSAGES': 'en_US.UTF-8', 'LOGNAME': 'root', 'MAIL': '/var/mail/root', 'PATH': '/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games', 'PWD': '/root', 'SHELL': '/bin/bash', 'SHLVL': '1', 'SSH_CLIENT': '192.168.79.134 50916 22', 'SSH_CONNECTION': '192.168.79.134 50916 192.168.79.134 22', 'SSH_TTY': '/dev/pts/7', 'TERM': 'xterm', 'USER': 'root', 'XDG_RUNTIME_DIR': '/run/user/0', 'XDG_SESSION_ID': '422', '_': '/usr/bin/python'}, 'ansible_fips': False, 'ansible_form_factor': 'Other', 'ansible_fqdn': 'ubuntu', 'ansible_hostname': 'ubuntu', 'ansible_interfaces': ['docker0', 'br-98c78b3a9494', 'lo', 'veth7f6ad9f', 'br-5eb40caf2429', 'vethb9a4f78', 'ens33'], 'ansible_kernel': '4.4.0-87-generic', 'ansible_lo': {'active': True, 'device': 'lo', 'ipv4': {'address': '127.0.0.1', 'broadcast': 'host', 'netmask': '255.0.0.0', 'network': '127.0.0.0'}, 'ipv6': [{'address': '::1', 'prefix': '128', 'scope': 'host'}], 'mtu': 65536, 'promisc': False, 'type': 'loopback'}, 'ansible_lsb': {'codename': 'xenial', 'description': 'Ubuntu 16.04.6 LTS', 'id': 'Ubuntu', 'major_release': '16', 'release': '16.04'}, 'ansible_machine': 'x86_64', 'ansible_machine_id': '92d81600c402ddebf4ee66c15a50db13', 'ansible_memfree_mb': 124, 'ansible_memory_mb': {'nocache': {'free': 1055, 'used': 2879}, 'real': {'free': 124, 'total': 3934, 'used': 3810}, 'swap': {'cached': 4, 'free': 2023, 'total': 2044, 'used': 21}}, 'ansible_memtotal_mb': 3934, 'ansible_mounts': [{'device': '/dev/sda1', 'fstype': 'ext4', 'mount': '/', 'options': 'rw,relatime,errors=remount-ro,data=ordered', 'size_available': 3127353344, 'size_total': 18889830400, 'uuid': 'a495a7cd-deb0-417f-95e7-c23a933c1f43'}], 'ansible_nodename': 'ubuntu', 'ansible_os_family': 'Debian', 'ansible_pkg_mgr': 'apt', 'ansible_processor': ['GenuineIntel', 'Intel(R) Core(TM) i5-6300U CPU @ 2.40GHz', 'GenuineIntel', 'Intel(R) Core(TM) i5-6300U CPU @ 2.40GHz'], 'ansible_processor_cores': 1, 'ansible_processor_count': 2, 'ansible_processor_threads_per_core': 1, 'ansible_processor_vcpus': 2, 'ansible_product_name': 'VMware Virtual Platform', 'ansible_product_serial': 'VMware-56 4d ce e7 c1 7c c1 2b-ad a4 73 04 93 c2 14 ab', 'ansible_product_uuid': '564DCEE7-C17C-C12B-ADA4-730493C214AB', 'ansible_product_version': 'None', 'ansible_python_version': '2.7.12', 'ansible_selinux': {'status': 'disabled'}, 'ansible_service_mgr': 'systemd', 'ansible_ssh_host_key_dsa_public': 'AAAAB3NzaC1kc3MAAACBAKNq+mdGjliGGhcUxwO+kmrmZzbm/llhPipWyXosOQQCd/bx8KqzcKVaCGKmSsA4RUid88yw+d57ITwce+sN0FVje0iRLUU92Yy9KAMJW+WK2l7Skq1U2qb3vY0cV5vfQPWJVaHzE5BwjGQhXW1EBVNRjk4H3lm8KLlMy99zRF/BAAAAFQCK4tS3qxmlIof3rsQVxagPV5MkxwAAAIAye+LRZwKAPjY+Cb+Brf4Qy6ZTlJbTtIU9suWdEP7uM/hO1fARKHcPhM43h9D2VMQZYfm/ioiClfm+fpjqaUPqQVMdBIOGOY1TzaJG5ToUdK7kl87teFeKh8heoJ8DDjb/7ZMjW2GNYNposgCRe+94kWcL5KzjUSqMZUD9WntxuQAAAIEAh5QFbjra4Eu1gKIU1Uc5kuZFqJDbKgJXgCyyhielGwOaqkGurGS95sceVNwdIUhNMiu7BfsRPml4d6LtNsejXuC0rlMuGUksoIST6Eui29nSN/a1/x30sv1AlzoUFx09ugvQFJhDSvq/lxVXdkbs4GTY9Z67dwdiUVt8WV5x8go=', 'ansible_ssh_host_key_ecdsa_public': 'AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBDDxoCnDiIdCwOa64OYLhFn2XpwJ9NFfU6rCtcM5M6D4Xg4OY7FdNs3zwj1PdFVIjEL3J5x1SoWaPSXV+rn0EBk=', 'ansible_ssh_host_key_ed25519_public': 'AAAAC3NzaC1lZDI1NTE5AAAAILuDWvBjmsRSt5X8fEEZwh14w8aGMYfPEHu8m1PGbYlg', 'ansible_ssh_host_key_rsa_public': 'AAAAB3NzaC1yc2EAAAADAQABAAABAQD1+tiBobzgSJ71sP/exRm86XFns3CX5eDpjVlVI1Ftl9qoj0x3AiAKt/lP/2EoqaSJwYQ0KVANeoNgJ6gpqMV7OX65UxOUtGXCeOSLL40UQWd2kchTbYgVxJQ8agyXczJXvyXfejjM81SLx1xW0MLl5HJPhdc6lntYYJSohPGjIjeSuH8Lm61CI2PTihl2KG1+claTv7GWtoOE0q3+OA2q+iCeHVrcRJtn56werNmcuA4UZWlzDY5/X5ZeDms+RbyESuBUzosx9dJ/u7E40aoHrdkuCFLWCJZFn1yjYcBJ8x0nndk0wlNfJ+/5bI/bWzFG/LKjGhIRUEDkV1Qtssd5', 'ansible_swapfree_mb': 2023, 'ansible_swaptotal_mb': 2044, 'ansible_system': 'Linux', 'ansible_system_vendor': 'VMware, Inc.', 'ansible_uptime_seconds': 24199, 'ansible_user_dir': '/root', 'ansible_user_gecos': 'root', 'ansible_user_gid': 0, 'ansible_user_id': 'root', 'ansible_user_shell': '/bin/bash', 'ansible_user_uid': 0, 'ansible_userspace_architecture': 'x86_64', 'ansible_userspace_bits': '64', 'ansible_veth7f6ad9f': {'active': True, 'device': 'veth7f6ad9f', 'ipv6': [{'address': 'fe80::885e:70ff:fe17:1fbf', 'prefix': '64', 'scope': 'link'}], 'macaddress': '8a:5e:70:17:1f:bf', 'mtu': 1500, 'promisc': True, 'type': 'ether'}, 'ansible_vethb9a4f78': {'active': True, 'device': 'vethb9a4f78', 'ipv6': [{'address': 'fe80::9852:91ff:fe83:74a0', 'prefix': '64', 'scope': 'link'}], 'macaddress': '9a:52:91:83:74:a0', 'mtu': 1500, 'promisc': True, 'type': 'ether'}, 'ansible_virtualization_role': 'guest', 'ansible_virtualization_type': 'VMware', 'module_setup': True}, 'changed': False}
asset_dict = {}
# print (json.dumps(b,indent=4))

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
asset_dict['ram'] = [
    {"capacity": asset_dict['ram_size'], "slot": "RAM slot #0", "model": "DRAM", "manufacturer": "Not Specified",
     "sn": "Not Specified", "asset_tag": "Not Specified"}]

nic_list = [b["ansible_facts"]['ansible_' + i.replace('-','_')] for i in b["ansible_facts"]['ansible_interfaces']]
print (nic_list)
nic_list_refactor = []

for nic_obj in nic_list:
    nic_dict = {}
    ipv4 = nic_obj.get('ipv4',None)
    nic_dict['name'] = nic_obj.get('device',None)
    nic_dict['mac'] = nic_obj.get('macaddress') or nic_obj['device']
    nic_dict['net_mask'] =  ipv4['netmask'] if ipv4 else None
    nic_dict['network'] = ipv4['network'] if ipv4 else None
    nic_dict['model'] = nic_obj.get('module') or nic_obj['device']
    nic_dict['ip_address'] = ipv4['address'] if ipv4 else None
    nic_dict['active'] = nic_obj['active']
    nic_list_refactor.append(nic_dict)
    # print (nic_obj)

asset_dict['nic'] = nic_list_refactor
asset_dict['physical_disk_driver'] = [{'model': b["ansible_facts"]['ansible_devices']['sda']['model'],
                                       'capacity': float(
                                           b["ansible_facts"]['ansible_devices']['sda']['size'].split()[0]),
                                       'sn': 'sda-' + b["ansible_facts"]['ansible_hostname'],
                                       'manufacturer': b["ansible_facts"]['ansible_devices']['sda']['vendor'],
                                       }
                                      ]

print (asset_dict)

