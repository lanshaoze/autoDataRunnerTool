import json
import re
import os
import glob
import generate_docx
import pytest
# from conftest import setup_channels
from Singleton import Singleton

log_dir = 'logs'
logs_data = {}
final_result = {}
# tag_base = r'用户通用事件报送'
tag_base = 'auto_runner_log'
pattern = fr'{tag_base}.*channel_init_success|{tag_base}.*login|{tag_base}.*enter_server|{tag_base}.*payment'
# print(pattern)
tag_list = [tag_base]
# tag_list = ["auto_runner_log"]

def deal_original():
    for filename in glob.glob(os.path.join(log_dir, '*.txt')):
        with open(filename, 'rb') as f:
            # ignore or replace
            log = f.read().decode('utf-8', 'ignore')

        # 解析日志内容
        result = parse_log(log)

        # print(result)
        # logs_data = parse_log(log)
        # 保存解析结果
        logs_data[filename] = result
    # print(logs_data)


def parse_log(log):
    data = []
    for line in log.split('\n'):
        if any(tag in line for tag in tag_list):
            # print(line)
            # remove pattern
            data.append(line.strip())
            # if re.search(pattern,line):
            #     # print(line.strip())
            #     data.append(line.strip())

    return data


def parse_result():
    pattern = r'(\d+-\d+ \d+:\d+:\d+)'
    for key, data in logs_data.items():
        for value in data:
            # print(value)
            action = None
            vlus = None
            temp = {}
            if 'action:' in value:
                action = re.search(r'action:(\w+)', value).group(1)
            if 'values:' in value:
                vlus = json.loads(re.search(r'values:(.+)', value).group(1))


            if action and vlus:
                temp[action] = vlus
                # channelid = re.search(r"'channelid':\s*'(\w+)'", str(temp)).group(1)
                # # print("channelid:", channelid)
                # gameid = re.search(r"'gameid':\s*'(\w+)'", str(temp)).group(1)
                # # print("gameid:", gameid)
                # key = channelid + '_' + gameid
                key = re.search(r"'adChannel':\s*'(\w+)'", str(temp)).group(1)
                # print(key)
                if key not in final_result:
                    final_result[key] = {}
                final_result[key][action] = vlus
                # 读取时间
                match = re.search(pattern, value)
                if match:
                    vlus["time"] = match.group(1)

            print('{}:{}'.format(action,vlus))
    # print('keys--->',final_result.keys())
    singleTon = Singleton()
    for key, value in final_result.items():
        singleTon.set(key, value)

def build_docx():
    generate_docx.build_docx(final_result)


def getChannels():
    print('channnnn--->', final_result.keys())
    return final_result.keys()


dst_file = "docx/dest.txt"
if __name__ == '__main__':
    deal_original()
    parse_result()
    build_docx()
    pytest.main([
        'test_run.py', '-v', '--html=./html/report.html',
        '--self-contained-html'
    ])

    # if dst_file:
    #     os.truncate(dst_file,0)
    # cmd = "grep -E {} {} > {}".format(tag_list,"logs/new_log.txt",dst_file)
    # os.system(cmd)
    # print(data['payment'])
    # print("payment:{}".format(data['payment']['pay_status']))
