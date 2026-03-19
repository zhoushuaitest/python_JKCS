import time
import pytest
import  os
from common.Readyaml import  get_testcase_yaml
from base.apiutil import  BaseRequest
import allure

class Test_adduser:

#进行参数化处理：里面有多少个参数，该用例就会执行多少遍
    # @pytest.mark.run(order=1)
    # @allure.story('用户登录测试')
    # @pytest.mark.parametrize('params' ,get_testcase_yaml('testcase/adduser/login.yaml'))
    # def test_adduser(self,params):
    #     print("获取到的参数为", params)
    #     BaseRequest().specification_yaml(params)


    # @pytest.mark.run(order=2)
    @allure.story('添加用户测试')
    @pytest.mark.parametrize('params', get_testcase_yaml('testcase/login/adduser.yaml'))
    def test_login1(self, params):
        print("获取到的参数为", params)
        time.sleep(2)
        BaseRequest().specification_yaml(params)

if __name__ == '__main__':
    pytest.main()
