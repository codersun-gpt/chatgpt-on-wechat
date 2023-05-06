# -*- coding=utf-8 -*-
import io
import os
import time

import requests
from flask import Flask, request
from bridge.context import *
import web
from wechatpy.enterprise import create_reply, parse_message
from wechatpy.enterprise.crypto import WeChatCrypto
from wechatpy.enterprise.exceptions import InvalidCorpIdException
from wechatpy.exceptions import InvalidSignatureException, WeChatClientException

from bridge.context import Context
from bridge.reply import Reply, ReplyType
from channel.chat_channel import ChatChannel
from channel.wechatbot.chatbotserver_message import ChatbotServerMessage
from common.log import logger
from common.singleton import singleton
from common.utils import compress_imgfile, fsize, split_string_by_utf8_length
from config import conf, subscribe_msg
from voice.audio_convert import any_to_amr, split_audio

MAX_UTF8_LEN = 2048


app = Flask(__name__)


@singleton
class ChatBotServerChannel(ChatChannel):
    NOT_SUPPORT_REPLYTYPE = []

    def __init__(self):
        super().__init__()

    def startup(self):
        # start message listener
        port = conf().get("chatbot_server_port", 9898)
        app.run("0.0.0.0", port, debug=True)

    def send(self, reply: Reply, context: Context):
        logger.info("[chatbot] requestId:{} msg:[{}] reply: [{}]".format(Context.msg_id, Context.content, reply))


@app.route("/chatbot", methods=["GET", "POST"])
def chatBot():
    # 获取header信息
    channel = ChatBotServerChannel()
    headers = dict(request.headers)

    requestId = headers.get("Requestid", "")
    bid = headers.get("Bid", "")
    uid = headers.get("Uid", "")
    appId = headers.get("AppId", "")

    # 获取请求参数
    params = {}
    for key in request.args:
        params[key] = request.args.get(key)

    logger.info("[chatbot] receive head:{} params: {}".format(headers, params))

    msg = params["msg"]

    context = channel._compose_context(ContextType.TEXT, msg, msg=ChatbotServerMessage(requestId, uid, msg))
    if context:
        channel.produce(context)

    return {"data_list": {"reply": "reply:" + msg}, "error_code": 0}
