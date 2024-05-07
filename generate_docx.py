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
    tpl.save('docx/{}.docx'.format(get_current_time()))


def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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

        #{"adChannel":"hoolai","balance":"0","baseEvent":false,"currency":"CNY","extendAction":"payment",
        # "gameData":{"productId":"1","orderId":"AD7F3054BEEE40E7ADF25D2509C1EE1D","roleId":"1235761",
        # "goodsId":"1","adChannel":"hoolai","gameInfo":"callbackInfo","serverName":"大唐战机","gps_adid":"",
        # "payState":"success","serverId":"100","userId":"3000236226","package_belong":"12345678","uid":"3000236226",
        # "payType":"weixin","price":"1","roleName":"昵称2","zoneId":"100","currency":"CNY","zoneName":"华东大区","roleLevel":"11",
        # "udid":"SH5K3UG867C4ZPPE","goodsName":"钻石","channelId":"1"},"itemId":"1","itemName":"钻石","orderId":"AD7F3054BEEE40E7ADF25D2509C1EE1D",
        # "partName":"无帮派","price":"1","result":true,"roleId":"0","roleLevel":"1","roleName":"无","serverId":"0","serverName":"国服","userId":"3000236226","vip":"1","zoneId":"0","zoneName":"1区"}
        print('支付:', "success" if has_field(ed, 'payment') and ed['payment']['result'] else "fail")

        channel = match_field(str(ed), 'adChannel')
        gameid = match_field(str(ed), 'productId')
        channelid = match_field(str(ed), 'channelId')
        uid = match_field(str(ed), 'uid')
        price = ed['payment']['gameData']['price'] if has_field(ed,'payment') else None
        currency = ed['payment']['gameData']['currency'] if has_field(ed, 'payment') else None
        orderid = ed['payment']['gameData']['orderId'] if has_field(ed, 'payment') else None

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
        payment = "success" if has_field(ed, 'payment') and ed['payment']['result'] else RichText(
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