from rest_framework.decorators import api_view
from user_app.api.serializers import RegistrationSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken



@api_view(['POST'])
def registration_view(request):
    if request.method == 'POST':
        data={}
        serializer=RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            accout=serializer.save()
            #in case of normal token authentication
            token=Token.objects.create(user=accout)#there exist another automatic methods for creating token refer api guide
            data['username']=accout.username
            data['email']=accout.email
            data['response']="registration successful"
            data['token']=token.key
            
            #in case of jwt token we create access and refresh tokens and passes it to frontend
            #no need of database storing
            # refresh = RefreshToken.for_user(accout)
            # data['token']={
            #         'refresh': str(refresh),
            #         'access': str(refresh.access_token),
            #         }
            
            return Response(data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST',])
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)