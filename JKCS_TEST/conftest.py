import  pytest
from  common.models import  ReadYamlData


"""
-function：每一个函数或方法都会调用
-class：每一个类调用一次，一个类中可以有多个方法
-module：每一个.py文件调用一次，该文件内又有多个function和class
-session：是多个文件调用一次，可以跨.py文件调用，每个.py文件就是module,整个会话只会运行一次
-autouse：默认为false，不会自动执行，需要手动调用，为true可以自动执行，不需要调用
- yield：前置、后置
"""







read = ReadYamlData()
@pytest.fixture(scope='session', autouse=True)
def clear_extract():
    read.clear_extract_data()

@pytest.fixture(scope='function', autouse=True)
def fixture_test():
    print('============开始接口测试================')
    yield
    print("============结束接口测试================")