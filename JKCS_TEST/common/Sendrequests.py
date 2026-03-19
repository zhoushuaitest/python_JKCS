import  pytest
import  requests
import  json
import yaml
from common.recordlog import  logs
from  common.models import  ReadYamlData
from  requests import  utils
class Sendrequests:
    def __init__(self):
        self.read = ReadYamlData()
    #封装请求方式
    def send_request(self, **kwargs):
        cookie = {}
        session = requests.session()
        result =   None
        try:
            result = session.request(**kwargs)
            set_cookie = requests.utils.dict_from_cookiejar(result.cookies)
            #将ccokie写入到extract.yaml文件中
            if set_cookie:
                cookie['Cookie'] = set_cookie
                self.read.write_yaml(set_cookie)
                logs.info(f'cookie为 : {cookie}')
            logs.info(f'接口的实际返回信息为： : {result.text if result.text else result}')
        except requests.exceptions.ConnectionError:
            logs.error("ConnectionError--连接异常")
            pytest.fail("接口请求异常，可能是request的连接数过多或请求速度过快导致程序报错！")
        except requests.exceptions.HTTPError:
            logs.error("HTTPError--http异常")
        except requests.exceptions.RequestException as e:
            logs.error(e)
            pytest.fail("请求异常，请检查系统或数据是否正常！")
        return result

    #定义一个主函数，可以去调用不同的请求方式
    def run_main(self, name, url, case_name,header, method,cookies=None,flie=None,**kwargs):

        """

                        :param url: 请求地址
                        :param header: 请求头
                        :param data: 请求参数
                        :param method: 请求方法
                        :return:
                        """
        try:
            # 收集报告日志信息
            logs.info('接口名称：{}'.format(name))
            logs.info('接口请求地址：{}'.format(url))
            logs.info(f'请求方法：{method}')
            logs.info(f'测试用例名称：{case_name}')
            logs.info(f'请求头：{header}')
            logs.info(f'cookies：{cookies}')
            # 处理请求参数,因为请求参数有data/parmas/json数据格式
            req_params = json.loads(kwargs, ensure_ascii=False)
            # kwargs = {'data': {'user_name': '${get_params()}', 'passwd': 'admin123'}}
            if 'data' in kwargs.keys():
                logs.info(f'请求参数：{kwargs}')
            elif 'json' in kwargs.keys():
                logs.info(f'请求参数：{kwargs}')
            elif 'params' in kwargs.keys():
                logs.info(f'请求参数：{kwargs}')
            # return req_params

        except Exception as e:
            logs.error(e)
        response = self.send_request(method=method, url=url, headers=header,cookies=cookies, files=flie, verify=False,
                                 **kwargs)
        return response


if __name__ == '__main__':
    url2 = 'http://127.0.0.1:8787/coupApply/cms/goodsList'

    header2 = {'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}

    json_data2 = {
        "msgType": "getHandsetListOfCust",
        "page": 1,
        "size": 20
    }
    method2 = 'get'
#
#POST 请求
    url = 'http://127.0.0.1:8787/dar/user/login'

    header = {'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}

    data = {
        "user_name": "test01",
        "passwd": "admin123"
    }
    method = 'post'
    A = Sendrequests()
    # print(A.send_get(url=url2,data=json_data2,header=header2))
    # print(A.send_post(url=url,data=data,header=header))
    #get请求
    CS = A.run_main(method=method2,url=url2,data=json_data2,header=header2)
    print(CS)
#post请求
    CS2 = A.run_main(method=method,url=url,data=data,header=header)
    print(CS2)