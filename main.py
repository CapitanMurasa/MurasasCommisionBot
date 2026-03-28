import requests
import time
import settings

class commissionBot:
    def __init__(self):
        self.token = settings.token
        self.chat_id = "795546759"
        self.url = f"https://api.telegram.org/bot{self.token}/"
        
        self.last_update_id = None
        self.keyboard = {}
        

    def Keyboard(self, sender_id):
        return {
            "inline_keyboard": [
                [
                    {"text": "Approve", "callback_data": f"approve_{sender_id}"},
                    {"text": "Reject", "callback_data": f"reject_{sender_id}"}
                ]
            ]
        } 
    
    def SendMessage(self, message):
        params = {"chat_id": self.chat_id,
                   "text": message,
                   "reply_markup": self.keyboard}
        requests.post(self.url + "sendMessage", json=params)

    def SendSystemMessage(self, message, chat_id):
        params = {"chat_id": chat_id,
                   "text": message}
        requests.post(self.url + "sendMessage", json=params)
    
    def SendSticker(self, sticker):
        params = {"chat_id": self.chat_id,
                  "sticker": sticker,
                  "reply_markup": self.keyboard}
        requests.post(self.url + "sendSticker", json=params)
    
    def SendPhoto(self, photo, caption):
        params = {"chat_id": self.chat_id,
                   "photo": photo,
                   "caption": caption,
                   "reply_markup": self.keyboard}
        requests.post(self.url + "sendPhoto", json=params)

    def SendDocument(self, document, caption):
        params = {"chat_id": self.chat_id,
                  "document": document,
                  "caption": caption,
                  "reply_markup": self.keyboard}
        requests.post(self.url + "sendDocument", json=params)

    def SendVideo(self, video, caption):
        params = {"chat_id": self.chat_id,
                  "video": video,
                  "caption": caption,
                  "reply_markup": self.keyboard}
        requests.post(self.url + "sendVideo", json=params)

    def SendVoice(self, voice, caption):
        params = {"chat_id": self.chat_id,
                  "voice": voice,
                  "caption": caption,
                  "reply_markup": self.keyboard}
        requests.post(self.url + "sendVoice", json=params)

    def SendAudio(self, audio, caption):
        params = {"chat_id": self.chat_id,
                  "audio": audio,
                  "caption": caption,
                  "reply_markup": self.keyboard}
        requests.post(self.url + "sendAudio", json=params)

    def copy_message(self, chat_id, message_id):
        params = {
            "chat_id": chat_id,
            "from_chat_id": self.chat_id,
            "message_id": message_id
        }
        requests.post(self.url + "copyMessage", json=params)
    
    def GetUpdates(self):
        url = self.url + "getUpdates"
        if self.last_update_id is not None:
            url += f"?offset={self.last_update_id + 1}"
            
        response = requests.get(url)
        return response.json()

    def GetMessage(self): 
        response = self.GetUpdates()
        if response.get("ok"):
            messages = response.get("result", [])
            for update in messages:
                
                self.last_update_id = update["update_id"]
                pastupdateid = self.last_update_id - 1
                
                if "callback_query" in update:
                    callback = update["callback_query"]
                    callback_id = callback["id"]
                    button_data = callback["data"]
                    
                    currentmessageid = callback["message"]["message_id"]

                    if button_data.startswith("approve_"):
                        original_sender_id = button_data.split("_")[1]
                        self.copy_message(-1003074081220, currentmessageid)
                        self.SendSystemMessage("your commision was approved!", original_sender_id)
                        
                    elif button_data.startswith("reject_"):
                        original_sender_id = button_data.split("_")[1]
                        self.SendSystemMessage("lol", original_sender_id)
                        
                    requests.post(self.url + "answerCallbackQuery", json={"callback_query_id": callback_id})
                    
                    continue 
                
                elif "message" in update:
                    message = update["message"]
                    sender_id = message["from"]["id"]
                    sender_name = message["from"].get("username", "No_Username")
                    base_caption = message.get("caption", "")
                    final_caption = base_caption + f"\nsent by: {sender_name}"

                    self.SendSystemMessage(f"message sent to admin! Just wait till he will aprove...", sender_id)
                    
                    self.keyboard = self.Keyboard(sender_id)

                    if "photo" in message:
                        photo = message["photo"]
                        fileid = photo[-1]["file_id"]
                        self.SendPhoto(fileid, final_caption)

                    elif "text" in message: 
                        text = message["text"]
                        self.SendMessage(f"{text}\nsent by: {sender_name}")

                    elif "document" in message:
                        document = message["document"]
                        fileid = document["file_id"]
                        self.SendDocument(fileid, final_caption)

                    elif "video" in message:
                        video = message["video"]
                        fileid = video["file_id"]
                        self.SendVideo(fileid, final_caption)

                    elif "voice" in message:
                        voice = message["voice"]
                        fileid = voice["file_id"]
                        self.SendVoice(fileid, final_caption)

                    elif "sticker" in message:
                        sticker = message["sticker"]
                        fileid = sticker["file_id"]
                        self.SendSticker(fileid)

                    elif "audio" in message:
                        audio = message["audio"]
                        fileid = audio["file_id"]
                        self.SendAudio(fileid, final_caption)


if __name__ == "__main__":
    commbot = commissionBot()
    
    while True:
        commbot.GetMessage()
        time.sleep(2)