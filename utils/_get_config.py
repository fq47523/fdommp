import configparser
import  os

class ConfigR(object):
    def __init__(self):
        #if os.getenv('FDOMMP_RUN_ENV') == 'DEV':
        #    self.conf_ini_file = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '/fdommp/dev_env.ini'

        self.cf = configparser.ConfigParser()
        self.cf.read(self.conf_ini_file)



    def sections_name(self):
        '''
        :return: all  sections_name
        '''
        self.sn = self.cf.sections()

        return self.sn

    def sections_add(self,sections_name):
        '''
        :return: add sections_name
        '''
        self.cf.add_section(sections_name)
        with open(self.path, 'w+')as conf:
            self.cf.write(conf)

        return 200


    def sections_delete(self,sections_name):
        '''
        :return: del  sections_name
        '''
        self.cf.remove_section(sections_name)
        with open(self.path, 'w+')as conf:
            self.cf.write(conf)

        return 200



    def sections_key(self,key):
        '''
        :return: all  sections_key
        '''
        self.sk = self.cf.options(key)

        return self.sk

    def sections_value(self,sections,key):
        '''
        :return:  sections_key  value
        '''
        self.sv = self.cf.get(sections,key)

        return self.sv


    def sections_value_modify(self,sections,key,newvalue):
        '''
        :return:  sections_key  value
        '''
        self.cf.set(sections,key,newvalue)
        with open(self.path, 'w+')as conf:
            self.cf.write(conf)

        return 200

    def sections_value_delete(self,sections,key):
        '''
        :return:  sections_key  value
        '''
        self.cf.remove_option(sections,key)
        with open(self.path, 'w+')as conf:
            self.cf.write(conf)

        return 200


if __name__ == '__main__':

    get_f = ConfigR()
    print (get_f.sections_value('debug','DEBUG'))




