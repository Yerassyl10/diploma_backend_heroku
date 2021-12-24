from django.contrib.auth import logout, login
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, generics
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.utils import json
from accounts.models import Users
from accounts.api.serilalizers import RegistrationSerializer, ChangePasswordSerializer, UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny


@csrf_exempt
@api_view(['PUT', 'DELETE', 'GET'])
@permission_classes([IsAuthenticated])
def user_profile_view(request):
    try:
        user_profile = Users.objects.get(pk=request.user.id)
    except Users.DoesNotExist as e:
        return Response({'error': str(e)})

    if request.method == 'GET':
        serializer = UserSerializer(user_profile)
        if request.user.is_authenticated:
            return Response(serializer.data)
        else:
            return Response('error')

    elif request.method == 'PUT':
        serializer = UserSerializer(instance=user_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    elif request.method == 'DELETE':
        user_profile.delete()
        return Response({'data': 'User has been deleted'})


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        d = {}
        if serializer.is_valid():
            account = serializer.save()
            d['response'] = 'You are registered successfully!!!'
            d['email'] = account.email
            token = Token.objects.get_or_create(user=account)[0].key
            d['token'] = token
        else:
            d = serializer.errors
        return Response(d)


@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
    d = {}
    err = None
    requestBody = json.loads(request.body)
    email = requestBody['email']
    password = requestBody['password']

    try:
        account = Users.objects.get(email=email)
    except BaseException:
        responseBody = {"data": err, "error": "User not found!!!"}
        return Response(responseBody)

    token = Token.objects.get_or_create(user=account)[0].key

    if not check_password(password, account.password):
        responseBody = {"data": err, "error": "Your email or password is wrong!!!"}
        return Response(responseBody)

    if account:
        if account.is_active:
            login(request, account)
            d["email"] = account.email
            d["token"] = token
            responseBody = {"data": d, "error": err}
            return Response(responseBody)



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def logout_user(request):
    request.user.auth_token.delete()
    logout(request)
    responseBody = {"data": 'User Logged out successfully'}
    return Response(responseBody)


class ChangePasswordView(generics.UpdateAPIView):
    model = Users
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        o = self.request.user
        return o

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("oldPassword")):
                return Response({"error": "Wrong password."})
            self.object.set_password(serializer.data.get("newPassword"))
            self.object.save()
            responseBody = {'data': 'Password has been updated successfully'}
            return Response(responseBody)
        return Response(serializer.errors)
