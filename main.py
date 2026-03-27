import requests, time

import settings

class commissionBot:
    def __init__(self):
        self.token = settings.token
        self.chat_id = "795546759"
        self.url = f"https://api.telegram.org/bot{self.token}/"
    
    def SendMessage(self, message):
        params = {
            "chat_id": self.chat_id,
            "text": message
        }

        response = requests.post(self.url + "sendMessage", data=params)
    
    def GetUpdates(self):
        response = requests.get(self.url + "getUpdates?offset=-1")
        return response.json()

    def GetMessage(self, pastmessageid):
        response = self.GetUpdates()
        if response.get("ok"):
            messages = response.get("result", [])
            for update in messages:
                if "message" in update:
                    message = update["message"]
                    currentmessageid = message["message_id"]
                    if currentmessageid != pastmessageid:
                        sender_id = message["from"]["id"]
                        sender_name = message["from"]["username"]
                        text = message["text"]
                        self.SendMessage(f"text:{text}\nsent by:{sender_name}\nhis id is:{sender_id}")
                        pastmessageid = currentmessageid

    def GetMessageId(self):
        response = self.GetUpdates()
        if response.get("ok"):
            messages = response.get("result", [])
            for update in messages:
                if "message" in update:
                    message = update["message"]
                    currentmessageid = message["message_id"]
                    return currentmessageid
        
    

if __name__ == "__main__":
    pastmessageid = ""
    while True:
        commbot = commissionBot()
        messagesResponse = commbot.GetMessage(pastmessageid)
        pastmessageid = commbot.GetMessageId()
        time.sleep(2)