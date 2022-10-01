from dataclasses import fields
from pyexpat import model
from django.contrib.auth.models import User
from rest_framework import serializers
from shop.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','email','password']
        extra_kwargs={
            # 'password':{'write_only':True}
        }

    def create(self, validated_data):
        password=validated_data.pop('password', None)
        user=self.Meta.model(**validated_data)
        if password is not None:
            user.set_password(password)
            user.save()
            return user 


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model= Product
        fields= '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields='__all__'