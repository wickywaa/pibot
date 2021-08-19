import socketio, json
from botdata import botDetails
from webRTCHandler import handleBotPreOffer, handleBotWebRTCOffer
import asyncio
import aiohttp
sio= socketio.AsyncClient()




botdetails = botDetails()


newBotdata = {
    **botdetails,
    "botsurname":"guess"
    }




@sio.event
def connect():
    print('connected to warbotz')

async def registerBot():
    await sio.emit('register-new-bot',newBotdata)


async def preOfferAnswer(data):
    await sio.emit('bot-pre-offer-answer',data)


@sio.on('bot-pre-offer')
async def onPreOffer(data):
    print('got the pre offer', data)
    await  handleBotPreOffer(data,preOfferAnswer)


async def webRTCOfferAnswer(data):
    print(data)
    print('sending back the webrtc offer')
    await  sio.emit('bot_web_rtc_answer',data)

@sio.on('bot_webrtc_offer')
async def onTCeOffer(data):
    print('got the RTC Offer')
    await handleBotWebRTCOffer(data,webRTCOfferAnswer)

async def main():
    await sio.connect('https://b0b91055329d.ngrok.io')
    await registerBot()
    await sio.wait()


if __name__ == '__main__':
    asyncio.run(main())
