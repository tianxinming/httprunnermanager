import datetime
import hashlib
import os
import time

import pytz
from django.core.exceptions import ObjectDoesNotExist

from ApiManager.models import TestCaseInfo, ModuleInfo, ProjectInfo, DebugTalk, TestSuite
from ApiManager.utils.testcase import dump_python_file, dump_yaml_file

def getXlogPath(timestamp,signNo):
    #默认前后各一个小时
    interval = 3600
    local_tz = pytz.timezone("Asia/Shanghai")
    local_format = "%Y-%m-%d %H:%M:%S"
    time_str = time.strftime(local_format, time.localtime(timestamp-interval))
    dt = datetime.datetime.strptime(time_str, local_format)
    local_dt = local_tz.localize(dt, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)
    startTime = utc_dt.strftime("%Y-%m-%dT%H:%M:%SZ")

    time_str = time.strftime(local_format, time.localtime(timestamp + interval))
    dt = datetime.datetime.strptime(time_str, local_format)
    local_dt = local_tz.localize(dt, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)
    endTime = utc_dt.strftime("%Y-%m-%dT%H:%M:%SZ")

    urlPath = "https://xlog.pagoda.com.cn/app/kibana#/discover?_g=(refreshInterval:(display:Off,pause:!f,value:0),time:(from:'{}',mode:absolute,to:'{}'))&_a=(columns:!(_source),index:c45a0650-cb70-11e8-bc02-afb1529a08c5,interval:auto,query:(language:kuery,query:'x_params : {}'),sort:!(timestamp,desc))".format(
        startTime, endTime, signNo)
    return urlPath

def run_by_single(index, base_url, path):
    # print("1:%s"%index)
    # print("2:%s"%base_url)
    # print(path)
    """
    加载单个case用例信息
    :param index: int or str：用例索引
    :param base_url: str：环境地址
    :return: dict
    """
    config = {
        'config': {
            'name': '',
            'request': {
                'base_url': base_url
            }
        }
    }
    testcase_list = []

    testcase_list.append(config)

    try:
        obj = TestCaseInfo.objects.get(id=index)
        print(obj.request)
    except ObjectDoesNotExist:
        return testcase_list

    include = eval(obj.include)
    print("include为%s"%include)
    request = eval(obj.request)
    #start:新增xlog的日志地址 --add by yqw 2020/5/26
    h1 = hashlib.md5()
    now_time = time.time()
    myData = "{}{}{}".format(base_url, request, now_time)
    h1.update(myData.encode(encoding="utf-8"))
    sign = h1.hexdigest()
    t = request.get('test').get('request')
	#修复header没用的bug add by yqw 2020/6/19
    if t.get("headers"):
        t["headers"]["xlogPath"] = getXlogPath(now_time,sign)
    else:
	
        t["headers"] = {"xlogPath":getXlogPath(now_time,sign)}
    t["url"] = "{}?xlogSign={}".format(t["url"],sign)
    #end:
    name = obj.name
    project = obj.belong_project
    module = obj.belong_module.module_name
    run_mode = obj.run_mode
    print("run_mode:%s" % run_mode)

    config['config']['name'] = name

    testcase_dir_path = os.path.join(path, project)

    if not os.path.exists(testcase_dir_path):
        os.makedirs(testcase_dir_path)

        try:
            obj = DebugTalk.objects.filter(belong_project__project_name=project)
            # 合并多个debugtalk文件
            debugtalk = ""
            for i in obj:

                debugtalk += i.debugtalk
        except ObjectDoesNotExist:
            debugtalk = ''

        dump_python_file(os.path.join(testcase_dir_path, 'debugtalk.py'), debugtalk)

    testcase_dir_path = os.path.join(testcase_dir_path, module)

    if not os.path.exists(testcase_dir_path):
        os.mkdir(testcase_dir_path)

    for test_info in include:
        try:
            if isinstance(test_info, dict):
                config_id = test_info.pop('config')[0]
                config_request = eval(TestCaseInfo.objects.get(id=config_id).request)
                config_request.get('config').get('request').setdefault('base_url', base_url)
                config_request['config']['name'] = name
                testcase_list[0] = config_request
            else:
                id = test_info[0]
                pre_request = eval(TestCaseInfo.objects.get(id=id).request)
                testcase_list.append(pre_request)

        except ObjectDoesNotExist:
            return testcase_list

    if request['test']['request']['url'] != '':
        testcase_list.append(request)
        print("用例数据为%s"% testcase_list)


    dump_yaml_file(os.path.join(testcase_dir_path, name + '.yml'), testcase_list)


def run_by_suite(index, base_url, path):
    obj = TestSuite.objects.get(id=index)

    include = eval(obj.include)

    for val in include:
        run_by_single(val[0], base_url, path)


def run_by_batch(test_list, base_url, path, type=None, mode=False):
    """
    批量组装用例数据
    :param test_list:
    :param base_url: str: 环境地址
    :param type: str：用例级别
    :param mode: boolean：True 同步 False: 异步
    :return: list
    """
    print("test_list:", test_list)
    if mode:
        for index in range(len(test_list) - 3):
            form_test = test_list[index].split('=')
            value = form_test[1]
            if type == 'project':
                run_by_project(value, base_url, path)
            elif type == 'module':
                run_by_module(value, base_url, path)
            elif type == 'suite':
                run_by_suite(value, base_url, path)
            else:
                run_by_single(value, base_url, path)

    else:
        if type == 'project':
            for value in test_list.values():
                run_by_project(value, base_url, path)

        elif type == 'module':
            for value in test_list.values():
                run_by_module(value, base_url, path)
        elif type == 'suite':
            for value in test_list.values():
                run_by_suite(value, base_url, path)

        else:
            for index in range(len(test_list) - 1):
                form_test = test_list[index].split('=')
                index = form_test[1]
                run_by_single(index, base_url, path)


def run_by_module(id, base_url, path):
    """
    组装模块用例
    :param id: int or str：模块索引
    :param base_url: str：环境地址
    :return: list
    """
    obj = ModuleInfo.objects.get(id=id)
    test_index_list = TestCaseInfo.objects.filter(belong_module=obj, type=1, is_complete="Y").values_list('id', 'run_mode')
    # run_mode = TestCaseInfo.objects.filter(belong_module=obj, type=1).values_list('run_mode')
    # print("运行:%s"%run_mode)
    # print("123:%s"%type(run_mode))
    # #run_mode = run_mode_list.pop('run_mode')
    # # print("模式:%s"%run_mode)
    # # print(type(run_mode))
    # print("分析%s"%test_index_list)
    for index in test_index_list:
        print("用例执行类型%s" % index[1])
        if index[1] in "集成":
            continue
        else:
            run_by_single(index[0], base_url, path)


def run_by_project(id, base_url, path):
    """
    组装项目用例
    :param id: int or str：项目索引
    :param base_url: 环境地址
    :return: list
    """
    if id:
        obj = ProjectInfo.objects.get(id=id)
        module_index_list = ModuleInfo.objects.filter(belong_project=obj).values_list('id')

        for index in module_index_list:
            module_id = index[0]
            run_by_module(module_id, base_url, path)


def run_test_by_type(id, base_url, path, type):
    print(path)
    if type == 'project':
        run_by_project(id, base_url, path)
    elif type == 'module':
        run_by_module(id, base_url, path)
    elif type == 'suite':
        run_by_suite(id, base_url, path)
    else:
        run_by_single(id, base_url, path)
