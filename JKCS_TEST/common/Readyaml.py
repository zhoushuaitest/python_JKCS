#读取yaml文件中的数据，进行接口测试数据的读取
import os

from common.Sendrequests import Sendrequests
import yaml
import  json
from common.models import ReadYamlData
#定义一个方法，并读取Yaml文件中的数据，进行接口测试数据的读取
def get_testcase_yaml(file):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            yaml_read = yaml.safe_load(f.read())
            return yaml_read

    except Exception as e:
        print(e)



    # 将读取的数据写入到yaml中
# class ReadYamlData:
#         def __init__(self, yaml_file=None):
#             if yaml_file is not None:
#                 self.yaml_file = yaml_file
#             else:
#                 self.yaml_file = '../testcase/login/login.yaml'
#
#         def write_yaml(self, value):
#             """
#
#             :param value: 写入的数据·
#             :return:
#             """
#             # 创建一个需要写入的文件
#             try:
#                 # 这个文件为setting.py中的文件路径
#                 file_path = '../EXTRACT.yaml'
#                 # 将这个文件先打开，再进行写入
#                 with open(file_path, 'w', encoding='utf-8') as f:
#                     # 判断写入的文件是否为字典，如果不是字典，则提示
#                     if isinstance(value, dict):
#                         # 将要写入的VALUE,进行写入加入allow_unicode=True表示可以写入中文
#                         yaml_write = yaml.dump(value, allow_unicode=True)
#                         f.write(yaml_write)
#                     else:
#                         print('写入到【extract.yaml】文件中的格式必须为字典')
#             except Exception as e:
#                 print(e)
#
#
#             #写一个方法，进行读取extract.yaml文件中的数据，方便面做参数动态读取
#         def read_extract_yaml(self, vaule):
#             """
#             读取extracr.yaml文件中的数据
#             :param node_name:
#             :return:
#             """
#             try:
#                 with open('../EXTRACT.yaml', 'r', encoding='utf-8') as f:
#                     yaml_read = yaml.safe_load(f.read())
#                     return yaml_read[vaule]
#             except Exception as e:
#                 print(e)

if __name__ == '__main__':
    TEST = get_testcase_yaml('../testcase/login/login.yaml')
    print(TEST)
#
# #获取URL
    url = TEST[0]['baseInfo']['url']
    add_url ='http://127.0.0.1:8787' + str(url)
    print(add_url)
# #获取header
    header = TEST[0]['baseInfo']['header']
    print(header)
# # 获取data
    data = TEST[0]['testcase'][0]['data']
    print(data)
# # #获取请求方式
    method = TEST[0]['baseInfo']['method']
    #输出对应的yaml文件中的数据
    print(method)

    A = Sendrequests()
    CS = A.run_main(method=method, url=add_url , data=data, header=header)
    print(CS)
    print(type(CS))
#
#     # #通过反序列化将STR变为JSON
    token_res = json.loads(CS)
    print(token_res)
    # 获取token
    token = token_res.get('token')
    print(token)
#
#     #定义一个字典，将token进行写入到字典中
    token_dict = {}
    token_dict['token'] = token
    print(token_dict)

    B = ReadYamlData()
    B.write_yaml(token_dict)

    #读取extract.yaml文件中的数据
    print(B.read_extract_yaml('token'))


#
