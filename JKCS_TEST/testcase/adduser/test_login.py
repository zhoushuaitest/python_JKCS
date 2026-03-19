import json
import allure
import  pytest
#进行前后置处理
from common.Readyaml import get_testcase_yaml
from  common.Sendrequests import Sendrequests
from  common.recordlog import  *
from base.apiutil import  BaseRequest


class Test_login:
    #登录成功用例
    #设置执行顺序
    # @pytest.mark.run(order=1)
    #skip 通过跳过测试用例
    # @pytest.mark.skip
    #读取测试用例中数据
    # testcase / login / login.yaml
    @allure.story('用户登录测试一')
    @pytest.mark.parametrize('params' ,get_testcase_yaml('testcase/adduser/login.yaml'))
    def test_login1(self,params):
        time.sleep(2)
        print("获取到的参数为",params)
        BaseRequest().specification_yaml(params)

        # 提取URL
    #     url = params['baseInfo']['url']
    #     new_url = 'http://127.0.0.1:8787' + str(url)
    #     method = params['baseInfo']['method']
    #     data = params['testcase'][0]['data']
    #     header = params['baseInfo']['header']
    #     send = Sendrequests()
    #     CS = send.run_main(method=method,url=new_url  ,data=data,header=header)
    #     B = json.loads(CS)
    #     print(B)
    # #     # 获取Log
    #     logs.info(CS)
    #     assert  B['msg'] == '登录成功'
    # @allure.story('用户登录测试二')
    # @pytest.mark.parametrize('params', get_testcase_yaml('testcase/login/login.yaml'))
    # def test_login2(self, params):
    #     time.sleep(2)
    #     print("获取到的参数为", params)
    #     BaseRequest().specification_yaml(params)
        # 提取URL
        # url = params['baseInfo']['url']
        # new_url = 'http://127.0.0.1:8787' + str(url)
        # method = params['baseInfo']['method']
        # data = {'user_name':'test01' ,'passwd':'124124'}
        # header = params['baseInfo']['header']
        # send = Sendrequests()
        # CS = send.run_main(method=method, url=new_url, data=data, header=header)
        # B = json.loads(CS)
        # print(B)
        # #     # 获取Log
        # logs.info(CS)
        # assert B['msg'] == '登录失败,用户名或密码错误'

if __name__ == '__main__':
    pytest.main()
    os.system(f'allure serve ./report/temp')