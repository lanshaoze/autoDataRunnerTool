# 一、修改测试报告标题
from time import strftime
import tabulate
# import base64
# import io
# import pyautogui
# import pyautogui as pyautogui
import pytest
from py._xmlgen import html

from pytest_html import extras

from Singleton import Singleton


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

    prefix.extend([html.h2("测试结果")])
    Singleton().clearBiData()


# @pytest.mark.optionalhook
# def pytest_html_results_summary(prefix, summary, postfix):
#     summary.append(f'{prefix}报告生成时间:{strftime("%Y-%m-%d %H:%M:%S")}{postfix}')

# 三、修改Results部分的信息，并自动截取错误截图
def pytest_html_results_table_header(cells):
    cells.insert(1, html.th('Channel'))
    # cells.insert(2, html.th('Description'))
    cells.insert(2, html.th('TaskCompleteTime'))
    cells.pop(-1)


def pytest_html_results_table_row(report, cells):
    cells.insert(1, html.td(report.Channel))
    # cells.insert(2, html.td(report.Description))
    cells.insert(2, html.td(report.TaskCompleteTime))
    cells.pop(-1)


channels = Singleton().getConfig().keys()

# # 准备要添加到HTML报告中的数据
# data1 = [
#     ["Name", "Age", "City"],
#     ["Alice", 25, "New York"],
#     ["Bob", 30, "London"],
#     ["Charlie", 35, "Paris"]
# ]
#
# # 将数据格式化为HTML表格
# table_html = tabulate.tabulate(data1, headers="firstrow", tablefmt="html", numalign="center", stralign="center")
#
#
# # 自定义HTML报告
# @pytest.mark.optionalhook
# def pytest_html_results_table_html(report, data):
#     # 在报告底部添加额外的HTML表格
#     data.append(f"<h2>检测结果</h2>{table_html}")

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


