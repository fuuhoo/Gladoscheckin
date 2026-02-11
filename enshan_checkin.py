import requests
import json
import os

from pypushdeer import PushDeer

# -------------------------------------------------------------------------------------------
# github workflows
# -------------------------------------------------------------------------------------------
if __name__ == '__main__':
    # pushdeer key 申请地址 https://www.pushdeer.com/product.html
    sckey = os.environ.get("SENDKEY", "")
    # 推送内容
    title = ""
    success, fail, repeats = 0, 0, 0        # 成功账号数量 失败账号数量 重复签到账号数量
    context = ""


    # glados账号cookie 直接使用数组 如果使用环境变量需要字符串分割一下
    cookies = os.environ.get("ENSHAN_COOKIES", []).split("&")
    if cookies[0] != "":

        check_in_url = "https://www.right.com.cn/forum/plugin.php?id=erling_qd:action&action=sign"        # 签到地址
        # status_url = "https://glados.cloud/api/user/status"          # 查看账户状态

        referer = 'https://www.right.com.cn/forum/erling_qd-sign_in.html'
        origin = "https://www.right.com.cn"
        useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"
        payload = {
            'formhash': 'daf5405d'
        }
        
        for cookie in cookies:
            checkin = requests.post(check_in_url, headers={'cookie': cookie, 'referer': referer, 'origin': origin,
                                    'user-agent': useragent, 'content-type': 'application/x-www-form-urlencoded'}, data=payload)



            message_status = ""
            points = 0
            message_days = ""
            
            
            if checkin.status_code == 200:
                # 解析返回的json数据
                result = checkin.json()     
                # 获取签到结果
                check_result = result.get('message')
                continuous_days = result.get('continuous_days')

                # 获取账号当前状态
                # result = state.json()
                # 获取剩余时间
                # leftdays = int(float(result['data']['leftDays']))
                # # 获取账号email
                # email = result['data']['email']
                
                print("签到结果:",check_result)
                if "签到成功" in check_result:
                    success += 1
                    message_status = "签到成功，连续签到时间 +" + str(continuous_days)
                    context+=message_status
                    title = f'恩山论坛,签到成功'
                else:
                    print("签到失败原因1:",check_result)
                    fail += 1
                    message_status = "签到失败，请检查..."
                    context+=message_status
                    title = f'恩山论坛,签到失败'
            else:
                print("签到失败原因2:",text)
                email = ""
                message_status = "签到失败, 请检查..."
                message_days = "-1"
                context+=message_status

            # context += "账号: " + email + ", P: " + str(points) +", 剩余: " + message_days + " | "

        # 推送内容 
        # print("Send Content:" + "\n", context)
        
    else:
        # 推送内容 
        title = f'# 恩山论坛，未找到enshan cookies!'

    print("enshan_sckey:", sckey)
    print("enshan_cookies:", cookies)
    print("enshan_Send Content:", context)
 
    # 推送消息
    # 未设置 sckey 则不进行推送
    if not sckey:
        print("Not push")
    else:
        pushdeer = PushDeer(pushkey=sckey) 
        pushdeer.send_text(title, desp=context)


