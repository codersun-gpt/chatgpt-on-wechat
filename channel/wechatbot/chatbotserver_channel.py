# -*- coding=utf-8 -*-

from flask import Flask, request
from bridge.context import *

from bridge.context import Context
from bridge.reply import Reply
from channel.chat_channel import ChatChannel
from channel.wechatbot.chatbotserver_message import ChatbotServerMessage
from common.log import logger
from common.singleton import singleton
from config import conf

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
        logger.info("[chatbot] requestId:{} msg:[{}] reply: [{}]".format("context.msg_id", context.content, reply))


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

    context = channel._compose_context(ContextType.TEXT, msg,msg=ChatbotServerMessage(requestId, uid, msg))
    if context:
        channel.produce(context)

    return {"data_list": {"reply": "reply:" + msg}, "error_code": 0}
