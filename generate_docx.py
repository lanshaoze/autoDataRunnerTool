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
    time_table = {}
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
        price = ed['payment']['price'] if has_field(ed,'payment') else None
        currency = ed['payment']['currency'] if has_field(ed, 'payment') else None
        orderid = ed['create_order']['orderId'] if has_field(ed, 'create_order') else None

        for key, item in ed.items():
            time = item['time'] if has_field(item, 'time') else ""
            time_table[key] = time
        # channel_init_time = ed['channel_init_success']['time'] if has_field(ed,'payment') else ""


        print('渠道：', channel)
        print('游戏id:', gameid)
        print('渠道id:', channelid)
        print('胡莱uid:', uid)
        print('支付金额:',price)
        print('金额类型：',currency)
        print('订单Id:', orderid)
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
            'result': result,
            'channel_init_time':time_table['channel_init_success'] if 'channel_init_success' in time_table else '',
            'login_time': time_table['login'] if 'login' in time_table else '',
            'enter_server_time': time_table['enter_server'] if 'enter_server' in time_table else '',
            'payment_time': time_table['payment']if 'payment' in time_table else '',
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
            'price':price,
            'currency':currency,
            'orderid':orderid
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