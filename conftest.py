# 一、修改测试报告标题
from time import strftime
import tabulate
# import base64
# import io
# import pyautogui
# import pyautogui as pyautogui
import pytest
from py._xmlgen import html
import plotly.graph_objs as go

from pytest_html import extras

from Singleton import Singleton

# 存储测试结果数据
test_results = {
    'total': 0,
    'passed': 0,
    'failed': 0,
    'skipped': 0,
    'error': 0
}
@pytest.mark.optionalhook
def pytest_metadata(metadata):
    metadata.pop("Python", None)
    metadata.pop("Platform", None)
    metadata.pop("Packages", None)
    metadata.pop("Plugins", None)
    metadata.pop("JAVA_HOME", None)


@pytest.hookimpl(optionalhook=True)
def pytest_html_report_title(report):
    report.title = "自动化测试报告"




# 二、修改Summary部分的信息
@pytest.mark.parametrize
def pytest_html_results_summary(prefix, summary, postfix):
    prefix.extend([html.p("所属部门：平台支持中心")])
    prefix.extend([html.p("技术人员：芦杰")])
    prefix.extend([html.p("报告生成时间：{}".format(strftime("%Y-%m-%d %H:%M:%S")))])

    prefix.extend([html.h2("通过率占比")])
    # 准备数据
    labels = ['Passed', 'Failed', 'Skipped', 'Error']
    values = [test_results['passed'], test_results['failed'], test_results['skipped'], test_results['error']]

    # print("valuees==>{}".format(values))

    # colors = ['green', 'red', '#99FF99','#FF9999']    ,marker=dict(colors=colors)

    # 创建饼图
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])

    # 设置布局
    fig.update_layout(
        title='',
        width=500,
        height=400
    )
    # 将图形转换为HTML
    html_str = fig.to_html(full_html=False, include_plotlyjs='cdn')
    prefix.extend([html_str])

    prefix.extend([html.h2("BI相关信息")])

    # 准备数据
    # data = [
    #     ["channel", "gameid", "channelid","uid","price","currency","orderid"],
    #     ["4399",3007,   10138,   "3000476824",   100,   "CNY", "6042FD14062A4C1B9B78D17C8BFB570B"],
    #     ["4399", 3007, 10138, "3000476824", 100, "CNY", "6042FD14062A4C1B9B78D17C8BFB570B"],
    #     ["4399", 3007, 10138, "3000476824", 100, "CNY", "6042FD14062A4C1B9B78D17C8BFB570B"],
    #     ["4399", 3007, 10138, "3000476824", 100, "CNY", "6042FD14062A4C1B9B78D17C8BFB570B"],
    #     ["4399", 3007, 10138, "3000476824", 100, "CNY", "6042FD14062A4C1B9B78D17C8BFB570B"],
    #     ["4399", 3007, 10138, "3000476824", 100, "CNY", "6042FD14062A4C1B9B78D17C8BFB570B"],
    #     ["4399", 3007, 10138, "3000476824", 100, "CNY", "6042FD14062A4C1B9B78D17C8BFB570B"],
    #     ["4399", 3007, 10138, "3000476824", 100, "CNY", "6042FD14062A4C1B9B78D17C8BFB570B"],
    #     ["4399", 3007, 10138, "3000476824", 100, "CNY", "6042FD14062A4C1B9B78D17C8BFB570B"],
    #     ["4399", 3007, 10138, "3000476824", 100, "CNY", "6042FD14062A4C1B9B78D17C8BFB570B"],
    # ]
    data = Singleton().getBiData()
    data[0] = ["channel", "gameid  ", "  channelid  ","  uid  ","price","currency","  orderid  "]

    # 使用tabulate打印居中对齐的表格
    table_html = tabulate.tabulate(data, headers="firstrow", tablefmt="html", numalign="center", stralign="center")
    prefix.extend([table_html])

    # prefix.extend([html.h2("测试结果")])
    Singleton().clearBiData()

    prefix.extend([html.h2("渠道详细信息")])




# @pytest.mark.optionalhook
# def pytest_html_results_summary(prefix, summary, postfix):
#     summary.append(f'{prefix}报告生成时间:{strftime("%Y-%m-%d %H:%M:%S")}{postfix}')

# 三、修改Results部分的信息，并自动截取错误截图
def pytest_html_results_table_header(cells):
    cells.insert(1, html.th('Channel'))
    # cells.insert(2, html.th('Description'))
    cells.insert(2, html.th('TaskCompleteTime'))
    cells.pop(-1)
@pytest.mark.optionalhook
def pytest_sessionfinish(session, exitstatus):
    print("进入了pytest_sessionfinish")


def pytest_html_results_table_row(report, cells):
    cells.insert(1, html.td(report.Channel))
    # cells.insert(2, html.td(report.Description))
    cells.insert(2, html.td(report.TaskCompleteTime))
    cells.pop(-1)
    if report.when == 'call':
        test_results['total'] += 1
        if report.passed:
            test_results['passed'] += 1
        elif report.failed:
            test_results['failed'] += 1
        elif report.skipped:
            test_results['skipped'] += 1
        elif report.outcome == 'error':
            test_results['error'] += 1
        print("====total:{} passed:{} skipped:{}  error:{}".format(test_results['passed'], test_results['failed'], test_results['skipped'], test_results['error']))

channels = Singleton().getConfig().keys()

# 自定义HTML报告
# @pytest.mark.optionalhook
# def pytest_html_results_table_html(report, data):
#     # 获取测试结果数据

def get_channel():
    # 这里可以动态获取渠道
    channels = Singleton().getConfig().keys()
    # print("getreceiver:",channels)
    return channels


def getData():
    return Singleton().getConfig()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_setup(item):
    channel = item.callspec.params['channel']
    item.channel = channel
    yield


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # print("item========>",item)
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    report.Channel = 'None'
    # report.Description = str(item.function.__doc__)
    report.TaskCompleteTime = str(strftime("%Y-%m-%d %H:%M:%S"))
    # print('getChannels:',channels)
    if report.when == 'call' or report.when == 'setup':
        # 在报告中添加标签
        for channel in channels:
            if item.channel == channel:
                report.Channel = channel
                report.user_properties.append(('tag', channel))
    #
    # extra = getattr(report, 'extra', [])
    # if report.when == 'call' or report.when == 'setup':
    #     xfail = hasattr(report, 'wasxfail')
    #     if (report.skipped and xfail) or (report.failed and not xfail):
    #         print('report')
    #         # screenshot = pyautogui.screenshot()
    #         # screenshot_buffer = io.BytesIO()
    #         # screenshot.save(screenshot_buffer, format='PNG')
    #         # screenshot_base64 = base64.b64encode(
    #         #     screenshot_buffer.getvalue()).decode('utf-8')
    #         # html = '<div><img src="data:image/png;base64,{}" alt="screenshot" style="width:500px;height:260px;" ' \
    #         #        'οnclick="window.open(this.src)" align="right"/></div>'.format(screenshot_base64)
    #         # extra.append(pytest_html.extras.html(html))
    #     report.extra = extra


