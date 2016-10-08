
from flask import Flask
from flask import Response
from flask import request
import json
import requests


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
            send_msg(userId, '안녕하세요! 대화형 진단봇 StoneFly입니다!')
        elif '소개' in text:
            send_msg(userId, '/진단 을 입력하고 상태를 입력하면 여러분의 병을 진단해드려요~')
        elif '/진단' in text:
            send_msg(userId, '안알랴줌')
            
            url = "http://hackathon.yangs.party/"
            params = {
                'content' : text
            }
            r = requests.post(url, params = prarms)
            print(r)

    except :
        print('error')
        return 'er'
    return 'hi'



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
    data=json.dumps({
      "recipient": {"id": userId},
      "message": {"text": msg}
    }),
    headers={'Content-type': 'application/json'})
    print(ret.text)

ssl_context = ('last.crt', 'ssoma.key')

app.run(host='0.0.0.0', debug='True', port = 90, ssl_context = ssl_context)