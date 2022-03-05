from aiocqhttp import CQHttp, Event
import httpx
import json
bot = CQHttp()

#读取配置文件
with open("config.json","r") as f:
    config = json.load(f)
MiPush = config[0]["MiPush"]
FCM = config[1]["FCM"]
KEY = config[2]["KEY"]
group_whitelist = config[3]["WhiteList"]

print("MiPush状态:"+MiPush)
print("FCM状态:"+FCM)
print("已配置的KEY:"+KEY)
@bot.on_message('private')
async def _(event: Event):
    msg = event['message']
    if "CQ:image" in msg:
        msg = "[图片]"
    elif "CQ:record" in msg:
        msg = "[语音]"
    elif "CQ:share" in msg:
        msg = "[链接]"
    elif "CQ:music" in msg:
        msg = "[音乐分享]"
    elif "CQ:redbag" in msg:
        msg = "[红包]"
    elif "CQ:forward" in msg:
        msg = "[合并转发]"
    nickName = event['sender']["nickname"]
    print("收到来自%s的私聊消息:%s"%(nickName,msg))
    async with httpx.AsyncClient() as client:
        if MiPush == True:
            await client.post("https://tdtt.top/send",data={'title':'%s'%nickName,'content':'%s'%(msg),'alias':KEY})
        if FCM == True:
            await client.post("http://xdroid.net/api/message",data={'t':'%s'%groupName,'c':'%s:%s'%(nickName,msg),'k':KEY})
@bot.on_message('group')
async def _(event: Event):
    groupId = str(event['group_id'])
    if groupId in group_whitelist:
        msg = event['message']
        if "CQ:image" in msg:
            msg = "[图片]"
        elif "CQ:record" in msg:
            msg = "[语音]"
        elif "CQ:share" in msg:
            msg = "[链接]"
        elif "CQ:music" in msg:
            msg = "[音乐分享]"
        elif "CQ:redbag" in msg:
            msg = "[红包]"
        elif "CQ:forward" in msg:
            msg = "[合并转发]"
        nickName = event['sender']
        groupName = group_whitelist[groupId]
        if nickName['card'] != "":
            nickName = nickName['card']
        elif nickName['card'] == "":
            nickName = nickName['nickname']
        print("收到来自%s的群聊消息:%s"%(groupName,msg))
        async with httpx.AsyncClient() as client:
            if MiPush == True:
                await client.post("https://tdtt.top/send",data={'title':'%s'%groupName,'content':'%s:%s'%(nickName,msg),'alias':KEY})
            if FCM == True:
                await client.post("http://xdroid.net/api/message",data={'t':'%s'%groupName,'c':'%s:%s'%(nickName,msg),'k':KEY})
bot.run(host='127.0.0.1', port=8081)
