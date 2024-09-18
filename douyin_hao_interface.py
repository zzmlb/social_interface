
from datetime import datetime
import requests
import time

def timestamp_to_datetime(timestamp):
    # 使用 datetime.utcfromtimestamp 将时间戳转换为 UTC 时间
    utc_datetime = datetime.utcfromtimestamp(timestamp)

    # 使用 strftime 格式化时间
    formatted_datetime = utc_datetime.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_datetime

def fetch_posts_detail(noteId):
    for i in range(1):
        token = "HzqX4EA3"
        # noteId = '6474bd660000000013001b6e'
        url = "http://52.83.102.195:8008/api/douyin/get-video-detail/v2?token={}&videoId={}"
        # url = "http://52.83.102.195:8008/api/xiaohongshu/get-note-detail/v2?token={}&noteId={}"

        url = url.format(token, noteId)
        print(url)
        payload = {}
        headers = {"User-Agent": "Apifox/1.0.0 (https://apifox.com)"}

        response = requests.request("GET", url, headers=headers, data=payload)
        code = response.json()["code"]
        if code == 301:
            print("重试", response.status_code, response.text)
            continue
        if  not response.json()["data"].get('aweme_detail', ''):
            print("---视频不存在")
            fail_record = {
                'notExit':1,
                'info': '帖子不存在',
                'noteid': noteId
            }
            return fail_record

        # print(response.json())
        note_info = response.json()["data"]['aweme_detail']
        title = note_info["item_title"]
        desc = note_info["preview_title"]
        time = note_info["create_time"]
        name = note_info["author"]["nickname"]
        userid = note_info["author"]["sec_uid"]
        nickname = note_info["author"]["nickname"]
        # red_id = note_info["user"]["red_id"]
        user_image = note_info["author"]["avatar_larger"]['url_list'][0]

        liked_count = note_info["statistics"]["digg_count"]
        collected_count = note_info["statistics"]["collect_count"]
        comments_count = note_info["statistics"]["comment_count"]
        shared_count = note_info["statistics"]["share_count"]

        duration = int(note_info['duration'])/1000
        # video_url = note_info['video']['play_addr']['url_list'][3]

        record = {}
        images = note_info['video']['cover']['url_list'][0]
        media_type = note_info['media_type']
        print("----当前的类型是", media_type)
        leixing = 'video'
        if media_type == 2:
            leixing = 'image'
        if leixing == 'video':        
            video_url = note_info['video']['play_addr']['url_list'][3]
        else:
            video_url = ''
            images =  ','.join([each['url_list'][-1] for each in note_info['images']])

        # hash_tag = [each["name"] for each in note_info["hash_tag"]]
        record["帖子id"] = noteId
        record["标题"] = title
        record["内容"] = desc
        record["用户名称"] = name
        record["用户nickname"] = nickname
        record["用户id"] = userid
        record["用户头像"] = user_image
        record["发布时间"] = timestamp_to_datetime(time)
        record["点赞数"] = liked_count
        record["分享数"] = shared_count
        record["收藏数"] = collected_count
        record["评论数"] = comments_count
        record["标签"] = ""
        record["链接"] = 'https://www.douyin.com/video/{}'.format(noteId)
        record["图片链接"] = images
        record["视频时长"] = duration
        record["视频链接"] = video_url
        record["帖子类型"] = leixing
        # print(record)
        return record
    fail_record = {
        'info': '请求失败, 请重试！！',
        'noteId': noteId,
    }
    return fail_record


def fetch_user_info(secUid):
    for i in range(1):
        token = "HzqX4EA3"
        url = "http://52.83.102.195:8008/api/douyin/get-user-detail/v3?token={}&secUid={}"
        url = url.format(token, secUid)
        print(url)

        payload = {}
        headers = {"User-Agent": "Apifox/1.0.0 (https://apifox.com)"}

        response = requests.request("GET", url, headers=headers, data=payload)
         
        # print(response.json())
        code = response.json()["code"]
        if code == 301:
            print("重试", response.status_code, response.text)
            continue
                
        userinfo = response.json()["data"]["user"]
        # collected = userinfo['collected']
        nickname = userinfo["nickname"]
        fans = userinfo["follower_count"]
        ip_location = userinfo.get("ip_location",'')
        location = ''
        post_count = userinfo["aweme_count"]
        desc = userinfo["signature"]
        userid = userinfo["sec_uid"]
        imageb = userinfo['avatar_larger']['url_list'][0]
        # red_id =  userinfo['unique_id']
        red_id = userinfo['unique_id'] if userinfo['unique_id'] else  userinfo['short_id']
        record = {}

        record["nickname"] = nickname
        record["userid"] = userid
        record["fans"] = fans
        record["ip_location"] = ip_location
        record["location"] = location
        record["post_count"] = post_count
        record["desc"] = desc
        record["image"] = imageb
        record["account_id"] = red_id
        # print(record)
        return record

    fail_record = {
        'info': '请求失败, 请重试！！',
        'userid': secUid,
    }
    return fail_record
             

def fetch_user_posts(secUid, lastCursor=0):
    for i in range(1):
        lastCursor = lastCursor
        token = "HzqX4EA3"
        url = "http://52.83.102.195:8008/api/douyin/get-user-video-list/v3?token={}&secUid={}&maxCursor={}".format(
            token, secUid, lastCursor
        )

        print(url)
        

        payload = {}
        headers = {"User-Agent": "Apifox/1.0.0 (https://apifox.com)"}

        response = requests.request("GET", url, headers=headers, data=payload)
         
        # print(response.json())
        code = response.json()["code"]
        if code == 301:
            print("重试", response.status_code, response.text)
            continue
        result_info = {'posts':[] }
        if response.json()["data"]["aweme_list"]:
            result_info = {'posts':[] }
            cursor = response.json()["data"]['max_cursor']
            for each in response.json()["data"]["aweme_list"]:
                # print(each)
                id = each["aweme_id"]
                desc = each['desc']
                title = ''
                likes = each["statistics"]['digg_count']
                nickname = each["author"][ "nickname"]
                sec_uid = each["author"][ "sec_uid"]
                record = {}
                record["title"] = title
                record["desc"] = desc
                record["likes"] = likes
                record["post_url"] = 'https://www.douyin.com/video/{}'.format(id)
                record["sec_uid"] = sec_uid
                result_info['posts'].append(record)
                result_info['nickname'] = nickname
                result_info['cursor'] = cursor
                # print(record)
        elif code == 0: # 说明正常完结
            result_info['nickname'] = secUid
        return result_info
    fail_record = {
        'info': '请求失败, 请重试！！',
        'userid': secUid,
    }
    return fail_record
               



if __name__ == "__main__":
    noteId = '7392389007788821811' 
    result = fetch_posts_detail(noteId)
    print(result)

    # userid = 'MS4wLjABAAAA3027ug_pyVjr506anZuqUGXwWegS4Ct2A1jDOYai6wpTUSlio3V8H1A_woUPL95a' 
    # lastCursor = 0
    # result = fetch_user_posts(userid, lastCursor)
    # print(result)

    # userid = 'MS4wLjABAAAA3027ug_pyVjr506anZuqUGXwWegS4Ct2A1jDOYai6wpTUSlio3V8H1A_woUPL95a' 
    # result = fetch_user_info(userid)
    # print(result)

