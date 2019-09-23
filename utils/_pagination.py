__author__ = 'Administrator'
from django.utils.safestring import mark_safe


class Page:
    '''
    标签样式：Bootstrap
    current_page: 前端请求页码
    data_count： 数据量总计
    per_page_count： 每页显示多少条数据
    pager_num：返回客户端的页码个数
    '''
    def __init__(self, current_page, data_count, per_page_count=8, pager_num=7,onclick=None):
        self.current_page = current_page
        self.data_count = data_count
        self.per_page_count = per_page_count
        self.pager_num = pager_num
        self.onclick = onclick

    @property
	# 根据前端页码显示那部分数据
    def start(self):
        return (self.current_page - 1) * self.per_page_count

    @property
    def end(self):
        return self.current_page * self.per_page_count

	# 返回前端的页码总数（总数据量除以每页显示多少条数据，如果有余数总页码条数+1）	
    @property
    def total_count(self):
        v, y = divmod(self.data_count, self.per_page_count)
        if y:
            v += 1
        return v    # 101个页码
	# 页码逻辑
    def page_str(self, base_url):
        page_list = []  # 空页码列表
		# 数据量页码 < 指定页码数
        if self.total_count < self.pager_num:
            start_index = 1
            end_index = self.total_count + 1
        else:
			# 请求的页码 <=  4
            if self.current_page <= (self.pager_num + 1) / 2:
                start_index = 1
                end_index = self.pager_num + 1
            else:
				# 请求的页码 - 3
                start_index = self.current_page - (self.pager_num - 1) / 2	# 2
                # 请求的页码 + 4
                end_index = self.current_page + (self.pager_num + 1) / 2	# 9
				# 45 > 50
                if (self.current_page + (self.pager_num - 1) / 2) > self.total_count:
                    end_index = self.total_count + 1
                    start_index = self.total_count - self.pager_num + 1

        # 如果请求页码 == 1 点击就无效果,否则返回一个请求页码 - 1 的<a></a>标签
        if self.current_page == 1:
            prev = '<li><a class="page" href="javascript:void(0);">&laquo;</a></li>'
        else:
            prev = '<li><a class="page" target=%s onclick="%s">&laquo;</a></li>' % (self.current_page - 1,self.onclick)
        page_list.append(prev)
        # 得到页码逻辑的结果,循环返回标签给前端
        for i in range(int(start_index), int(end_index)):
            # 如果i == 当前请求的页码,就给他多个样式
            if i == self.current_page:
                temp = "<li class='active'><a target=%s onclick='%s'>%s</a></li>" % (i,self.onclick, i)
            else:
                temp = "<li><a  target=%s onclick='%s'>%s</a></li>" % (i,self.onclick, i)
            page_list.append(temp)
        # 如果请求页码 == 数据量页码 点击就无效果,否则返回一个请求页码 + 1 的<a></a>标签
        if self.current_page == self.total_count:
            # print (self.current_page,self.total_count)
            nex = '<li><a class="page" href="javascript:void(0);">&raquo;</a></li>'
        else:
            nex = '<li><a class="page" target="%s" onclick="%s">&raquo;</a></li>' % (self.current_page + 1,self.onclick)
        page_list.append(nex)

        jump = """
        <input type='text'  /><a onclick='jumpTo(this, "%s?p=");'>GO</a>
        <script>
            function jumpTo(ths,base){
                var val = ths.previousSibling.value;
                location.href = base + val;
            }
        </script>
        """ % (base_url,)



        page_list.append(jump)

        page_str = mark_safe("".join(page_list))

        return page_str
