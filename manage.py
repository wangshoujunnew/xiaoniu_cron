#!/usr/bin/env python
#coding:utf-8
import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell, Server

from gevent import monkey
from gevent.pywsgi import WSGIServer
monkey.patch_all() # 多线程处理同一个url的请求

"""Manager: @manager.command 在终端使用命令来操作程序进程 
（1）Flask Script扩展提供向Flask插入外部脚本的功能，包括运行一个开发用的服务器，一个定制的Python shell，设置数据库的脚本，cronjobs，及其他运行在web应用之外的命令行任务；使得脚本和系统分开；

（2）Flask Script和Flask本身的工作方式类似，只需定义和添加从命令行中被Manager实例调用的命令；

（3）flask_script的作用是可以通过命令行的形式来操作flask例如通过一个命令跑一个开发版本的服务器，设置数据库，定时任务等

（4）通过使用Flask-Script扩展，我们可以在Flask服务器启动的时候，通过命令行的方式传入参数。而不仅仅通过app.run()方法中传参，比如我们可以通过python hello.py runserver --host ip地址，告诉服务器在哪个网络接口监听来自客户端的连接。默认情况下，服务器只监听来自服务器所在计算机发起的连接，即localhost连接。
"""

from app import create_app, db
from configs import configs
from datas.model.cron_infos import CronInfos

from datas.model.job_log import JobLog
from mycron.test_cron import *

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
# ========================= 引入其他url模块
# 注册蓝图
app.register_blueprint(blueprint=helloworld1, url_prefix="/test_cron")
# =========================== end

manager = Manager(app)

migrate = Migrate(app, db)

def make_shell_context():
    return dict(
        app=app,
        JobLog=JobLog,
        CronInfos=CronInfos
    )

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
manager.add_command("runserver", Server("10.2.3.100", port=10080, threaded=True, use_debugger=False))
# manager 启动服务
# manager.add_command("runserver", Server("localhost", port=8080))

@manager.command
def test():
    """
    使用场景：创建一些敏感数据（如后台管理员），批量添加测试数据等等
    终端中操作指令 ： python 文件名 方法名
    :return:
    """
    print("Hello world")
    d = configs('job_log_counts')
    print(d)
    pass

if __name__ == '__main__':
    #gunicorn -b 127.0.0.1:5000 -w 1 -k gevent manage:app
    manager.run()
    # 浏览器的问题, 浏览器会将相同的url进行阻塞执行, 生产环境使用WSGIServer部署
    # http_server = WSGIServer(("10.2.3.100", 10080), app)
    # http_server.serve_forever()
