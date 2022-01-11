from rest_framework import fields, serializers
from .models import Account

    
    
class UserRegister(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model = Account
        fields = ['id','name','phone_number','email','date_of_birth','profile_picture','password','password2']
        extra_kwargs = {
            'password' : {'write_only':True}
        }
    
    def get_profile_image_url(self, obj):
        return obj.profile_picture.url
    
    def create(self,validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
    def save(self):
        reg = Account(
            email=self.validated_data['email'],
            phone_number=self.validated_data['phone_number'],
            date_of_birth=self.validated_data['date_of_birth'],
            name=self.validated_data['name'],
            profile_picture=self.validated_data['profile_picture'],
        )
        if Account.objects.filter(phone_number=self.validated_data['phone_number']).exists():
            raise serializers.ValidationError({'error':'phone number already registered!!'})
        password=self.validated_data['password']
        password2=self.validated_data['password2']
        
        if password != password2:
            raise serializers.ValidationError({'error':'password does not match!!'})
        reg.set_password(password)
        reg.save()
        return reg


class UserDataSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Account
        fields=['id','name','phone_number','email','date_of_birth','profile_picture']