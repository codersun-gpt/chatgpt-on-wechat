from wechatpy.enterprise import WeChatClient

from bridge.context import ContextType
from channel.chat_message import ChatMessage
from common.log import logger
from common.tmp_dir import TmpDir


class ChatbotServerMessage(ChatMessage):
    def __init__(
        self,
        msg_id,
        from_user_id,
        content,
        ctype=ContextType.TEXT,
        to_user_id="Chatgpt",
        other_user_id="Chatgpt",
    ):
        self.msg_id = msg_id
        self.ctype = ctype
        self.content = content
        self.from_user_id = from_user_id
        self.to_user_id = to_user_id
        self.other_user_id = other_user_id
