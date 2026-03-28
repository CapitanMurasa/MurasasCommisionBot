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
    
    def SendSticker(self, sticker):
        params = {
            "chat_id": self.chat_id,
            "sticker": sticker
        }

        response = requests.post(self.url + "sendSticker", data=params)
    
    def SendPhoto(self, photo, caption):
        params = {
            "chat_id": self.chat_id,
            "photo": photo,
            "caption": caption
        }
        response = requests.post(self.url + "sendPhoto", data=params)

    def SendDocument(self, document, caption):
        params = {
            "chat_id": self.chat_id,
            "document": document,
            "caption": caption
        }
        response = requests.post(self.url + "sendDocument", data=params)

    def SendVideo(self, video, caption):
        params = {
            "chat_id": self.chat_id,
            "video": video,
            "caption": caption
        }
        response = requests.post(self.url + "sendVideo", data=params)

    def SendVoice(self, voice, caption):
        params = {
            "chat_id": self.chat_id,
            "voice": voice,
            "caption": caption
        }
        response = requests.post(self.url + "sendVoice", data=params)


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
                        if "photo" in message:
                            photo = message["photo"]
                            photoQuality = photo[len(photo) - 1]
                            fileid = photoQuality["file_id"]
                            if "caption" in photo:
                                caption = photo["caption"]
                            else:
                                caption = ""
                            self.SendPhoto(fileid, caption)

                        if "text" in message: 
                            text = message["text"]
                            self.SendMessage(f"text:{text}\nsent by:{sender_name}\nhis id is:{sender_id}")

                        if "document" in message:
                            document = message["document"]
                            fileid = document["file_id"]
                            if "caption" in document:
                                caption = document["caption"]
                            else:
                                caption = ""
                            self.SendDocument(fileid, caption)

                        if "video" in message:
                            video = message["video"]
                            fileid = video["file_id"]
                            if "caption" in video:
                                caption = video["caption"]
                            else:
                                caption = ""
                            self.SendVideo(fileid, caption)

                        if "voice" in message:
                            voice = message["voice"]
                            fileid = voice["file_id"]
                            if "caption" in voice:
                                caption = voice["caption"]
                            else:
                                caption = ""
                            self.SendVoice(fileid, caption)


                        if "sticker" in message:
                            sticker = message["sticker"]
                            fileid = sticker["file_id"]
                            self.SendSticker(fileid)

                        else:
                            return

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
        time.sleep(1)