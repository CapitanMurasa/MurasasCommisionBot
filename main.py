import requests, time

import settings

class commissionBot:
    def __init__(self):
        self.token = settings.token
        self.chat_id = "795546759"
        self.url = f"https://api.telegram.org/bot{self.token}/"
        self.keyboard = {
        "inline_keyboard": [
            [
                {"text": "Approve", "callback_data": "action_approve"},
                {"text": "Reject", "callback_data": "action_reject"}
            ]
        ]
        }  
    
    def SendMessage(self, message):
        params = {
            "chat_id": self.chat_id,
            "text": message,
            "reply_markup": self.keyboard
        }

        response = requests.post(self.url + "sendMessage", json=params)
    
    def SendSticker(self, sticker):
        params = {
            "chat_id": self.chat_id,
            "sticker": sticker,
            "reply_markup": self.keyboard
        }

        response = requests.post(self.url + "sendSticker", json=params)
    
    def SendPhoto(self, photo, caption):
        params = {
            "chat_id": self.chat_id,
            "photo": photo,
            "caption": caption,
            "reply_markup": self.keyboard
        }
        response = requests.post(self.url + "sendPhoto", json=params)

    def SendDocument(self, document, caption):
        params = {
            "chat_id": self.chat_id,
            "document": document,
            "caption": caption,
            "reply_markup": self.keyboard
        }
        response = requests.post(self.url + "sendDocument", json=params)

    def SendVideo(self, video, caption):
        params = {
            "chat_id": self.chat_id,
            "video": video,
            "caption": caption,
            "reply_markup": self.keyboard
        }
        response = requests.post(self.url + "sendVideo", json=params)

    def SendVoice(self, voice, caption):
        params = {
            "chat_id": self.chat_id,
            "voice": voice,
            "caption": caption,
            "reply_markup": self.keyboard
        }
        response = requests.post(self.url + "sendVoice", json=params)

    def SendAudio(self, audio, caption):
        params = {
            "chat_id": self.chat_id,
            "audio": audio,
            "caption": caption,
            "reply_markup": self.keyboard
        }
        response = requests.post(self.url + "sendAudio", json=params)

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
                            caption = caption + f"\nsent by: {sender_name}"
                            self.SendPhoto(fileid, caption)

                        if "text" in message: 
                            text = message["text"]
                            self.SendMessage(f"text:{text}\nsent by:{sender_name}")

                        if "document" in message:
                            document = message["document"]
                            fileid = document["file_id"]
                            if "caption" in document:
                                caption = document["caption"]
                            else:
                                caption = ""
                            caption = caption + f"\nsent by: {sender_name}"
                            self.SendDocument(fileid, caption)

                        if "video" in message:
                            video = message["video"]
                            fileid = video["file_id"]
                            if "caption" in video:
                                caption = video["caption"]
                            else:
                                caption = ""
                            caption = caption + f"\nsent by: {sender_name}"
                            self.SendVideo(fileid, caption)

                        if "voice" in message:
                            voice = message["voice"]
                            fileid = voice["file_id"]
                            if "caption" in voice:
                                caption = voice["caption"]
                            else:
                                caption = ""
                            caption = caption + f"\nsent by: {sender_name}"
                            self.SendVoice(fileid, caption)


                        if "sticker" in message:
                            sticker = message["sticker"]
                            fileid = sticker["file_id"]
                            self.SendSticker(fileid)

                        if "audio" in message:
                            audio = message["audio"]
                            fileid = audio["file_id"]
                            if "caption" in audio:
                                caption = audio["caption"]
                            else:
                                caption = ""
                            caption = caption + f"\nsent by: {sender_name}"
                            self.SendAudio(fileid, caption)

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
        time.sleep(2)