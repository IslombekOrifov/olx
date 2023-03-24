from rest_framework import serializers

from .models import MainComplaint, Complaint


class MainComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainComplaint
        fields = "__all__"
        extra_kwargs = {
            'creator': {'read_only': True},
            'created_date': {'read_only': True},
            'updated_date': {'read_only': True},
        }



class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = "__all__"
        extra_kwargs = {
            'client': {'read_only': True},
            'created_date': {'read_only': True},
            'updated_date': {'read_only': True},
        }

