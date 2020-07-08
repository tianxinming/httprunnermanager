#自定义函数，用于扩展相关功能
import json
import re

import requests

def formatTestResult(my,project_name,test_user,key,env):
    new_dict = {}
    test_details = my["details"]
    new_dict["success"] = my["success"]
    new_dict["stat"] = my["stat"]
    new_dict["time"] = {"startTime": my["time"]["start_datetime"], "duration": my["time"]["duration"]}
    # 存放具体的失败的测试用例
    fail_list = []
    for i in test_details:
        # 存放临时的失败的用例
        temp_dict = {}
        if i["success"]:
            pass
        else:
            # 放置重现步骤:
            repeat_step = {}
            temp_dict["summary"] = i["name"]
            temp_dict["success"] = False
            temp_dict["belong_project"] = project_name
            temp_dict["reporter"] = test_user
            for j in i["records"]:
                if j["status"] == "failure":
                    #实际中去掉xlog相关的信息 add by yqw 2020/6/5
                    j["meta_data"]["request"]["url"] = re.sub("\?.+","",j["meta_data"]["request"]["url"])
                    temp_dict["description"] = j["meta_data"]["request"]["headers"].pop("xlogpath")
                    #end
                    repeat_step["request"] = j["meta_data"]["request"]
                    repeat_step["actual"] = j["meta_data"]["response"]
                    repeat_step["expect"] = j["meta_data"]["validators"]
                    break
            temp_dict["repeat_steps"] = repeat_step
            temp_dict["jira_key"] = key
            temp_dict["env"] = env
            fail_list.append(temp_dict)
    new_dict["details"] = fail_list
    return new_dict

def submitToJira(jira_key,env_name,test_data):
    #CMDB生产环境
    host_port = '193.112.206.36:11025'
    param = {"accesskey": "zOxmraYdEwqMytSSq", "secretkey": "OdyoWyKjYBZFHNrOowtvqhQaB"}
    #CMDB开发环境
    # host_port = "118.126.92.41:1543"
    # param = {"accesskey": "YyDNzioZGlsMntfRj", "secretkey": "erMLOiVeMSbVgXVpIRvMqMisH"}

    #获取token
    url = "http://%s/gettoken" % host_port
    data = requests.get(url, param)
    print(data.text)
    token = json.loads(data.text)["data"]["token"]
    subUrl = "http://%s/api/v1/cmdb/aiops/autotests/manual_add/" % host_port
    data_info = {"jira_key":jira_key,"env_name":env_name,"test_data":test_data}
    header = {"Authorization":"Token %s" % token}
    #提交JIRA
    returnValue = requests.post(url=subUrl,data=data_info,headers=header)

if __name__ == "__main__":
    jira_key = "TEST"
    env_name = "test"
    test_data = ""
    submitToJira(jira_key,env_name,test_data)