import configparser
import os
from conf.setting import FILE_PATH

#封装方法进行读取config.ini配置文件
class OperationConfig:

    def __init__(self,file_path = None):
        #在setting文件中读取ini文件的路径
        if file_path is None:
            self.__file_path = FILE_PATH['CONFIG']
        else:
            self.__file_path = file_path

        self.conf = configparser.ConfigParser()
        # 在setting文件中读取ini文件的路径
        try:
            self.conf.read(self.__file_path,encoding='utf-8')
        except Exception as e:
            print(e)

    def get_section_for_data(self,section,option):
        try:
            data = self.conf.get(section,option)
            return data
        except Exception as e:
            print(e)

    #再封装一个方法，用来进行读取ini文件中数据
    def get_envi(self,option):
        return self.get_section_for_data('api_envi',option)

    #读取MYSQL配置
    def get_myswl_conf(self,option):
        return self.get_section_for_data('MYSQL',option)

if __name__ == '__main__':
    poer = OperationConfig()
    a = poer.get_envi('url')
    print(a)