from datetime import datetime
import requests
import time


def timestamp_to_datetime(timestamp):
    # 使用 datetime.utcfromtimestamp 将时间戳转换为 UTC 时间
    utc_datetime = datetime.utcfromtimestamp(timestamp)

    # 使用 strftime 格式化时间
    formatted_datetime = utc_datetime.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_datetime


def fetch_videos(post_id):
    for i in range(3):
        token = 'wuic-qackd-fga-z17770'
        url = 'https://proxy.layzz.cn/lyz/getAnalyse?token={}&link=https://www.xiaohongshu.com/explore/{}'
        response = requests.get(url.format(token, post_id))
        info = response.json()
        if info['message'] == '操作成功':
            playAddr = info['data']['playAddr']
            cover = info['data']['cover']
            return [playAddr, cover]
        time.sleep(1)
    return  None 

def fetch_posts_detail(noteId):
    for i in range(1):
        token = "HzqX4EA3"
        # noteId = '6474bd660000000013001b6e'
        url = "http://52.83.102.195:8008/api/xiaohongshu/get-note-detail/v2?token={}&noteId={}"

        url = url.format(token, noteId)
        # print(url)
        payload = {}
        headers = {"User-Agent": "Apifox/1.0.0 (https://apifox.com)"}

        response = requests.request("GET", url, headers=headers, data=payload)
        code = response.json()["code"]
        if code == 301:
            print("重试", response.status_code, response.text)
            continue
        if  not response.json()["data"]:
            print("---视频不存在")
            fail_record = {
                'notExit':1,
                'info': '帖子不存在',
                'noteid': noteId
            }
            return fail_record
                    


        print(response.json())
        if 'v1'in url:
            note_info = response.json()["data"]["data"][0]["note_list"][0]
        else:
            note_info = response.json()["data"][0]["note_list"][0]
        title = note_info["title"]
        desc = note_info["desc"]
        time = note_info["time"]
        name = note_info["user"]["name"]
        userid = note_info["user"]["id"]
        liked_count = note_info["liked_count"]
        note_type = note_info['type']
        collected_count = note_info["collected_count"]
        comments_count = note_info["comments_count"]
        shared_count = note_info["shared_count"]
        video_info = note_info.get('video', {})
        # duration = video_info.get('duration', '')
        duration = video_info.get('media', {}).get('video', {}).get('duration', '')

        video_url = video_info.get('url', '')
        image_lists = [each["url"] for each in note_info["images_list"]]

        if note_type == 'video':
            videos_info = fetch_videos(noteId)
            if videos_info:
                playAddr, cover = videos_info
                image_lists = [cover]
                video_url = playAddr
            else:
                fail_record = {
                    'info': '请求失败, 请重试！！',
                    'noteid': noteId
                }
                return fail_record


        record = {}
        
        hash_tag = [each["name"] for each in note_info["hash_tag"]]
        record["帖子id"] = noteId
        record["标题"] = title
        record["内容"] = desc
        record["用户名称"] = name
        record["用户id"] = userid
        record["发布时间"] = timestamp_to_datetime(time)
        record["点赞数"] = liked_count
        record["分享数"] = shared_count
        record["收藏数"] = collected_count
        record["评论数"] = comments_count
        record["标签"] = ", ".join(hash_tag)
        record["链接"] = "https://www.xiaohongshu.com/explore/{}".format(noteId)
        record["图片链接"] = ",".join(image_lists)
        record["视频时长"] = duration
        record["视频链接"] = video_url
        record["帖子类型"] = note_type
        # print(record)
        return record
    fail_record = {
        'info': '请求失败, 请重试！！',
        'noteid': noteId
    }
    return fail_record


def fetch_user_posts(userid, lastCursor=""):
    for i in range(1):
        lastCursor = lastCursor
        token = "HzqX4EA3"
        url = "http://52.83.102.195:8008/api/xiaohongshu/get-user-note-list/v2?token={}&userId={}&lastCursor={}".format(
            token, userid, lastCursor
        )
        # print(url)

        payload = {}
        headers = {"User-Agent": "Apifox/1.0.0 (https://apifox.com)"}

        response = requests.request("GET", url, headers=headers, data=payload)

        code = response.json()["code"]
        if code == 301:
            print("重试", response.status_code, response.text)
            continue
        result_info = {'posts':[] }
        if response.json()["data"]["notes"]:
            cursor = ""
            for each in response.json()["data"]["notes"]:
                if 'v1' in url:
                    cursor = each["cursor"]
                    id = each["id"]
                    title = each["title"]
                    desc = each["desc"]
                    likes = each["likes"]
                    nickname = each["user"]["nickname"]
                    record = {}
                    record["title"] = title
                    record["desc"] = desc
                    record["likes"] = likes
                    record["post_url"] = "https://www.xiaohongshu.com/explore/{}".format(id)
                    result_info['posts'].append(record)
                    result_info['nickname'] = nickname
                    result_info['cursor'] = cursor
                if 'v2' in url:
                    id = each["id"]
                    cursor = id
                    desc = ''
                    title = each["display_title"]
                    likes = each["likesc"]
                    nickname = each["user"]["nickname"]
                    record = {}
                    record["title"] = title
                    record["desc"] = desc
                    record["likes"] = likes
                    record["post_url"] = "https://www.xiaohongshu.com/explore/{}".format(id)
                    result_info['posts'].append(record)
                    result_info['nickname'] = nickname
                    result_info['cursor'] = cursor

                print(record)
        elif code == 0: # 说明正常完结
            result_info['nickname'] = userid
        return result_info
    fail_record = {
        'info': '请求失败, 请重试！！',
        'userid': userid,
        'lastCursor': lastCursor
    
    }
    return fail_record
               

def fetch_user_info(userid):
    for i in range(1):
        token = "HzqX4EA3"
        url = "http://52.83.102.195:8008/api/xiaohongshu/get-user/v3?token={}&userId={}"
        url = url.format(token, userid)
        print(url)

        payload = {}
        headers = {"User-Agent": "Apifox/1.0.0 (https://apifox.com)"}

        response = requests.request("GET", url, headers=headers, data=payload)
         
        code = response.json()["code"]
        if code == 301:
            print("重试", response.status_code, response.text)
            continue
                      
        if 'v2' in url:
            userinfo = response.json()["data"]
            nickname = userinfo["nickname"]
            fans = userinfo["fans"]
            ip_location = userinfo["ip_location"]
            location = userinfo["location"]
            post_count = userinfo["ndiscovery"]
            desc = userinfo["desc"]
            userid = userinfo["userid"]
            imageb = userinfo['imageb']
            red_id = userinfo['red_id']
        else:
            userinfo = response.json()["data"]['basic_info']
            nickname = userinfo['nickname']
            extra_info = {}
            for each in  response.json()["data"]['interactions']:
                extra_info[each['type']] = each['count']
            fans = extra_info.get('fans')
            ip_location = userinfo['ip_location']
            location = ''
            post_count = ''
            desc = userinfo['desc']
            imageb = userinfo['images']
            red_id = userinfo['red_id']
        record = {}

        record["nickname"] = nickname
        record["userid"] = userid
        record["fans"] = fans
        record["ip_location"] = ip_location
        record["location"] = location
        record["post_count"] = post_count
        record["desc"] = desc
        record["image"] = imageb
        record["red_id"] = red_id
        # print(record)
        return record

    fail_record = {
        'info': '请求失败, 请重试！！',
        'userid': userid,
    }
    return fail_record
               



if __name__ == "__main__":
    noteId = '64c2555e888080808800d25c'
    result = fetch_posts_detail(noteId)
    print(result)

    # userid = '631614a4000000000f005eb8'
    # lastCursor = ""
    # result = fetch_user_posts(userid, lastCursor)
    # print(result)

    # userid = '66c30ff7000000001d01b0b6'
    # result = fetch_user_info(userid)
    # print(result)


    