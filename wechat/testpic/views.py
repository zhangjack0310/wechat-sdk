#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import json
import time
from PIL import Image


from django.views.decorators.csrf import csrf_exempt

from wechat_sdk.basic import WechatBasic
from wechat_sdk.messages import TextMessage, VoiceMessage, ImageMessage, VideoMessage, LinkMessage, LocationMessage
import requests
import os
from os.path import dirname
from wechat_sdk import WechatBasic
dirn = dirname(__file__)

def deal_pic():
    dirn = dirname(__file__)
    print dirn
    with open("%s/1314.jpg"%dirn,'w') as f:
        a = requests.get('http://mmbiz.qpic.cn/mmbiz_jpg/l45ibT5PYBP7evNSRwmia0dom5HUY2HrJ4SXkFH7PykKF68mAxrIbibFVzVrFJUbKW4skLVPQQiaDYZy8Ee0CEP4lQ/0')

        f.write(a.content)
        f.close()

token = 'zhang310'

class Msg(object):
    def __init__(self, xmlData):
        self.ToUserName = xmlData.find('ToUserName').text
        self.FromUserName = xmlData.find('FromUserName').text
        self.CreateTime = xmlData.find('CreateTime').text
        self.MsgType = xmlData.find('MsgType').text
        self.MsgId = xmlData.find('MsgId').text


class ImageMsg(Msg):
    def __init__(self, toUserName, fromUserName, mediaId):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['MediaId'] = mediaId
    def send(self):
        XmlForm = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[image]]></MsgType>
        <Image>
        <MediaId><![CDATA[{MediaId}]]></MediaId>
        </Image>
        </xml>
        """
        return XmlForm.format(**self.__dict)





@csrf_exempt
def home(request):
    wechat = WechatBasic(token=token)
    if wechat.check_signature(signature=request.GET['signature'],
                              timestamp=request.GET['timestamp'],
                              nonce=request.GET['nonce']):
        if request.method == 'GET':
            rsp = request.GET.get('echostr', 'error')
        else:
            wechat.parse_data(request.body)
            message = wechat.get_message()
            print dir(message)
            t =  message.source
            print t
            pid = message.media_id
            print pid
            print message.picurl
            deal_pic()
            try:
                if isinstance(message, ImageMessage):
                    path = "%s/1314.jpg" % dirn
                    with open (path,"r") as f:
                        print 111,WechatBasic(appid='wxf7351e88c4bffc0f',appsecret='60ca3e67fedfdbc127f23c980fe0acb3').upload_media(media_type='image', media_file=f)
                    rsp = wechat.response_image(pid)
                    # im = Image.open(message.raw)
                    # out = im.transpose(Image.FLIP_LEFT_RIGHT)
                    # print "here"
                    # rsp = wechat.response_image(out)
                    # print "rsp", rsp
                else:
                    content = message.content
                    print content
                    rsp = wechat.response_text(u'消息类型: {}'.format(message.type))
            except Exception as e:
                print e,"error"
                print message
                rsp = wechat.response_text(message)
    else:
        rsp = wechat.response_text('check error')
    return HttpResponse(rsp)




def test(request):
    print request
    a = request.POST.get()
    print request
    a = {"good":123}
    ret = json.dumps(a)
    return JsonResponse(a)