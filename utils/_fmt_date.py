import datetime

class DateFmt(object):
    def __init__(self,date):
        self.date = date

    @property
    def date_fmt_1(self):
        '''
        '2019-03-30 09:47:23' str convert datetime
        :return:
        '''
        fmt_date_ret = datetime.datetime.strptime(self.date, "%Y-%m-%d %H:%M:%S")
        return fmt_date_ret

    @property
    def date_fmt_2(self):
        '''
        2019-07-29 10:15:52.421 str convert 2019-07-29 10:15:52 str
        :return:
        '''
        return self.date.split('.')[0]




if __name__ == '__main__':

    a = '2019-07-29 10:15:52.421'
    # print (a.split('.')[0])
    # c = DateFmt(a)
    print (DateFmt(a).date_fmt_2)