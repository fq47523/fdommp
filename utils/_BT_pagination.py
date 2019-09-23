from utils._fmt_date import DateFmt

class BtPaging(object):
    def __init__(self,TableClassName=None,PageJsonDate=None):
        self.TableName = TableClassName
        self.PageJsonDate = PageJsonDate
        self.page_date_list = []


        # print (self.TableName,self.PageJsonDate)

    def page_data_count(self):
        data_count = self.TableName.objects.all().count()
        return data_count

    def sort_query(self):
        sort_type = self.PageJsonDate['sort'] if self.PageJsonDate['sortOrder'] == 'asc' else '-' + self.PageJsonDate['sort']
        sort_query_obj = self.TableName.objects.all().values().order_by(sort_type)[(self.PageJsonDate['page'] - 1) * self.PageJsonDate['rows']:self.PageJsonDate['rows'] * self.PageJsonDate['page']]
        return sort_query_obj


    def page_query(self):
        page_query_obj = self.TableName.objects.all()[(self.PageJsonDate['page'] - 1) * self.PageJsonDate['rows']:self.PageJsonDate['rows'] * self.PageJsonDate['page']]
        return page_query_obj

    def host_paging(self):

        if 'sort' in self.PageJsonDate:
            sort_query_data = self.sort_query()



            for i in sort_query_data:
                self.self.page_date_list.append(i)

            table_paging_data = {'total': int(self.page_data_count()), 'rows': self.page_date_list}

            return table_paging_data

        else:

            page_query_data = self.page_query()


            for i in page_query_data:
                gouzhao = {}
                try:
                    host_zabbix_obj = i.host_zabbix_set.all().values()

                    gouzhao['h_id'] = i.h_id
                    gouzhao['h_name'] = i.h_name
                    gouzhao['h_ip'] = i.h_ip
                    gouzhao['h_status'] = 'ok' if host_zabbix_obj[0]['za_action'] == 0 else 'not ok'
                    gouzhao['h_cpu'] = host_zabbix_obj[0]['za_cpu']
                    gouzhao['h_mem'] = host_zabbix_obj[0]['za_mem']
                    gouzhao['h_disk'] = host_zabbix_obj[0]['za_disk']
                    self.page_date_list.append(gouzhao)
                except IndexError:
                    gouzhao['h_id'] = i.h_id
                    gouzhao['h_name'] = i.h_name
                    gouzhao['h_ip'] = i.h_ip
                    gouzhao['h_status'] = 'not zabbix-agentd'
                    gouzhao['h_cpu'] = '---'
                    gouzhao['h_mem'] = '---'
                    gouzhao['h_disk'] = '---'
                    self.page_date_list.append(gouzhao)

            table_paging_data = {'total': int(self.page_data_count()), 'rows': self.page_date_list}

            return table_paging_data


    def server_paging(self):
        if 'sort' in self.PageJsonDate:
            sort_query_data = self.sort_query()

            for i in sort_query_data:
                self.self.page_date_list.append(i)

            table_paging_data = {'total': int(self.page_data_count()), 'rows': self.page_date_list}

            return table_paging_data

        else:

            page_query_data = self.page_query()

            for i in page_query_data:
                structure = {}

                structure['s_id'] = i.s_id
                structure['s_name'] = i.s_name
                structure['s_type'] = i.s_type
                structure['s_host'] = [ host['h_ip'] for host in i.h_server.all().values()]

                self.page_date_list.append(structure)


            table_paging_data = {'total': int(self.page_data_count()), 'rows': self.page_date_list}

            return table_paging_data


    def confd_paging(self):
        page_query_data = self.page_query()

        for i in page_query_data:
            structure = {}
            structure['conf_id'] = i.id
            structure['create_date'] = i.create_date.strftime('%Y-%m-%d %H:%M:%S')
            structure['edit_date'] = i.edit_date.strftime('%Y-%m-%d %H:%M:%S')
            structure['server_type'] = [server_type['s_name'] for server_type in i.conf_service.all().values()]
            structure['hostip'] = [host['h_ip'] for host in i.conf_host.all().values()]
            structure['conf_name'] = i.conf_name
            structure['conf_path'] = i.conf_path
            structure['current_ver'] = i.current_ver
            structure['modified_ver'] = i.modified_ver

            self.page_date_list.append(structure)

        table_paging_data = {'total': int(self.page_data_count()), 'rows': self.page_date_list}


        return table_paging_data


    def confd_rollback_paging(self,conf_id):
        page_query_data = self.TableName.objects.filter(conf_id=conf_id)[(self.PageJsonDate['page'] - 1) * self.PageJsonDate['rows']:self.PageJsonDate['rows'] * self.PageJsonDate['page']]

        for i in page_query_data:
            structure = {}
            structure['cuh_id'] = i.cuh_id
            structure['conf_id'] = i.conf_id
            structure['backup_ver'] = i.backup_ver
            structure['backup_date'] = i.backup_date.strftime('%Y-%m-%d %H:%M:%S')

            self.page_date_list.append(structure)

        table_paging_data = {'total': int(self.page_data_count()), 'rows': self.page_date_list}

        return table_paging_data



    def log_paging(self,log_fileter_obj):
        page_data = log_fileter_obj[
                    (self.PageJsonDate['page'] - 1) * self.PageJsonDate['rows']:self.PageJsonDate['rows'] * self.PageJsonDate['page']]

        for i in page_data:
            structure = {}
            structure['create_time'] = i.create_time.strftime('%Y-%m-%d %H:%M:%S')
            structure['log_type'] = i.log_type
            structure['module'] = i.module
            structure['user'] = i.user
            structure['status'] = i.status
            structure['description'] = i.description
            self.page_date_list.append(structure)

        table_paging_data = {'total': int(log_fileter_obj.count()), 'rows': self.page_date_list}

        return table_paging_data