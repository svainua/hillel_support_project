from rest_framework import serializers

class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField()
    
