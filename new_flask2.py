import time
from flask import Flask, request, jsonify
import json
import redis
from xiaohonshu_hao_interface import fetch_posts_detail as xhs_post_deail, fetch_user_posts as xhs_user_posts, fetch_user_info as xhs_user_info
from douyin_hao_interface import fetch_posts_detail as dy_post_detail, fetch_user_posts as dy_user_posts,  fetch_user_info as dy_user_info
# pool = redis.ConnectionPool(host="127.0.0.1", port=6379, db=1, decode_responses=True)
# redis_cli = redis.Redis(connection_pool=pool)
REDIS_CONFIG = {
    'host': 'sh-crs-jgiq8q91.sql.tencentcdb.com',
    'port': 29695,
    'db': 1,
    'decode_responses': True,
    'password': 'zzm282910'
}
pool = redis.ConnectionPool(**REDIS_CONFIG)
redis_cli = redis.Redis(connection_pool=pool)



app = Flask(__name__)
price_map = {
    'get_xhs_user_posts': 150,
    'get_xhs_post_detail': 150,
    'get_xhs_user_info':150,
    'get_douyin_user_posts': 150,
    'get_douyin_post_detail': 150,
    'get_douyin_user_info':150
}

@app.route('/dy/info/user_info', methods=['GET'])
def get_dy_user_info():
    # 在这里编写处理请求的代码
    # 例如，从数据库或其他数据源获取用户信息，并返回相应的数据
    userid = request.args.get('userid')
    # lastCursor = request.args.get('lastCursor', '')
    custom_token = request.args.get('token')
    if redis_cli.hexists(f"user_quota:{custom_token}", "user_id"):  # 如果用户存在
        
        result = redis_cli.hgetall(f"user_quota:{custom_token}")
        quota = int(result["quota"])
        if quota <=0 :
            return {'code': -1, 'msg': 'token:{} 没有额度, 请联系管理员'.format(custom_token)}, 400

        result = dy_user_info(secUid=userid)
        if '失败' not in result.get('info', 'a'):
            fee_each = int(price_map.get('get_douyin_user_info'))
            redis_cli.hincrby(f"user_quota:{custom_token}", "quota", -fee_each)
        return result, 200
    else:
        return {'code': -1, 'msg': 'token:{} 验证失败, 账号异常或不存在请联系管理员'.format(custom_token)}, 400

@app.route('/dy/info/post_detail', methods=['GET'])
def get_dy_post_detail():
    # 在这里编写处理请求的代码
    # 例如，从数据库或其他数据源获取用户信息，并返回相应的数据
    note_id = request.args.get('note_id')
    custom_token = request.args.get('token')
    if redis_cli.hexists(f"user_quota:{custom_token}", "user_id"):  # 如果用户存在

        result = redis_cli.hgetall(f"user_quota:{custom_token}")
        quota = int(result["quota"])
        if quota <=0 :
            return {'code': -1, 'msg': 'token:{} 没有额度, 请联系管理员'.format(custom_token)}, 400

        result = dy_post_detail(note_id)
        if '失败' not in result.get('info', ''):
            fee_each = int(price_map.get('get_douyin_post_detail'))
            redis_cli.hincrby(f"user_quota:{custom_token}", "quota", -fee_each)
        return result, 200
    else:
        return {'code': -1, 'msg': 'token:{} 验证失败, 账号异常或不存在请联系管理员'.format(custom_token)}, 400
        


@app.route('/dy/info/user_posts', methods=['GET'])
def get_dy_user_posts():
    # 在这里编写处理请求的代码
    # 例如，从数据库或其他数据源获取用户信息，并返回相应的数据
    userid = request.args.get('userid')
    lastCursor = request.args.get('lastCursor', 0)
    custom_token = request.args.get('token')
    if redis_cli.hexists(f"user_quota:{custom_token}", "user_id"):  # 如果用户存在

        result = redis_cli.hgetall(f"user_quota:{custom_token}")
        quota = int(result["quota"])
        if quota <=0 :
            return {'code': -1, 'msg': 'token:{} 没有额度, 请联系管理员'.format(custom_token)}, 400

        result = dy_user_posts(secUid=userid, lastCursor=lastCursor)
        if '失败' not in result.get('info', ''):
            fee_each = int(price_map.get('get_douyin_user_posts'))
            redis_cli.hincrby(f"user_quota:{custom_token}", "quota", -fee_each)
        return result, 200
    else:
        return {'code': -1, 'msg': 'token:{} 验证失败, 账号异常或不存在请联系管理员'.format(custom_token)}, 400
        
     


@app.route('/xhs/info/user_info', methods=['GET'])
def get_xhs_user_info():
    # 在这里编写处理请求的代码
    # 例如，从数据库或其他数据源获取用户信息，并返回相应的数据
    userid = request.args.get('userid')
    # lastCursor = request.args.get('lastCursor', '')
    custom_token = request.args.get('token')
    if redis_cli.hexists(f"user_quota:{custom_token}", "user_id"):  # 如果用户存在
        
        result = redis_cli.hgetall(f"user_quota:{custom_token}")
        quota = int(result["quota"])
        if quota <=0 :
            return {'code': -1, 'msg': 'token:{} 没有额度, 请联系管理员'.format(custom_token)}, 400

        result = xhs_user_info(userid=userid)
        if '失败' not in result.get('info', ''):
            fee_each = int(price_map.get('get_xhs_user_info'))
            redis_cli.hincrby(f"user_quota:{custom_token}", "quota", -fee_each)
        return result, 200
    else:
        return {'code': -1, 'msg': 'token:{} 验证失败, 账号异常或不存在请联系管理员'.format(custom_token)}, 400
        


@app.route('/xhs/info/post_detail', methods=['GET'])
def get_xhs_post_detail():
    # 在这里编写处理请求的代码
    # 例如，从数据库或其他数据源获取用户信息，并返回相应的数据
    note_id = request.args.get('note_id')
    custom_token = request.args.get('token')
    if redis_cli.hexists(f"user_quota:{custom_token}", "user_id"):  # 如果用户存在

        result = redis_cli.hgetall(f"user_quota:{custom_token}")
        quota = int(result["quota"])
        if quota <=0 :
            return {'code': -1, 'msg': 'token:{} 没有额度, 请联系管理员'.format(custom_token)}, 400

        result = xhs_post_deail(note_id)
        if '失败' not in result.get('info', ''):
            fee_each = int(price_map.get('get_xhs_post_detail'))
            redis_cli.hincrby(f"user_quota:{custom_token}", "quota", -fee_each)
        return result, 200
    else:
        return {'code': -1, 'msg': 'token:{} 验证失败, 账号异常或不存在请联系管理员'.format(custom_token)}, 400
        


@app.route('/xhs/info/user_posts', methods=['GET'])
def get_xhs_user_posts():
    # 在这里编写处理请求的代码
    # 例如，从数据库或其他数据源获取用户信息，并返回相应的数据
    userid = request.args.get('userid')
    lastCursor = request.args.get('lastCursor', '')
    custom_token = request.args.get('token')
    if redis_cli.hexists(f"user_quota:{custom_token}", "user_id"):  # 如果用户存在

        result = redis_cli.hgetall(f"user_quota:{custom_token}")
        quota = int(result["quota"])
        if quota <=0 :
            return {'code': -1, 'msg': 'token:{} 没有额度, 请联系管理员'.format(custom_token)}, 400

        result = xhs_user_posts(userid=userid, lastCursor=lastCursor)
        if '失败' not in result.get('info', ''):
            fee_each = int(price_map.get('get_xhs_user_posts'))
            redis_cli.hincrby(f"user_quota:{custom_token}", "quota", -fee_each)
        return result, 200
    else:
        return {'code': -1, 'msg': 'token:{} 验证失败, 账号异常或不存在请联系管理员'.format(custom_token)}, 400
        


@app.route('/check_balance', methods=['GET'])
def check_balance():
    # 在这里编写处理请求的代码
    # 例如，从数据库或其他数据源获取用户信息，并返回相应的数据

    custom_token = request.args.get('token')
    if redis_cli.hexists(f"user_quota:{custom_token}", "user_token"):  # 如果用户存在
        result = redis_cli.hgetall(f"user_quota:{custom_token}")
        user_id = result["user_id"]
        quota = int(result["quota"])
        result = {'user_name': user_id, 'balance': quota/10000}
        return result, 200
    else:
        return {'code': -1, 'msg': 'token:{} 验证失败, 账号异常或不存在请联系管理员'.format(custom_token)}, 400
    



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
#  =RequestData("叫我柏文")
#   nohup  python3  flask_interface.py   >/dev/null 2>error.log  2>&1


# http://124.223.33.177:5000/get_user_info2?name=%E7%8C%AA%E7%8C%AA


# nohup  /usr/bin/python3 -m gunicorn -c config.py flask_interface:app  >/dev/null 2>error.log  2>&1
# 自动检测代码变化
# nohup /usr/bin/python3 -m gunicorn --reload -c config.py flask_interface:app >/dev/null 2>error.log 2>&1 & 


#pkill -f gunicorn   296.1575 296.1445
# lsof -i:5000


# 检查链接数 netstat -an | grep CLOSE_WAIT | wc -l
# ulimit -n 65535 过增加文件描述符的上限
