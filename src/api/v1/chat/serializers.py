from rest_framework import serializers

from .models import Chat, ChatMessage


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        exclude = ['is_deleted', 'date_created']


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        exclude = ['is_deleted']
        extra_kwargs = {
            'date_created': {'read_only': True}
        }
    def validate(self, attrs):
        if not attrs['body'] and not attrs['image']:
            raise serializers.ValidationError('You must enter message body or image')
        return super().validate(attrs)