from rest_framework import serializers
from .models import Product, User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email', 'phone')
        read_only_fields = ('username', )

    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        user = User.objects.create_user(username=username, password=password, **validated_data)
        return user
    

class UserLoginSerializer(serializers.Serializer): 
    username =serializers.CharField(min_length=2, max_length=50, required=True)
    password = serializers.CharField(min_length=1, max_length=50, required=True)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'price', 'description', 'is_active')
        read_only_fields = ('id', )


# class ProductUpdatedViewSet(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = ('name', 'price', 'description', 'is_active')