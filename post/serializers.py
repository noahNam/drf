from rest_framework import serializers

from .models import *


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('__all__')  # 전부 serialize 할 때
        # fields = ('title', 'content')
