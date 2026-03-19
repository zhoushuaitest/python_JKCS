import sys, os
from  common.Readyaml import   get_testcase_yaml
from  common.models import  ReadYamlData
import  json
import  re
import  jsonpath
from common.debugtalk import Debugtalk
from common.Sendrequests import Sendrequests
from  conf.operationConfig import OperationConfig
from  common.recordlog import logs
from common.assertions import Assertions


assert_res = Assertions()
class BaseRequest:
    def __init__(self):
        self.read = ReadYamlData()
        self.send = Sendrequests()
        self.conf = OperationConfig()

    def replace_load(self, data):
        """
        将extract。yaml文件中的数据进行解析
        :return:
        """
        # 判断读取的文件数据是什么类型,如果不是就将他转成字符串
        str_data = data
        original_is_str = isinstance(data, str)
        if not original_is_str:
            # serialize non-string data to JSON string for placeholder replacement
            str_data = json.dumps(data, ensure_ascii=False)
            # print(str_data)


        # 用循环判断有多少个$标识的额
        for i in range(str_data.count('${')):
            if "${" in str_data and "}" in str_data:
                # index检测是否为字符串，并找到字符串的索引位置
                start_index = str_data.index('$')
                end_index = str_data.index('}', start_index)
                # 通过找到开头和结尾的索引可以将${}取出来
                ref_startdata = str_data[start_index:end_index + 1]
                # 打印出循环取出的$
                # 通过索引的方式取出函数名
                func_name = ref_startdata[2:ref_startdata.index('(')]
                # 取出里面的参数值
                func_pream = ref_startdata[ref_startdata.index('(') + 1:ref_startdata.index(')')]
  # 传入替换的参数获取对应的值 通过用python中的getatt,这就是反射,Debugtalk()代表对象，func_name代表函数名，(func_pream)代表传入的参数
                extract_data = getattr(Debugtalk(), func_name)(*func_pream.split(',') if func_pream else '')
 # 替换解析后的完整的testcase.yaml数据
 #                str_data = str_data.replace(ref_startdata, str(excract_data))
                if extract_data and isinstance(extract_data, list):
                    extract_data = ','.join(e for e in extract_data)
                str_data = str_data.replace(ref_startdata, str(extract_data))


        #还原数据
        # Try to parse the result back to Python object (dict/list) if possible.
        if data and isinstance(data, dict):
            data = json.loads(str_data)
        else:
            data = str_data
        return data

    #参数md5加密
    def md5_parme(self,parme):
        return 'admin' + str(parme)

    #封装方法，进行读取接口文件中的信息
    def specification_yaml(self,case_info):
        """
        规范yaml接口数据的写法
        :param case_info:指yaml文件中的2数据信息
        :return:
        """
        #接口地址
        base_url = self.conf.get_envi('host')
        # print(base_url)   #http://127.0.0.1:8787

        params_type = ['params' ,'data' ,'json']
        #路径
        url =  case_info['baseInfo']['url']
        # print(url)
        andurl =base_url + url
        # print(andurl)
        api_name = case_info['baseInfo']['url']
        # print(api_name)
        method = case_info['baseInfo']['method']
        # print(method)
        header = case_info['baseInfo']['header']
        # print(header)
        try:
            cookies = self.replace_load(case_info['baseInfo']['cookies'])
        except:
            pass

        # 通过循环将yaml文件中testcase数据取出来
        for tc in case_info['testcase']:

            case_name = tc.pop('case_name')
            validation = tc.pop('validation')
            extract = tc.pop('extract',None)
            # print('extract值为' ,extract)
            #获取yaml文件中为list的情况
            extract_list = tc.pop('extract_list',None)
            #判断
            for key, value in tc.items():
            #判断testcase中，数据的方式为data /paremes/json  再去调用·解析数据
                if key in params_type:
                    tc[key] = self.replace_load(value)
            #**tc 表示传入数据tc tc为yaml文件中的数据data,为了方便，自动传入去判断是data 还是praeme,还是json
            res = self.send.run_main(name=api_name,url=andurl,case_name=case_name,method=method,header=header,cookies=cookies,flie=None,**tc)
            print(res)
            res_text = res.text
            res_json = res.json()
            if extract is not None:
                #这一步是去调用extract_data方法中，测试yaml文件中的正则，json提取值，提取到获取接口返回值中的关联数据，
                self.extract_data(extract,res_text)
            if extract_list is not None:
                #这一步是获取接口返回的列表数据
                self.extract_data_list(extract_list,res_text)
            #处理接口断言
            assert_res.assert_result(validation, res_json, res.status_code)


    #获取接口返回值，并写入Extarct文件中
    def extract_data(self, testcase_extarct, response):
        """
        提取接口的返回值，支持正则表达式和json提取器
        :param testcase_extarct: testcase文件yaml中的extract值
        :param response: 接口的实际返回值
        :return:
        """
        try:
            pattern_lst = ['(.*?)', '(.+?)', r'(\d)', r'(\d*)']
            for key, value in testcase_extarct.items():
                print(key, value)
                # 处理正则表达式提取
                for pat in pattern_lst:
                    if pat in value:
                        ext_lst = re.search(value, response)
                        if pat in [r'(\d+)', r'(\d*)']:
                            extract_data = {key: int(ext_lst.group(1))}
                        else:
                            extract_data = {key: ext_lst.group(1)}
                        self.read.write_yaml(extract_data)
                # 处理json提取参数
                if '$' in value:
                    ext_json = jsonpath.jsonpath(json.loads(response), value)[0]
                    if ext_json:
                        extarct_data = {key: ext_json}
                        logs.info('提取接口的返回值：', extarct_data)
                    else:
                        extarct_data = {key: '未提取到数据，请检查接口返回值是否为空！'}
                    self.read.write_yaml(extarct_data)
        except Exception as e:
            logs.error(e)

    def extract_data_list(self, testcase_extract_list, response):
        """
        提取多个参数，支持正则表达式和json提取，提取结果以列表形式返回
        :param testcase_extract_list: yaml文件中的extract_list信息
        :param response: 接口的实际返回值,str类型
        :return:
        """
        try:
            for key, value in testcase_extract_list.items():
                if "(.+?)" in value or "(.*?)" in value:
                    ext_list = re.findall(value, response, re.S)
                    if ext_list:
                        extract_date = {key: ext_list}
                        logs.info('正则提取到的参数：%s' % extract_date)
                        self.read.write_yaml(extract_date)
                if "$" in value:
                    # 增加提取判断，有些返回结果为空提取不到，给一个默认值
                    ext_json = jsonpath.jsonpath(json.loads(response), value)
                    if ext_json:
                        extract_date = {key: ext_json}
                    else:
                        extract_date = {key: "未提取到数据，该接口返回结果可能为空"}
                    logs.info('json提取到参数：%s' % extract_date)
                    self.read.write_yaml(extract_date)
        except:
            logs.error('接口返回值提取异常，请检查yaml文件extract_list表达式是否正确！')




if __name__ == '__main__':
    data =get_testcase_yaml('../testcase/login/login.yaml')[0]
    data2 = get_testcase_yaml('../testcase/login/adduser.yaml')[0]
    data3 = get_testcase_yaml('../testcase/delect/delect.yaml')[0]
    base = BaseRequest()
    base.specification_yaml(data2)
    # base.specification_yaml(data2)

    #调试adduser中添加数据
    # data2 = get_testcase_yaml('../testcase/systemmansege/systemmansege.yaml')[0]
    # base.specification_yaml(data2)
#解析接口关联数据
    # data = get_testcase_yaml('../testcase/adduser/adduser.yaml')[0]
    # base = BaseRequest()
    # base.specification_yaml(data)

    #再进行调用
    # print(a)
    # base.specification_yaml(a )
    # #调用添加用户方法
    # # #获取URL,先将他序列化，字符串转化为字典
    # # make sure we have a dict
    # dict_data = a if isinstance(a, dict) else json.loads(a)
    # print(dict_data)
    # url = dict_data['baseInfo']['url']
    # print(url)
    # # # #获取header
    # header =dict_data['baseInfo']['header']
    # print(header)
    # # # # 获取data
    # data = dict_data['testCase'][0]['data']
    # print(data)
    # # # #获取请求方式
    # method = dict_data['baseInfo']['method']
    # # # 输出对应的yaml文件中的数据
    # print(method)
    # #
    # A = Sendrequests()
    # CS = A.run_main(method=method, url=url, data=data, header=header)
    # print(CS)
