from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import Comment
import json

class CommentConsumer(AsyncWebsocketConsumer):


    async def connect(self):
        self.task_id = self.scope['url_route']['kwargs']['task_id']
        self.task_group_name = 'comment_%s' % self.task_id

        await self.channel_layer.group_add(
            self.task_group_name,
            self.channel_name
        )

        await self.accept()


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.task_group_name,
            self.channel_name
        )


    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        type = text_data_json['type']

        if type == 'comment_message':
            message = text_data_json['message']
            user = text_data_json['user']
            task = self.task_id
            get_user = User.objects.get(id=int(user))

            #insertDB
            addComment = Comment(comment=message,task_id=task,user=get_user)
            addComment.save()

            await self.channel_layer.group_send(
                self.task_group_name,
                {
                    'type': type,
                    'message': message,
                    'user':get_user.username,
                    'comment_id':addComment.id
                    }
                )

        elif type == 'delete_comment':
            comment_id = text_data_json['comment_id']

            #insertDB
            deleteComment = Comment(id=comment_id)
            deleteComment.delete()

            await self.channel_layer.group_send(
                self.task_group_name,
                {
                    'type': type,
                    'comment_id': comment_id
                    }
                )
        elif type == 'edit_comment':
            comment_id = text_data_json['comment_id']
            edited_comment = text_data_json['edited_comment']

            #updateDB
            updateComment = Comment.objects.filter(id=comment_id).update(comment=edited_comment)

            await self.channel_layer.group_send(
                self.task_group_name,
                {
                    'type': type,
                    'comment_id': comment_id,
                    'comment':edited_comment
                    }
                )


    async def comment_message(self, event):

        message = event['message']
        user = event["user"]
        comment_id = event["comment_id"]

        await self.send(text_data=json.dumps({
            'type':'comment_message',
            'message': message,
            'comment_id':comment_id,
            'user':user,
        }))

    async def delete_comment(self, event):
        comment_id = event["comment_id"]

        await self.send(text_data=json.dumps({
            'type':'delete_comment',
            'comment_id':comment_id
        }))

    async def edit_comment(self, event):
        comment_id = event["comment_id"]
        comment = event["comment"]

        await self.send(text_data=json.dumps({
            'type':'edit_comment',
            'comment_id':comment_id,
            'message':comment,
        }))
