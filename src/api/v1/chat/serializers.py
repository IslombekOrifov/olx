from rest_framework import serializers

from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        exclude = ['is_deleted',]

    def validate(self, attrs):
        if not attrs['body'] and not attrs['image']:
            raise serializers.ValidationError('You must enter message body or image')
        return super().validate(attrs)
