from django.contrib.auth import get_user_model
from .models import Transaction
from rest_framework import serializers,validators
User = get_user_model()
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','password']

        extra_kwargs = {
            "password":{"write_only":True},
            "email":{
                "required":True,
                "allow_blank":False,
                "validators":[
                    validators.UniqueValidator(
                        User.objects.all(),"A user with this email already exists"
                    )
                ]
            }
        }
    def create(self,validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
            
        
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id','amount','title','split_between_users']
        extra_kwargs = {
            'split_between_users':{'required':True}
        }

