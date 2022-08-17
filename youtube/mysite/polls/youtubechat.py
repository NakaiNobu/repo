import configparser
from tkinter.tix import INTEGER
import requests
import json
import django

yt_api_key = ''
yt_url = ''

def init():
    config = configparser.SafeConfigParser()
    config.read('polls/setting.ini')

    section1 = 'YOUTUBE'
    global yt_api_key
    global yt_url
    yt_api_key  = config.get(section1, 'api')
    yt_url = config.get(section1, 'url')

    print(yt_api_key)
    print(yt_url)

    return

def get_chat_id(yt_url):
    '''
    https://developers.google.com/youtube/v3/docs/videos/list?hl=ja
    '''
    video_id = yt_url.replace('https://www.youtube.com/watch?v=', '')
    print('video_id : ', video_id)

    url    = 'https://www.googleapis.com/youtube/v3/videos'
    params = {'key': yt_api_key, 'id': video_id, 'part': 'liveStreamingDetails'}
    data   = requests.get(url, params=params).json()

    liveStreamingDetails = data['items'][0]['liveStreamingDetails']
    if 'activeLiveChatId' in liveStreamingDetails.keys():
        chat_id = liveStreamingDetails['activeLiveChatId']
        print('get_chat_id done!')
    else:
        chat_id = None
        print('NOT live')

    return chat_id


def res_chat(usr, message):
    config = configparser.SafeConfigParser()
    config.read('polls/setting.ini')

    section = 'SOUNDS'
    num =  int(config.get(section, 'num'))
    sounds = []
    for i in range(num):
        sounds.append(config.get(section, 'sound' + str(i)))
    
    dict = {
        'name' : usr,
        'message' : message,
        'sound' : sounds[0],
    }

    return dict

def get_chat(chat_id):
    '''
    https://developers.google.com/youtube/v3/live/docs/liveChatMessages/list
    '''
    url    = 'https://www.googleapis.com/youtube/v3/liveChat/messages'
    params = {'key': yt_api_key, 'liveChatId': chat_id, 'part': 'id,snippet,authorDetails'}
    
    data   = requests.get(url, params=params).json()

    try:
        #channelId = item['snippet']['authorChannelId']
        msg       = data['items'][-1]['snippet']['displayMessage']
        usr       = data['items'][-1]['authorDetails']['displayName']
        #supChat   = item['snippet']['superChatDetails']
        #supStic   = item['snippet']['superStickerDetails']
        return res_chat(usr, msg)

    except:
        return res_chat('', 'コメントがないよ！')


def main():
    init()
    print('work on {}'.format(yt_url))

    log_file = yt_url.replace('https://www.youtube.com/watch?v=', '') + '.txt'
    with open(log_file, 'a') as f:
        print('{} のチャット欄を記録します。'.format(yt_url), file=f)
    chat_id  = get_chat_id(yt_url)

    return get_chat(chat_id)
        