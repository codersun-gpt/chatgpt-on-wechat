# 微信对话开放平台 channel

微信官方提供了微信对话开放平台可以接入对话机器人，对话机器能够接入公众号/小程序作为客服功能。

由于对话机器人接入是以第三方接口形式，并且允许自定义接口，所以本`channel`本质是`chatgpt-on-wechat`的一个后台服务器，接收对话请求并调用`chatgpt-on-wechat`的接口，返回结果。

在 chatgpt-on-wechat 项目中，该`channel`名称定义为`wechat_chatbot`。

[微信对话平台 api 配置说明](https://developers.weixin.qq.com/doc/aispeech/platform/3rdparty_api.html)

---

## 开始之前

- 在企业中确认自己拥有在企业内自建应用的权限。
- 如果没有权限或者是个人用户，也可创建未认证的企业。操作方式：登录手机企业微信，选择`创建/加入企业`来创建企业，类型请选择企业，企业名称可随意填写。
  未认证的企业有 100 人的服务人数上限，其他功能与认证企业没有差异。

本 channel 需安装的依赖与公众号一致，需要安装`wechatpy`和`web.py`，它们包含在`requirements-optional.txt`中。

此外，如果你是`Linux`系统，除了`ffmpeg`还需要安装`amr`编码器，否则会出现找不到编码器的错误，无法正常使用语音功能。

- Ubuntu/Debian

```bash
apt-get install libavcodec-extra
```

- Alpine

需自行编译`ffmpeg`，在编译参数里加入`amr`编码器的支持

## 使用方法

1.查看企业 ID

- 扫码登陆[企业微信后台](https://work.weixin.qq.com)
- 选择`我的企业`，点击`企业信息`，记住该`企业ID`

  2.创建自建应用

- 选择应用管理, 在自建区选创建应用来创建企业自建应用
- 上传应用 logo，填写应用名称等项
- 创建应用后进入应用详情页面，记住`AgentId`和`Secert`

  3.配置应用

- 在详情页点击`企业可信IP`的配置(没看到可以不管)，填入你服务器的公网 IP，如果不知道可以先不填
- 点击`接收消息`下的启用 API 接收消息
- `URL`填写格式为`http://url:port/wxcomapp`，`port`是程序监听的端口，默认是 9898
  如果是未认证的企业，url 可直接使用服务器的 IP。如果是认证企业，需要使用备案的域名，可使用二级域名。
- `Token`可随意填写，停留在这个页面
- 在程序根目录`config.json`中增加配置（**去掉注释**），`wechatcomapp_aes_key`是当前页面的`wechatcomapp_aes_key`

```python
    "channel_type": "wechatcom_app",
    "wechatcom_corp_id": "",  # 企业微信公司的corpID
    "wechatcomapp_token": "",  # 企业微信app的token
    "wechatcomapp_port": 9898,  # 企业微信app的服务端口, 不需要端口转发
    "wechatcomapp_secret": "",  # 企业微信app的secret
    "wechatcomapp_agent_id": "",  # 企业微信app的agent_id
    "wechatcomapp_aes_key": "",  # 企业微信app的aes_key
```

- 运行程序，在页面中点击保存，保存成功说明验证成功

  4.连接个人微信

选择`我的企业`，点击`微信插件`，下面有个邀请关注的二维码。微信扫码后，即可在微信中看到对应企业，在这里你便可以和机器人沟通。

向机器人发送消息，如果日志里出现报错:

```bash
Error code: 60020, message: "not allow to access from your ip, ...from ip: xx.xx.xx.xx"
```

意思是 IP 不可信，需要参考上一步的`企业可信IP`配置，把这里的 IP 加进去。

### Railway 部署方式

公众号不能在`Railway`上部署，但企业微信应用[可以](https://railway.app/template/-FHS--?referralCode=RC3znh)!

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/-FHS--?referralCode=RC3znh)

填写配置后，将部署完成后的网址`**.railway.app/wxcomapp`，填写在上一步的 URL 中。发送信息后观察日志，把报错的 IP 加入到可信 IP。（每次重启后都需要加入可信 IP）

## 测试体验

AIGC 开放社区中已经部署了多个可免费使用的 Bot，扫描下方的二维码会自动邀请你来体验。

<img width="200" src="../../docs/images/aigcopen.png">
