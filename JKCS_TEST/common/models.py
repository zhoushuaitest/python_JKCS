import yaml
import  os
from conf.setting import FILE_PATH
class ReadYamlData:
    def __init__(self, yaml_file=None):
        if yaml_file is not None:
            self.yaml_file = yaml_file
        else:
            self.yaml_file = '../testcase/login/login.yaml'

    def write_yaml(self, value):
        file = None
        file_path = FILE_PATH['EXTRACT']
        if not os.path.exists(file_path):
            os.system(file_path)

        try:
            file = open(file_path, 'a', encoding='utf-8')
            if isinstance(value, dict):
                write_data = yaml.dump(value, allow_unicode=True, sort_keys=False)
                file.write(write_data)
            else:
                print('写入到[extract.yaml]的数据必须是字典类型格式！')
        except Exception as e:
            print(e)
        finally:
            file.close()



    # def read_extract_yaml(self, vaule):
    #     """
    #     读取extracr.yaml文件中的数据
    #     :param node_name:
    #     :return:
    #     """
    #     try:
    #         with open('../EXTRACT.yaml', 'r', encoding='utf-8') as f:
    #             yaml_read = yaml.safe_load(f.read())
    #             return yaml_read[vaule]
    #     except Exception as e:
    #         print(e)

    def read_extract_yaml(self, node_name, second_node_name=None):
        """
        用于读取接口提取的变量值
        :param node_name:
        :return:
        """
        if os.path.exists(FILE_PATH['EXTRACT']):
            pass
        else:
            print('EXTRACT.yaml不存在')
            file = open(FILE_PATH['EXTRACT'], 'w')
            file.close()
            print('extract.yaml创建成功！')
        try:
            with open(FILE_PATH['EXTRACT'], 'r', encoding='utf-8') as rf:
                ext_data = yaml.safe_load(rf)
                if second_node_name is None:
                    return ext_data[node_name]
                else:
                    return ext_data[node_name][second_node_name]
        except Exception as e:
            print(f"【extract.yaml】没有找到：{node_name},--%s" % e)

    #写入一个方法，每次执行后，将excart.yaml文件中的数据进行清理

    def clear_extract_data(self):
        """
        清除extract.yaml文件的数据
        :return:
        """
        with open(FILE_PATH['EXTRACT'], 'w') as f:
            f.truncate()