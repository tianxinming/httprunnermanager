import io
import json
import time
import ast
import yaml


def get_time_stamp():
    ct = time.time()
    local_time = time.localtime(ct)
    data_head = time.strftime("%Y-%m-%d %H-%M-%S", local_time)
    data_secs = (ct - int(ct)) * 1000
    time_stamp = "%s-%03d" % (data_head, data_secs)
    return time_stamp


def dump_yaml_file(yaml_file, data):
    """ load yaml file and check file content format
    """
    """循环遍历data，将字典中file所对应值的双引号去掉，否则写入yaml文件中的数据不符合上传附件接口的格式"""
    # for item in data:
    #     if "test" in item.keys():
    #         if "files" in item["test"]["request"].keys():
    #             for key in item["test"]["request"]["files"]:
    #                 file_list = ast.literal_eval(item["test"]["request"]["files"][key])
    #                 item["test"]["request"]["files"][key] = file_list

    with io.open(yaml_file, 'w', encoding='utf-8') as stream:
        print("写入yaml文件...")
        yaml.dump(data, stream, indent=4, default_flow_style=False, encoding='utf-8', allow_unicode=True)
    print("写入yaml文件完成...")


def _dump_json_file(json_file, data):
    """ load json file and check file content format
    """
    with io.open(json_file, 'w', encoding='utf-8') as stream:
        json.dump(data, stream, indent=4, separators=(',', ': '), ensure_ascii=False)


def dump_python_file(python_file, data):
    with io.open(python_file, 'w', encoding='utf-8') as stream:
        stream.write(data)

    print("写入debugtalk文件数据：%s" % data)
    print("写入debugtalk文件成功：%s" % python_file)
