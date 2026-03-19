import random

from  common.models  import  ReadYamlData
class Debugtalk:
    def __init__(self):
        self.read = ReadYamlData()
 #写一个方法，进行调用读取extract.yaml文件中LIST的数据，方便面做参数动态读取
    def get_extract_data_list(self, node_name,randoms=None):

        data = self.read.read_extract_yaml(node_name)
        if randoms is not None:
            randoms = int(randoms)
            data_value = {
                randoms: 1,
                0: random.choice(data),
                -1: ','.join(data),
            }
            data = data_value[randoms]
        return data

        #专门读取extract.yaml文件中有嵌套的数据
    def get_extract_data(self, node_name,   sec_node_name=None):
        data = self.read.read_extract_yaml(node_name,sec_node_name)
        return data


    #参数md5加密
    def md5_parame(self,parme):
        return 'admin' + str(parme)

if __name__ == '__main__':
    debugtalk = Debugtalk()
    rse_extractyaml = debugtalk.get_extract_data('cookies','session')
    print(rse_extractyaml)