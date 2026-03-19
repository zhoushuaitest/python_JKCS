import sys
import time
import pytest
import allure
from common.Readyaml import  get_testcase_yaml
from base.apiutil import BaseRequest
class TestList:
    @allure.story('获取商品列表')
    @pytest.mark.parametrize('params' ,get_testcase_yaml('testcase/systemmansege/systemmansege.yaml'))
    def test_login1(self,params):
        time.sleep(2)
        print("获取到的参数为",params)
        BaseRequest().specification_yaml(params)

    @allure.story('获取商品详情')
    @pytest.mark.parametrize('params', get_testcase_yaml('testcase/systemmansege/Guanlian.yaml'))
    def test_login2(self, params):
        time.sleep(2)
        print("获取到的参数为02", params)
        BaseRequest().specification_yaml(params)


if __name__ == '__main__':
    pytest.main()