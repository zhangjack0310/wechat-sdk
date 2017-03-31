#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import json


from django.views.decorators.csrf import csrf_exempt

from wechat_sdk.basic import WechatBasic

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
            rsp = wechat.response_text(u'消息类型: {}'.format(message.type))
    else:
        rsp = wechat.response_text('check error')
    return HttpResponse(rsp)




def test(request):
    print request
    a = {"good":123}
    ret = json.dumps(a)
    return JsonResponse(a)