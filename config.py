# -*- coding: utf-8 -*-
debug = True
# 访问地址
bind = "0.0.0.0:5000"
# 工作进程数
workers = 2
# 工作线程数
threads = 2
# 超时时间
timeout = 600
# 输出日志级别
loglevel = 'debug'
# 存放日志路径
pidfile = "log/gunicorn.pid"
# 存放日志路径
accesslog = "log/access.log"
# 存放日志路径
errorlog = "log/debug.log"
# gunicorn + apscheduler场景下，解决多worker运行定时任务重复执行的问题
preload_app = True
# 超时时间，单位为秒
timeout = 30  # 请求处理超时
# keep-alive 超时
keepalive = 10  # 保持连接的时间，单位为秒
# 是否自动重载代码（开发环境下使用）
reload = True  # 每次代码变更后自动重启（适合开发时）
