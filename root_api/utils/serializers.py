from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    """ serialize data """

    name = serializers.CharField(max_length=10)
