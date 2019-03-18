from rest_framework import serializers
from . import models


class UserSerializer(serializers.ModelSerializer):  # class of User Serializer
    class Meta:                          # gives the information about the User serializer
        model = models.Profile
        fields = ('email', 'username',)  # fields of a email and username
