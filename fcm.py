import requests
import json

class FCM:
    url = 'https://fcm.googleapis.com/fcm/send'
    headers = {
        "Content-Type": "application/json", 
        "Authorization": "key=AAAAbDmb7w0:APA91bFzl8Um4yfoxL4T7x7BczrOskMS6DbGrJzBHHgSkWVfMu6w6N6ss7XlUrFM3CTosC92DLHZZjqiUqbAgowHSHALBb2YJ2g125952rT8FKrKxJ053xcjEYc0lhdilI3BtM9pAgpf"
    }
    data = dict()
    data['to'] = "/topics/news"

    def __init__(self, news):
        self.news = news
    
    def send_notification(self):
        FCM.data['notification'] = {
                                    "title": self.news.title,
                                    "body": self.news.pub_source,
                                    "sound": "default"
                                }
        response = requests.post(FCM.url, data=json.dumps(FCM.data), headers=FCM.headers)
        return response.status_code
        
