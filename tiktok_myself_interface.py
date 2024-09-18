import requests
import re 
import json
import random
import time
from datetime import datetime

headers = {
  'authority': 'www.tiktok.com',
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
  'accept-language': 'en,es;q=0.9,zh-CN;q=0.8,zh;q=0.7',
  'cache-control': 'no-cache',
  'cookie': '_ttp=2U9eTQ3nhGps6ZodwEQTJVcw2Zj; tiktok_webapp_theme=light; _ga=GA1.1.906841526.1698745659; _fbp=fb.1.1698745662484.784558763; _tt_enable_cookie=1; passport_csrf_token=5ce84b5b983b832474864624469d21f9; passport_csrf_token_default=5ce84b5b983b832474864624469d21f9; _ga_BZBQ2QHQSP=GS1.1.1700794407.2.1.1700796053.0.0.0; cookie-consent={%22ga%22:true%2C%22af%22:true%2C%22fbp%22:true%2C%22lip%22:true%2C%22bing%22:true%2C%22ttads%22:true%2C%22reddit%22:true%2C%22hubspot%22:true%2C%22version%22:%22v10%22}; lang=en; _ga_LVN0C1THGC=GS1.1.1701660741.1.0.1701660922.0.0.0; _tea_utm_cache_1233={%22utm_source%22:%22copy%22%2C%22utm_medium%22:%22android%22%2C%22utm_campaign%22:%22client_share%22}; tt_csrf_token=Dq0Rx3pP-o34fuMvn_Dg8tN-CJ81tvhM2xPE; odin_tt=fd5ad105836b259f5e49d927e56132a5a329a4456e18ecc0ecb1ff9cd473828dff4794b31155f59c37c6e502dce77147f231035f5ed3fa350b45922070d14aa88b513f79a3c2990b3047c07ed06a873c; s_v_web_id=verify_lpw9n3sn_9NJEj5aj_DLan_4JKy_AQdg_PhWjwfGAfzO2; d_ticket=db8bb089515c6e80972de0b7b89ccb192b43f; multi_sids=7021337342246880258%3A499fd5fb613836adb35b1c9d44b32f00; cmpl_token=AgQQAPO8F-RO0rFOI7s8_V07_xD50G0aP53ZYNNAjQ; passport_auth_status=3c3e3afd772c92cd61cba99d8733af6e%2C; passport_auth_status_ss=3c3e3afd772c92cd61cba99d8733af6e%2C; uid_tt=6d0a0df8d97f6977835c43163fc5bc8528493203b7f5e8ac5a4f27d54d32bd24; uid_tt_ss=6d0a0df8d97f6977835c43163fc5bc8528493203b7f5e8ac5a4f27d54d32bd24; sid_tt=499fd5fb613836adb35b1c9d44b32f00; sessionid=499fd5fb613836adb35b1c9d44b32f00; sessionid_ss=499fd5fb613836adb35b1c9d44b32f00; store-idc=alisg; store-country-code=sg; store-country-code-src=uid; tt-target-idc=alisg; tt-target-idc-sign=ilUVWWdpPKkyog6_eCHvKSzYpFHcY04CXLidfO-CJlKb8ZLYCC9VGnELzGukK3BhOWyuEmCayQD1UPG9dJeJ6tIPIJPvjwUonsRjYSG763GzRoPPYSwdeJ2r0N0dev2EgTq-Uo-ek5HmWg0FOzOzlN722FPMFGkNN7zTWMW09SvobMVs0TDyTm9rxBY_GaQapQJYpVkiQu9IdlbK19RgYrOyawbCsBmVBm8hlRXg_B-ZCQ9hp3kdtuDiMX2Y2CVTAqC3bfXzZ7BACwUGW7_TMRyFBzg6Ms2wUr9WgK5kXeo7Df9A26VZGzBlYOhTzJ_VzM15WnRo_P2kPJAbNMCpYqIWCgb5XIv-v4QWAYOTZdKdPTn26VMeGvxEmy5F0wlZfDs_d0x5KiEvs4pkL4ZicdMR9pifz5Mko0tI_WwMW6yPqqVkjJNfIH86cA_44-rrY6ZQkTEucU8uGH_oSkHfQX1x9AwXIhjZazsliF1ylnSOSgskuki7ZURJvZrvzfyM; sid_guard=499fd5fb613836adb35b1c9d44b32f00%7C1702018179%7C15551992%7CWed%2C+05-Jun-2024+06%3A49%3A31+GMT; sid_ucp_v1=1.0.0-KDZhMDBkNTg0NjYxOGExZWRmMWFiZTI5YWU0NjVhODEyNDVhZmQyZTgKGAiCiL6my6OzuGEQg_nKqwYYsws4AkDxBxADGgJteSIgNDk5ZmQ1ZmI2MTM4MzZhZGIzNWIxYzlkNDRiMzJmMDA; ssid_ucp_v1=1.0.0-KDZhMDBkNTg0NjYxOGExZWRmMWFiZTI5YWU0NjVhODEyNDVhZmQyZTgKGAiCiL6my6OzuGEQg_nKqwYYsws4AkDxBxADGgJteSIgNDk5ZmQ1ZmI2MTM4MzZhZGIzNWIxYzlkNDRiMzJmMDA; perf_feed_cache={%22expireTimestamp%22:1702188000000%2C%22itemIds%22:[%227282929085121105185%22%2C%227285573253320576262%22%2C%227292374289389473026%22]}; tt_chain_token=ByA9oqCWkcXTE+REVFm+rA==; __tea_cache_tokens_1988={%22_type_%22:%22default%22%2C%22user_unique_id%22:%227310112359367001607%22%2C%22timestamp%22:1702018198388}; passport_fe_beating_status=true; ttwid=1%7Cx-CH4utGQNo1cLXjl8eWLfysYireroT2rCKhGZfMDhs%7C1702357507%7C9baf1e771ae3afa40c1d14a487a82d2a21442a86a0a998ab4f43d2e61b3448b5; msToken=8a_cB7Va9nYETlcuOw0oBeQNdV35ez5aSTl9t1ahtxNsg87EVI_U4eCsDy_Zcdrg8jwfltUsfmbMBcZQYWSge57CfZqKGl6QVE3UaWDJuqqccnTAUjLtsinIyk8Oa_drTyJE0OkTsvaaZtTH; msToken=8a_cB7Va9nYETlcuOw0oBeQNdV35ez5aSTl9t1ahtxNsg87EVI_U4eCsDy_Zcdrg8jwfltUsfmbMBcZQYWSge57CfZqKGl6QVE3UaWDJuqqccnTAUjLtsinIyk8Oa_drTyJE0OkTsvaaZtTH; tt_chain_token=HBK1WjQ0mh1SPEW+KGjeJg==',
  'pragma': 'no-cache',
  'sec-ch-ua': '"Google Chrome";v="112", "Chromium";v="112", "Not=A?Brand";v="24"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"macOS"',
  'sec-fetch-dest': 'document',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-site': 'none',
  'sec-fetch-user': '?1',
  'upgrade-insecure-requests': '1',
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 uacq'
}


static_proxys = ['http://dfs:dfs@gz2020@146.71.62.164:3128', 'http://dfs:dfs@gz2020@146.71.62.165:3128', 'http://dfs:dfs@gz2020@146.71.62.166:3128', 'http://dfs:dfs@gz2020@146.71.62.167:3128', 'http://dfs:dfs@gz2020@146.71.62.168:3128', 'http://dfs:dfs@gz2020@146.71.62.169:3128', 'http://dfs:dfs@gz2020@146.71.62.170:3128', 'http://dfs:dfs@gz2020@146.71.62.171:3128', 'http://dfs:dfs@gz2020@146.71.62.172:3128', 'http://dfs:dfs@gz2020@146.71.62.173:3128', 'http://dfs:dfs@gz2020@146.71.62.174:3128', 'http://dfs:dfs@gz2020@146.71.61.210:3128', 'http://dfs:dfs@gz2020@146.71.61.211:3128', 'http://dfs:dfs@gz2020@146.71.61.212:3128', 'http://dfs:dfs@gz2020@146.71.61.213:3128', 'http://dfs:dfs@gz2020@146.71.61.214:3128', 'http://dfs:dfs@gz2020@146.71.61.215:3128', 'http://dfs:dfs@gz2020@146.71.61.216:3128', 'http://dfs:dfs@gz2020@146.71.61.217:3128', 'http://dfs:dfs@gz2020@146.71.61.218:3128', 'http://dfs:dfs@gz2020@146.71.61.219:3128', 'http://dfs:dfs@gz2020@146.71.61.220:3128', 'http://dfs:dfs@gz2020@146.71.61.221:3128', 'http://dfs:dfs@gz2020@146.71.61.222:3128', 'http://dfs:dfs@gz2020@146.71.57.98:3128', 'http://dfs:dfs@gz2020@146.71.57.99:3128', 'http://dfs:dfs@gz2020@146.71.57.100:3128', 'http://dfs:dfs@gz2020@146.71.57.101:3128', 'http://dfs:dfs@gz2020@146.71.57.102:3128', 'http://dfs:dfs@gz2020@146.71.57.103:3128', 'http://dfs:dfs@gz2020@146.71.57.104:3128', 'http://dfs:dfs@gz2020@146.71.57.105:3128', 'http://dfs:dfs@gz2020@146.71.57.106:3128', 'http://dfs:dfs@gz2020@146.71.57.107:3128', 'http://dfs:dfs@gz2020@146.71.57.108:3128', 'http://dfs:dfs@gz2020@146.71.57.109:3128', 'http://dfs:dfs@gz2020@146.71.57.110:3128', 'http://dfs:dfs@gz2020@146.71.56.226:3128', 'http://dfs:dfs@gz2020@146.71.56.227:3128', 'http://dfs:dfs@gz2020@146.71.56.228:3128', 'http://dfs:dfs@gz2020@146.71.56.229:3128', 'http://dfs:dfs@gz2020@146.71.56.230:3128', 'http://dfs:dfs@gz2020@146.71.56.231:3128', 'http://dfs:dfs@gz2020@146.71.56.232:3128', 'http://dfs:dfs@gz2020@146.71.56.233:3128', 'http://dfs:dfs@gz2020@146.71.56.234:3128', 'http://dfs:dfs@gz2020@146.71.56.235:3128', 'http://dfs:dfs@gz2020@146.71.56.236:3128', 'http://dfs:dfs@gz2020@146.71.56.237:3128', 'http://dfs:dfs@gz2020@146.71.56.238:3128']
proxy_ip = random.choice(static_proxys)
proxy_ip = ''
proxy = {"http": proxy_ip, "https": proxy_ip}

def fetch_videos(urk):
    for i in range(5):
        token = 'wuic-qackd-fga-z17770'
        url = 'https://proxy.layzz.cn/lyz/getAnalyse?token={}&link={}'
        response = requests.get(url.format(token, urk))
        info = response.json()
        if info['message'] == '操作成功':
            playAddr = info['data']['playAddr']
            cover = info['data']['cover']
            return [playAddr, cover]
        time.sleep(1)
    return  None 

def timestamp_to_datetime(timestamp):
    # 使用 datetime.utcfromtimestamp 将时间戳转换为 UTC 时间
    utc_datetime = datetime.utcfromtimestamp(timestamp)

    # 使用 strftime 格式化时间
    formatted_datetime = utc_datetime.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_datetime

def parse_post(user_post):
        """
          解析tiktok视频详情
        """
        item = {}
        origin_urls = []
        cover_urls = []
        # print("-----", user_post)
        post_id = user_post["id"]
        post_desc = user_post["desc"]
        post_createtime = user_post["createTime"]
        # print(post_createtime)
        post_at = timestamp_to_datetime(int(post_createtime))
        post_stats = user_post["stats"]
        dig_count = post_stats["diggCount"]
        share_count = post_stats["shareCount"]
        comment_count = post_stats["commentCount"]
        play_count = post_stats["playCount"]
        # video
        video_dict = user_post["video"]
        # video_id = video_dict["id"]
        video_cover_url = video_dict["cover"]
        video_url = video_dict["playAddr"]
        if not video_url:
            video_cover_url = ','.join([each['imageURL']['urlList'][0] for each in user_post['imagePost']['images']])
        origin_urls.append(video_url)
        cover_urls.append(video_cover_url)
        # user
        detail_user = {}
        post_username = user_post["author"]["uniqueId"]
        post_url = 'https://www.tiktok.com/@{}/video/{}'.format(post_username, post_id)
        if video_url:
            videos_info = fetch_videos(post_url)
            if videos_info:
                playAddr, cover = videos_info
                image_lists = [cover]
                video_url = playAddr
            # else:
            #     video_url = 
                # fail_record = {
                #     'info': '请求失败, 请重试！！',
                #     'noteid': post_url
                # }
                # return fail_record




        post_userid = user_post["author"]["id"]
        user_following_count = 0
        user_follower_count = 0
        user_heart_count = 0
        user_video_count = 0
        user_digg_count = 0
        detail_user['usename'] = post_username
        detail_user['userid'] = post_userid
        detail_user['following_count'] = user_following_count
        detail_user['follower_count'] = user_follower_count
        detail_user['heart_count'] = user_heart_count
        detail_user['video_count'] = user_video_count
        detail_user['digg_count'] = user_digg_count
        # music
        detail_music = {}
        music_dict = user_post.get("music")
        if music_dict:
            detail_music["id"] = music_dict.get("id")
            detail_music["title"] = music_dict.get("title")
            detail_music["url"] = music_dict.get("playUrl")
            detail_music['author_name'] = music_dict.get('authorName')
        # hashtag
        detail_hahtags = []
        challenges = user_post.get("challenges")
        if challenges:
            for challenge in challenges:
                hahtag_dict = {}
                hahtag_dict["id"] = challenge.get("id")
                hahtag_dict["title"] = challenge.get("title")
                detail_hahtags.append(hahtag_dict)
        detail = {'desc': post_desc, 'music': detail_music, 'hahtags': detail_hahtags,
                  'createtime': post_createtime, 'user': detail_user, 'origin_urls': origin_urls,
                  'cover_urls': cover_urls}
        item['post_username'] = post_username
        item['post_userid'] = post_userid
        item['post_at'] = post_at
        item['post_id'] = post_id
        item['post_url'] = post_url
        item['video_cover_url'] = video_cover_url
        item['video_url'] = video_url
        item['detail'] = detail
        item['dig_count'] = dig_count
        item['share_count'] = share_count
        item['play_count'] = play_count
        item['comment_count'] = comment_count
        record = {}
        record["帖子id"] = post_id
        record["标题"] = ''
        record["内容"] = post_desc
        record["用户名称"] = post_username
        record["用户nickname"] = post_username
        record["用户id"] = post_userid
        record["用户头像"] = ''
        record["发布时间"] = post_at
        record["点赞数"] = dig_count
        record["分享数"] = share_count
        record["收藏数"] = ''
        record["评论数"] = comment_count
        record["标签"] = ""
        record["链接"] = "https://www.tiktok.com/@{}/video/{}".format(post_username, post_id)
        record["图片链接"] = video_cover_url
        record["视频时长"] = ''
        record["视频链接"] = video_url
        record["帖子类型"] = 'video'
        # print(record)
        return record



def fetch_posts_detail(url):
    # url = "https://www.tiktok.com/@presleymabus_/video/7377112628562365739"
    for i in range(1):
        response = requests.get(url, headers=headers, timeout=10,proxies=proxy )
        if response and response.ok:
            print(response.status_code)
        
            try:
                response = re.search(
                    r"<script id=\"sigi-persisted-data\">window\['SIGI_STATE'\]=(.*?);window\['SIGI_RETRY'\]=(.*?)</script>",
                    response.text).group(1)
                print("-------1")
            except:
                response = re.search('id="__UNIVERSAL_DATA_FOR_REHYDRATION__" type="application/json">(.*?)</script><script', response.text).group(1)
                print("-------2")
            try:
                response = json.loads(response)

                # print("请求结果是", response)
                if 'SharingVideoModule' in str(response):
                    user_post = response['SharingVideoModule']['videoData']['itemInfo']['itemStruct']
                    # response = json.loads(response)['props']['pageProps']['itemInfo']
                else:
                    user_post = response['__DEFAULT_SCOPE__']['webapp.video-detail']['itemInfo']['itemStruct']

            except Exception as e:
                print(e)
                user_post = {}
            if user_post:
                return parse_post(user_post)
    fail_record = {
        'info': '请求失败, 请重试！！',
        'noteId': url,
    }
    return fail_record
       


def parse_user(response_user, type=1):
        item = {}
        # print(response_user)
        # user_info = response_user["users"][handle]

        region = ''
        if type == 3:
            user_info = response_user["data"]["user"]
        else:
            region = response_user["user"].get('region','') if type==1 else response_user["users"][list(response_user["users"].keys())[0]]['region']
            user_info = response_user["user"] if type==1 else response_user["users"][list(response_user["users"].keys())[0]]
        user_name = user_info["uniqueId"]
        user_id = user_info["id"]
        sec_uid = user_info["secUid"]
        fullname = user_info["nickname"]
        portrait_url = user_info.get("avatarLarger")
        is_private = user_info["privateAccount"]
        if is_private:
            is_private = 1
        else:
            is_private = 0
        is_open_favorite = user_info["openFavorite"]
        if is_open_favorite:
            is_open_favorite = 1
        else:
            is_open_favorite = 0
        is_verified = user_info["verified"]
        if is_verified:
            is_verified = 1
        else:
            is_verified = 0
        signature = user_info["signature"]
        if type == 3:
            user_stats = response_user["data"]["stats"]
        else:
            user_stats = response_user["stats"] if type == 1 else response_user["stats"][user_name]
        followers_count = user_stats["followerCount"]
        video_count = user_stats["videoCount"]
        followed_count = user_stats["followingCount"]
        diggedcount = user_stats["heartCount"]
        diggcount = user_stats["diggCount"]
        email = ''
        bio = signature
        if bio.find('.') != -1 and bio.find('@') != -1:
            email_list = re.findall(r'([\S]+?@\w*?\.\w*)', bio)
            email_list = set(email_list)
            email = ','.join(email_list)

        detail = {'sec_uid': sec_uid, 'signature': signature,
                  'followers_count': followers_count, 'video_count': video_count, 'followed_count': followed_count,
                  'diggedcount': diggedcount, 'diggcount': diggcount}
        item['email'] = email
        item['region'] = region
        item['user_id'] = user_id
        item['sec_uid'] = sec_uid
        item['user_name'] = user_name
        item['fullname'] = fullname
        item['portrait_url'] = portrait_url
        item['is_private'] = is_private
        item['is_open_favorite'] = is_open_favorite
        item['is_verified'] = is_verified
        item['detail'] = detail
        item['followers_count'] = followers_count
        item['video_count'] = video_count
        item['followed_count'] = followed_count
        item['diggedcount'] = diggedcount
        item['diggcount'] = diggcount
        item['bio_url'] = 'https://www.tiktok.com/@{}'.format(user_name)
        return item


def fetch_user_info(user_name):
    for i in range(1):
        user_url = "https://www.tiktok.com/@{}".format(user_name)
          
        # print(response.json())
        response = requests.get(user_url, headers=headers, params={}, timeout=10,proxies=proxy )
        response_text = response.text
        try:
            type = 1
            response_user = re.search(r'({"props.*?)\<\/script', response_text).group(1)
            response_user = json.loads(response_user)['props']['pageProps']['userInfo']
        except:
            type = 1
            info = re.findall('<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__" type="application/json">(.*?)</script><script', response.text)[0]
            response_user = json.loads(info).get("__DEFAULT_SCOPE__", {}).get('webapp.user-detail',{}).get('userInfo',{})

            
        userinfo = parse_user(response_user, type)
        # print(userinfo)
        record = {}

        record["nickname"] = userinfo['user_name']
        record["userid"] = userinfo['user_id']
        record["fans"] = userinfo['followers_count']
        record["ip_location"] = ''
        record["location"] = userinfo['region']
        record["post_count"] = userinfo['video_count']
        record["desc"] = userinfo['detail']['signature']
        record["image"] = userinfo['portrait_url']
        record["account_id"] = userinfo['sec_uid']
        # print(record)
        return record
    fail_record = {
        'info': '请求失败, 请重试！！',
        'userid': user_name,
    }
    return fail_record
               

def fetch_user_posts(unique_id, lastCursor=0):
    for i in range(1):
        lastCursor = lastCursor
        url = 'https://www.tikwm.com/api/user/posts?unique_id=@{}&count=35&cursor={}'.format(unique_id, lastCursor)
        print(url)
        

        payload = {}
        headers = {"User-Agent": "Apifox/1.0.0 (https://apifox.com)"}

        response = requests.request("GET", url, headers=headers, data=payload)
        # print(response.json())
        result_info = {'posts':[] }
        if response.json()["msg"] == "success":
            result_info['nickname'] = 'unique_id'
            lastCursor = response.json()["data"]['cursor']
            # cursor = ""
            for each in response.json()["data"]["videos"]:
                # print(each)
                # id = each["id"]
                # cursor = id
                post_id = each['video_id']
                title =  each['title']
                likes = each["digg_count"]
                nickname = each['author']['nickname']
                record = {}
                record["nickname"] = nickname
                record["userid"] = unique_id
                record["title"] = title
                record["desc"] = ''
                record["likes"] = likes
                record["post_url"] = "https://www.tiktok.com/@{}/video/{}".format(unique_id, post_id)
                record['cursor'] = lastCursor
                result_info['posts'].append(record)
                result_info['cursor'] = lastCursor
                print(record)
            return result_info
    fail_record = {
        'info': '请求失败, 请重试！！',
        'userid': unique_id,
    }
    return fail_record

if __name__ == "__main__":
    # 图
    # user_name = 'skylarrr_marie' 
    # record = fetch_user_info(user_name)
    # print(record)
    post_url = "https://www.tiktok.com/@fashionsnap/video/7410051289997987105"
    # post_url = "https://www.tiktok.com/@the.style.woman13/photo/7410051289997987105"
    record = fetch_posts_detail(post_url)
    print(record)


    # userid = 'skylarrr_marie'
    # record = fetch_user_posts(userid)
    # print(record)