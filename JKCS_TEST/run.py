import  pytest
import  os
if __name__ == '__main__':
    #主函数选择执行的测试用例
    # pytest.main(['-vs',  'testcase/systemmansege/test_delect.py'])
    # 主函数执行所有测试用例,需要指定目录
    # pytest.main(['-vs',  'testcase'])
    #通过分布式执行测试用例，指定线程数
    # pytest.main(['-vs',  'testcase' ,'-n 6'])
    pytest.main()
    os.system(f'allure serve  report/temp')

    # pytest.main(["-vs", "testcase", "--alluredir=./report/temp"])
    # os.system("allure generate ./report/temp -o ./report/report --clean")
    # os.system("allure open ./report/report")

