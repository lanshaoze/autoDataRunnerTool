from docxtpl import DocxTemplate, RichText
from datetime import datetime
import re
import test_run
def build_docx(data):
    docx_path = 'docx/temple.docx'
    tpl = DocxTemplate(docx_path)
    context = {}
    context = deal_context(data,context)
    tpl.render(context)
    tpl.save('docx/{}测试报告.docx'.format(get_current_time()))


def get_current_time():
    return datetime.now().strftime("%Y-%m-%d")

def deal_context(data,context):
    content_list = []
    success_list = []
    fail_list = []
    bi_table = []
    for key,ed in data.items():
        # print(f"Key: {key}, Value: {ed}")
        # for ed in value:
        print('初始化:', "success" if has_field(ed, 'channel_init_success') else "fail")
        print('登录:', "success" if has_field(ed, 'login') else "fail")
        print('进服:', "success" if has_field(ed, 'enter_server') else "fail")
        print('支付:', "success" if has_field(ed, 'payment') and ed['payment']['pay_status'] == 'success' else "fail")

        channel = match_field(str(ed), 'channel')
        gameid = match_field(str(ed), 'gameid')
        channelid = match_field(str(ed), 'channelid')
        uid = match_field(str(ed), 'uid')
        price = "{}{}".format(round(ed['payment']['price'] / 1000, 1), ed['payment']['currency']) if has_field(ed,'payment') else None
        print('渠道：', channel)
        print('游戏id:', gameid)
        print('渠道id:', channelid)
        print('胡莱uid:', uid)
        print('支付金额:',price)
        # channel = match_field(str(ed), 'channel')
        channel_init = "success" if has_field(ed, 'channel_init_success') else RichText("fail", color='FF0000', size=28)
        login = "success" if has_field(ed, 'login') else RichText("fail", color='FF0000', size=28)
        enter_server = "success" if has_field(ed, 'enter_server') else RichText("fail", color='FF0000', size=28)
        payment = "success" if has_field(ed, 'payment') and ed['payment']['pay_status'] == 'success' else RichText(
            "fail", color='FF0000', size=28)
        result = '通过' if channel_init == 'success' and login == 'success' and enter_server == 'success' and payment == 'success' else RichText(
            "不通过", color='FF0000', size=28)
        temp = {
            'channel': channel,
            'channel_init': channel_init,
            'login': login,
            'enter_server': enter_server,
            'payment': payment,
            'result': result
        }
        content_list.append(temp)
        if result == '通过':
            success_list.append(ed)
        else:
            fail_list.append(ed)

        bi_data = {
            'channel':channel,
            'gameid':gameid,
            'channelid':channelid,
            'uid':uid,
            'price':price
        }

        bi_table.append(bi_data)

    result = {
        'total_count':len(data),
        'success_count':len(success_list),
        'fail_count':len(fail_list)
    }

    context['result_table'] = content_list
    context['result'] = result
    context['bi_table'] = bi_table

    return context

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