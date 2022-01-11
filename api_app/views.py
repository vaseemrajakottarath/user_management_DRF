import re
from typing import ContextManager
from django.shortcuts import render
from rest_framework import response
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.views import APIView
from .serializers import UserDataSerializer, UserRegister
from rest_framework.parsers import FormParser, MultiPartParser
from .models import Account
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAdminUser
from rest_framework import generics
from rest_framework import mixins,serializers,status
# Create your views here.
from django.http.response import Http404








# @api_view(['POST', ])
# @parser_classes([MultiPartParser,FormParser])
# def RegisterView(request):
#     if request.method == 'POST':
#         serializer = UserRegister(data=request.data)

#         data = {}

#         if serializer.is_valid(raise_exception=True):
#             reg = serializer.save()
            
#             data['response'] = "Registered Successfully"
#             data['name'] = reg.name
#             data['phone_number'] = reg.phone_number
#             data['email'] = reg.email
#             data['date_of_birth'] = reg.date_of_birth
#             # data['profile_picture'] = reg.profile_picture
            
#             refresh = RefreshToken.for_user(reg)
#             data['token'] = {
#                                 'refresh': str(refresh),
#                                 'access': str(refresh.access_token),
#                             }
#         else:   
#             data = serializer.errors
#         return Response(data) 


class RegisterView(generics.CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = UserRegister
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        user=serializer.save()
        return Response({"user": UserRegister(user,context=self.get_serializer_context()).data,
        "message":" Reistered Successfully"})


class UsersList(APIView):
    permission_classes=[IsAdminUser]
    def get(self,request):
        users_list=Account.objects.all()
        serializer=UserDataSerializer(users_list,many=True)
        return Response(serializer.data)

class UserDetails(APIView):
    permission_classes=[IsAdminUser]
    def get(self,request,pk):
        user=Account.objects.get(pk=pk)
        serializer=UserDataSerializer(user)
        return Response(serializer.data)

    def put(self,request,pk):
        user=Account.objects.get(pk=pk)
        serializer=UserDataSerializer(user,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'User data updated successfullly'})
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        
        user=Account.objects.get(pk=pk)
        user.delete()
        return Response({'message':'Deleted Successfully'})



