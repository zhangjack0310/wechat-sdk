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


#zhanggengid:  wx9e08f08dcf4dae91
#secret :  40ca19f92fad40425288fa377d1e2f3e

def deal_pic(url):
    dirn = dirname(__file__)
    path = "%s/temp.jpg"%dirn
    outpath = "%s/out.jpg"%dirn
    print dirn
    with open(path,'w') as f:
        a = requests.get(url)
        f.write(a.content)
        f.close()
    im = Image.open(path)
    out = im.transpose(Image.FLIP_LEFT_RIGHT)
    out.save(outpath)
    os.popen('rm %s'%path)
    return outpath

token = 'zhang310'





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
            try:
                if isinstance(message, ImageMessage):
                    t = message.source
                    pid = message.media_id
                    picurl = message.picurl
                    path = deal_pic(picurl)
                    with open (path,"r") as f:
                        res = WechatBasic(appid='wx9e08f08dcf4dae91', appsecret='40ca19f92fad40425288fa377d1e2f3e').upload_media(media_type='image', media_file=f)
                        print res
                        f.close()
                        os.popen('rm %s'%path)
                    if res.get('media_id'):
                        media_id = res.get('media_id')
                        print media_id
                        rsp = wechat.response_image(media_id)
                    else:
                        rsp = wechat.response_text(u'Something wrong,we are working on it!')
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