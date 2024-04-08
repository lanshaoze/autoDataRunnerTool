import re

import pytest
from docxtpl import RichText
from pytest_html import extras
from conftest import get_channel,getData
# if __name__ == '__main__':
#     pytest.main([
#         'test_run.py', '-v', '--html=./directory/report.html',
#         '--self-contained-html'
#     ])

def getDataByChannel(channel):
    result = getData()
    return result[channel]

@pytest.mark.parametrize('channel', get_channel())
def test_channel(channel):
    # '''执行初始化测试'''
    ed = getDataByChannel(channel)
    print(f'\n开始测试渠道:{channel}的初始化功能')
    channel_init = "success" if has_field(ed, 'channel_init_success') else "fail"
    print('初始化:', channel_init)
    print(f'\n开始测试渠道:{channel}的登录功能')
    login = "success" if has_field(ed, 'login') else "fail"
    print('登录:', login)
    print(f'\n开始测试渠道:{channel}的进服功能')
    enter_server = "success" if has_field(ed, 'enter_server') else "fail"
    print('进服:', enter_server)
    print(f'\n开始测试渠道:{channel}的支付功能')
    payment = "success" if has_field(ed, 'payment') and ed['payment']['pay_status'] == 'success' else "fail"
    print('支付:', payment)
    result = '通过' if channel_init == 'success' and login == 'success' and enter_server == 'success' and payment == 'success' else "不通过"
    print(f"\n测试结果:",result)
    print('=============BI相关==================')
    print('支付:', "success" if has_field(ed, 'payment') and ed['payment']['pay_status'] == 'success' else "fail")
    print('渠道：', match_field(str(ed), 'channel'))
    print('游戏id:', match_field(str(ed), 'gameid'))
    print('渠道id:', match_field(str(ed), 'channelid'))
    print('胡莱uid:', match_field(str(ed), 'uid'))
    print('支付金额:', "{}{}".format(round(ed['payment']['price']/1000,1),ed['payment']['currency']) if has_field(ed, 'payment') else None)
    print('=============BI相关==================')
    print('=============行为日志==================')
    print("行为日志：",ed)

    assert True if result == '通过' else False
    extras.channel = channel


# @pytest.mark.parametrize('channel', get_channel())
# def test_init(channel):
#     '''执行初始化测试'''
#     print(f'\n开始测试渠道:{channel}的初始化功能')
#     ed = getDataByChannel(channel)
#     print('初始化:', "success" if has_field(ed, 'channel_init_success') else "fail")
#     channel = match_field(str(ed), 'channel')
#     channel_init = "success" if has_field(ed, 'channel_init_success') else RichText("fail", color='FF0000', size=28)
#     result = True if channel_init == 'success' else False
#     if not result:
#         print("行为日志：",ed)
#     assert result
#     extras.channel = channel

# @pytest.mark.parametrize('channel', get_channel())
# def test_login(channel):
#     '''执行登录测试'''
#     print(f'\n开始测试渠道:{channel}的登录功能')
#     ed = getDataByChannel(channel)
#     print('登录:', "success" if has_field(ed, 'login') else "fail")
#     channel = match_field(str(ed), 'channel')
#     login = "success" if has_field(ed, 'login') else RichText("fail", color='FF0000', size=28)
#     result = True if login == 'success' else False
#     if not result:
#         print("行为日志：",ed)
#     assert result
#     extras.channel = channel
#
#
#
#
# @pytest.mark.parametrize('channel', get_channel())
# def test_enterserver(channel):
#     '''执行进服测试'''
#     print(f'\n开始测试渠道:{channel}的进服功能')
#     ed = getDataByChannel(channel)
#     print('进服:', "success" if has_field(ed, 'enter_server') else "fail")
#     enter_server = "success" if has_field(ed, 'enter_server') else RichText("fail", color='FF0000', size=28)
#     # payment = "success" if has_field(ed, 'payment') and ed['payment']['pay_status'] == 'success' else RichText(
#     #     "fail", color='FF0000', size=28)
#     result = True if enter_server == 'success' else False
#     if not result:
#         print("行为日志：",ed)
#     assert result
#     extras.channel = channel
#
#
#
# @pytest.mark.parametrize('channel', get_channel())
# def test_pay(channel):
#     '''执行支付测试'''
#     print(f'\n开始测试渠道:{channel}的支付功能')
#
#     ed = getDataByChannel(channel)
#     print('支付:', "success" if has_field(ed, 'payment') and ed['payment']['pay_status'] == 'success' else "fail")
#     print('渠道：', match_field(str(ed), 'channel'))
#     print('游戏id:', match_field(str(ed), 'gameid'))
#     print('渠道id:', match_field(str(ed), 'channelid'))
#     print('胡莱uid:', match_field(str(ed), 'uid'))
#     print('支付金额:', ed['payment']['price'] if has_field(ed, 'payment') else None)
#
#     channel = match_field(str(ed), 'channel')
#     payment = "success" if has_field(ed, 'payment') and ed['payment']['pay_status'] == 'success' else RichText(
#         "fail", color='FF0000', size=28)
#     result = True if payment == 'success' else False
#     if not result:
#         print("行为日志：",ed)
#     assert result
#     extras.channel = channel


def has_field(json_obj,field):
    return field in json_obj

def match_field(json_obj,field):
    pattern2 = r"'%s':\s*'(\w+)'" % field
    # print("pattern:",pattern2)
    if field in json_obj:
        # pattern = r'channel:(\w+)'
        match = re.search(pattern2,json_obj)
        if match:
            return match.group(1)
        else:
            return None
    else:
        return None