from django.contrib.auth.models import User
from rest_framework import serializers




class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}},
        }

    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError('Passwords do not match')

        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError('Email already exists')

        account = User(email=self.validated_data['email'], username=self.validated_data['username'])
        account.set_password(password)
        account.save()
        return account


# class RegistrationSerializer(serializers.ModelSerializer):
#     #additional  field not in model
#     password2=serializers.CharField(write_only=True, style={'input_type': 'password'} )
                                  
#     class Meta:
#         model=User
#         fields=['username','email', 'password', 'password2']
#         #to add additional properties to fields
#         extra_kwargs={
#             'password': {'write_only': True,'style': {'input_type': 'password'}},
#             }
        
#         #overriding existing save method
#         def create(self, **kwargs):
#             password = self.validated_data['password']
#             password2 = self.validated_data['password2']

#             if password != password2:
#                 raise serializers.ValidationError('Passwords do not match')
                
               

#             if User.objects.filter(email=self.validated_data['email']).exists():
#                  raise serializers.ValidationError('Email already exists')
       

#             account = User.objects.create_user(email=self.validated_data['email'], username=self.validated_data['username'], password=password)
        
#             return account
    

        # def save(self,**kwargs):
        #     password = self.validated_data['password']
        #     password2 = self.validated_data['password2']
            
        #     if password != password2:
        #         raise serializers.ValidationError('Passwords do not match')
            
        #     if User.objects.filter(email=self.validated_data['email']).exists():
        #         raise serializers.ValidationError('Email already exists')
            
        #     account=User(email=self.validated_data['email'],username=self.validated_data['username'])
        #     account.set_password(password)
        #     account.save()
        #     return account
            