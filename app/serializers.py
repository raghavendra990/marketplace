from rest_framework import serializers

class SerializerSignup(serializers.Serializer):

    name = serializers.CharField(max_length=50)
    email = serializers.EmailField(max_length=100)
    password = serializers.CharField(max_length=50)
    iimb_id = serializers.CharField(max_length=20, default=None, allow_blank=True)
    type = serializers.CharField(max_length=20, default='user')

class SerializerLogin(serializers.Serializer):

    email = serializers.EmailField( max_length=100)
    password = serializers.CharField(max_length=50, min_length=6)