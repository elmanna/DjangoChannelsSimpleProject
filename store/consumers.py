import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class storeConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        
        self.room_group_name = "gg"
        
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'msg': f"Server: [شخصٌ ما إتصل]"
            }
        )
        # self.send(text_data=json.dumps({
        #     'type': 'connection',
        #     'message': "connected!"
        # }))
        
    def receive(self, text_data=None, bytes_data=None):
        # self.send(
        #     text_data=json.dumps({
        #             'type': 'message',
        #             'msg': text_data,
        #         },
        #     )
        # )
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'msg': text_data
            }
        )
    
    def chat_message(self, e):
        msg = e['msg']
        
        self.send(
            text_data=json.dumps({
                    'type': 'message',
                    'msg': msg,
                },
            )
        )
        
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'msg': f"Server: [ تم فقدان الإتصال بأحد المتصلين]"
            }
        )