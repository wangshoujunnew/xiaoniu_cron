import datetime
import time

from flask import Blueprint
from threading import current_thread
# 构造蓝图
helloworld1 = Blueprint('hello_world', __name__) # helloword1 不能和下面的helloword函数名字一样

@helloworld1.route('/hello_world', methods=["GET","POST"])
def helloworld():
    print("hello world ... >>>>>>>>>>>>>>>>>")
    # 需要返回一个有效的response
    return "success"

@helloworld1.route("/testThread")
def test_thread():
    # 测试同一个url的请求, 两个用户访问是否会阻塞执行
    info = """
    @index at: {}, 
    threadName: {}
    hello wrold
    """.format(str(datetime.datetime.now()), current_thread().getName())
    time.sleep(10)
    out = info + " end:  " + str(datetime.datetime.now())
    print(out)
    return out

