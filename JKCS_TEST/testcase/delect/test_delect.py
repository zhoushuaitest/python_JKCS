import time
import pytest
import  os
from common.Readyaml import  get_testcase_yaml
from base.apiutil import  BaseRequest
import allure

class Test_adduser:

    @allure.story('删除用户测试')
    @pytest.mark.parametrize('params', get_testcase_yaml('testcase/delect/delect.yaml'))
    def test_login1(self, params):
        print("获取到的参数为", params)
        time.sleep(2)
        BaseRequest().specification_yaml(params)

if __name__ == '__main__':
    pytest.main()
