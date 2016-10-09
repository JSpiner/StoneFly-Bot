
from flask import Flask
from flask import Response
from flask import request
import json
import requests
import time

app = Flask(__name__)

@app.route('/event', methods = ['GET'])
def slack_oauth():
    print('hi2')
    challenge = request.args.get('hub.challenge')
    return challenge
#df
@app.route('/event', methods = ['POST'])
def fb_post():
    print('hi')
    print(request.data)
    try:
        jsonObject = json.loads(str(request.data, 'utf-8'))
        userId = jsonObject['entry'][0]['messaging'][0]['sender']['id']
        if 'is_echo' in jsonObject['entry'][0]['messaging'][0]['message']:
            print('no echo')
            return 'bot'
        if 'delivery' in jsonObject['entry'][0]['messaging'][0]:
            print('no echo')
            return 'bot'
        print(jsonObject['entry'][0]['messaging'][0]['message']['text'])
        text = jsonObject['entry'][0]['messaging'][0]['message']['text']
        if '누구' in text:
            send_msg(userId, '안녕하세요! 대화형 진단봇 Dr. StoneFly입니다!')
        elif '안녕' in text:
            send_msg(userId, '좋은 아침입니다!')
        elif '소개' in text:
            send_msg(userId, '"나지금아파" 를 입력하고 상태를 입력하면 여러분의 병을 진단해드려요~')
        elif '나지금아파' in text:
            send_btn1_1(userId, '환자분의 성별을 입력 해 주세요.')
        elif '성별_' in text:
            send_btn1_2(userId, '환자분의 나이를 입력 해 주세요.')
        elif '나이_' in text:
            send_msg(userId, '/진단 을 입력하고 현재 환자분의 몸 상태를 간단히 설명해 주세요.(ex : 열이 나고 두통이 있습니다.)')
        elif '/진단' in text:
            send_msg(userId, '환자분과 비슷한 증상을 검색중입니다.')
            
            time.sleep(2)

            url = "http://hackathon.yangs.party/"
            params = {
                'content' : text
            }
            r = requests.post(url, data = params).json()
            print(r)

            a1 = []

            for row1 in r:
                for row2 in r[row1]:
                    if row2 not in a1:
                        a1.append(row2)
            result = "혹시 이 중에 비슷한 증상이 있으신가요? \n\n"+"\n".join(a1)+"\n\n 이 중 유사한 증상을 '/결과' 명령과 함께 알려주세요 "
            send_msg(userId, result)
            print(a1)

        elif '/결과' in text:
            send_msg(userId, '환자분의 병을 진단하는 중입니다....')
            time.sleep(2)

            url = "http://hackathon.yangs.party/andSearch"
            params = {
                'content' : text[3:]
            }
            r = requests.post(url, data = params).json()
            print(r)

            a1 = []

            for row1 in r:
                if row1 not in a1:
                    if len(row1) == 3:
                        row1 = row1 + "(가장높음)";
                    a1.append(row1)
            result = "아래 증상일 가능성이 있습니다.\n\n "+"\n".join(a1)+"\n\n 자세한 사항은 아래 링크 혹은 가까운 병원을 방문해주세요\n추천병원 : 서울삼성암병원(1599-3114)"
            send_msg(userId, result)
            print(a1)
        elif 'test1' in text:
            send_btn1(userId, "메세지를 골라봐")
        elif 'test2' in text:
            send_btn2(userId, "메세지를 골라봐222")
            

    except Exception as e:
        print('error' + str(e))
        return 'er'
    return 'hi'

def send_btn2(userId, msg):
    print(userId)
    print(msg)
    url = "https://graph.facebook.com/v2.6/me/messages"
    token = "EAAC3LDhBZCtABABsgraEaeMmmmzxZAWFW6dcZCZAXReIwJGBDjWm8WXePyJNsGqIel4NXZCZB9ZCx3LU76cCGzFvFEbY6rLZCvVk43dGHi77v0GiNmYj4g0xqO0ZCCOYl2JWCqZCClIDs1SiPI5NiBPd8M7U4vhaXqeZBW4t5w2MoOiUwZDZD"

    param = {
        'access_token':token
    }
    data = {
        'recipient':{
            'id':userId
        },
        "message":{
            "attachment":{
                "type":"template",
                "payload":{
                    "template_type":"generic",
                    "elements":[
                        {
                            "title":"Classic White T-Shirt",
                            "image_url":"http://petersapparel.parseapp.com/img/whiteshirt.png",
                            "subtitle":"Soft white cotton t-shirt is back in style",
                            "buttons":[
                                {
                                    "type":"postback",
                                    "title":"Bookmark Item",
                                    "payload":"DEVELOPER_DEFINED_PAYLOAD"
                                }
                            ]
                        }
                    ]
                }
            }
        }
    }
    ret = requests.post("https://graph.facebook.com/v2.6/me/messages",
    params={"access_token": token},
    data = json.dumps(data),
    headers={'Content-type': 'application/json'})
    print(ret.text)

def send_btn1_2(userId, msg):
    print(userId)
    print(msg)
    url = "https://graph.facebook.com/v2.6/me/messages"
    token = "EAAC3LDhBZCtABABsgraEaeMmmmzxZAWFW6dcZCZAXReIwJGBDjWm8WXePyJNsGqIel4NXZCZB9ZCx3LU76cCGzFvFEbY6rLZCvVk43dGHi77v0GiNmYj4g0xqO0ZCCOYl2JWCqZCClIDs1SiPI5NiBPd8M7U4vhaXqeZBW4t5w2MoOiUwZDZD"

    param = {
        'access_token':token
    }
    data = {
        'recipient':{
            'id':userId
        },
        'message':{
            'text':msg,
            "quick_replies":[
                {
                    "content_type":"text",
                    "title":"나이_10대",
                    "payload":"DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_RED"
                },
                {
                    "content_type":"text",
                    "title":"나이_20대",
                    "payload":"DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_RED"
                },
                {
                    "content_type":"text",
                    "title":"나이_30대",
                    "payload":"DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_RED"
                },
                {
                    "content_type":"text",
                    "title":"나이_40대",
                    "payload":"DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_RED"
                },
                {
                    "content_type":"text",
                    "title":"나이_50대",
                    "payload":"DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_RED"
                },
                {
                    "content_type":"text",
                    "title":"나이_60대",
                    "payload":"DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_GREEN"
                }
            ]
        }
    }
    ret = requests.post("https://graph.facebook.com/v2.6/me/messages",
    params={"access_token": token},
    data=json.dumps(data),
    headers={'Content-type': 'application/json'})
    print(ret.text)

def send_btn1_1(userId, msg):
    print(userId)
    print(msg)
    url = "https://graph.facebook.com/v2.6/me/messages"
    token = "EAAC3LDhBZCtABABsgraEaeMmmmzxZAWFW6dcZCZAXReIwJGBDjWm8WXePyJNsGqIel4NXZCZB9ZCx3LU76cCGzFvFEbY6rLZCvVk43dGHi77v0GiNmYj4g0xqO0ZCCOYl2JWCqZCClIDs1SiPI5NiBPd8M7U4vhaXqeZBW4t5w2MoOiUwZDZD"

    param = {
        'access_token':token
    }
    data = {
        'recipient':{
            'id':userId
        },
        'message':{
            'text':msg,
            "quick_replies":[
                {
                    "content_type":"text",
                    "title":"성별_남자",
                    "payload":"DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_RED"
                },
                {
                    "content_type":"text",
                    "title":"성별_여자",
                    "payload":"DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_RED"
                }
            ]
        }
    }
    ret = requests.post("https://graph.facebook.com/v2.6/me/messages",
    params={"access_token": token},
    data=json.dumps(data),
    headers={'Content-type': 'application/json'})
    print(ret.text)

def send_btn1(userId, msg):
    print(userId)
    print(msg)
    url = "https://graph.facebook.com/v2.6/me/messages"
    token = "EAAC3LDhBZCtABABsgraEaeMmmmzxZAWFW6dcZCZAXReIwJGBDjWm8WXePyJNsGqIel4NXZCZB9ZCx3LU76cCGzFvFEbY6rLZCvVk43dGHi77v0GiNmYj4g0xqO0ZCCOYl2JWCqZCClIDs1SiPI5NiBPd8M7U4vhaXqeZBW4t5w2MoOiUwZDZD"

    param = {
        'access_token':token
    }
    data = {
        'recipient':{
            'id':userId
        },
        'message':{
            'text':msg,
            "quick_replies":[
                {
                    "content_type":"text",
                    "title":"Red",
                    "payload":"DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_RED"
                },
                {
                    "content_type":"text",
                    "title":"Red1",
                    "payload":"DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_RED"
                },
                {
                    "content_type":"text",
                    "title":"Red2",
                    "payload":"DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_RED"
                },
                {
                    "content_type":"text",
                    "title":"Red3",
                    "payload":"DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_RED"
                },
                {
                    "content_type":"text",
                    "title":"Red4",
                    "payload":"DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_RED"
                },
                {
                    "content_type":"text",
                    "title":"Green",
                    "payload":"DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_GREEN"
                }
            ]
        }
    }
    ret = requests.post("https://graph.facebook.com/v2.6/me/messages",
    params={"access_token": token},
    data=json.dumps(data),
    headers={'Content-type': 'application/json'})
    print(ret.text)


def send_msg(userId, msg):
    print(userId)
    print(msg)
    url = "https://graph.facebook.com/v2.6/me/messages"
    token = "EAAC3LDhBZCtABABsgraEaeMmmmzxZAWFW6dcZCZAXReIwJGBDjWm8WXePyJNsGqIel4NXZCZB9ZCx3LU76cCGzFvFEbY6rLZCvVk43dGHi77v0GiNmYj4g0xqO0ZCCOYl2JWCqZCClIDs1SiPI5NiBPd8M7U4vhaXqeZBW4t5w2MoOiUwZDZD"

    param = {
        'access_token':token
    }
    data = {
        'recipient':{
            'id':userId
        },
        'message':{
            'text':msg
        }
    }
    ret = requests.post("https://graph.facebook.com/v2.6/me/messages",
    params={"access_token": token},
    data=json.dumps(data),
    headers={'Content-type': 'application/json'})
    print(ret.text)

ssl_context = ('last.crt', 'ssoma.key')

app.run(host='0.0.0.0', debug='True', port = 90, ssl_context = ssl_context)