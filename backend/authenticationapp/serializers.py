from rest_framework import serializers
from .models import Player


class PlayerSerializer(serializers.ModelSerializer):
    model = Player
    fields = ['email']

