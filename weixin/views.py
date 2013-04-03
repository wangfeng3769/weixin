# -*- coding: utf-8 -*-
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
import xml.etree.ElementTree as ET
from weixin.helper import judge_text, text_reply, to_unicode, userinfo_add, music_reply, judge_event, judge_location, weixinmessage_add, judge_voice
import hashlib
import time
TOKEN = 'leyingke'   #用于测试的名称
LYKNU = 'gh_0b00ec6bdcbc' # 乐影客微信账号
def check_signature(request):
    """本功能用于首次的签名验证，首次验证签名功能后即可注释掉"""
    global TOKEN
    signature = request.GET.get("signature", None)
    timestamp = request.GET.get("timestamp", None)
    nonce = request.GET.get("nonce", None)
    echoStr = request.GET.get("echostr",None)
    # print signature,timestamp,nonce,echoStr

    token = TOKEN
    tmpList = [token,timestamp,nonce]
    tmpList.sort()
    tmpstr = "%s%s%s" % tuple(tmpList)
    tmpstr = hashlib.sha1(tmpstr).hexdigest()
    if tmpstr == signature:
        return HttpResponse(echoStr,content_type="text/plain")
    else:
        return HttpResponse('none',content_type="text/plain")

def parse_msg(request):
    """此函数用于解析XML文档，确定XML的类型"""
    msg ={}
    xlm_tree = request.body
    # print str(xlm_tree)
    # xlm_tree = request.raw_post_data         #此处可以代替上一个表达式
    # print repr(xlm_tree)
    root= ET.fromstring(xlm_tree)
    for child in root:
        msg[child.tag] = to_unicode(child.text)
        # print msg
    # print msg
    userinfo_add(msg)
    weixinmessage_add(msg,xlm_tree)

    return msg

@csrf_exempt   #此函数用来避免403错误
def wechat(request):
    if request.method =="GET":
        return check_signature(request)
    if request.method =="POST":
        content =  response_msg(request)
        # print content
        return HttpResponse(content,content_type = "application/xml")

def response_msg(request):
    msg = parse_msg(request)
    # print msg
    if msg['MsgType'] == 'text':
        return judge_text(msg)
    elif msg['MsgType'] == 'music':
        response_content = dict(content = judge_text(msg),
            touser = msg['FromUserName'],
            fromuser = msg['ToUserName'],
            createtime = str(int(time.time())),)
        return music_reply.format(**response_content)

    elif msg['MsgType'] == 'event':
        return judge_event(msg)

    elif msg['MsgType'] == 'location':
        return judge_location(msg)
    elif msg['MsgType'] == 'voice':
        return judge_voice(msg)

