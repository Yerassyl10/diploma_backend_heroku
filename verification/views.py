from datetime import datetime
from .models import emailModel
import base64
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
import pyotp
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from accounts.models import Users

class generateKey:
    @staticmethod
    def returnValue(email):
        return str(email) + str(datetime.date(datetime.now())) + "Some Random Secret Key"


class getPhoneNumberRegistered(APIView):
    @staticmethod
    def get(request, email):
        try:
            emailV = emailModel.objects.get(email=email)
        except ObjectDoesNotExist:
            emailModel.objects.create(
                email=email,
            )
            emailV = emailModel.objects.get(email=email)
        emailV.counter += 1
        emailV.save()
        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(email).encode())
        OTP = pyotp.HOTP(key)
        print(OTP.at(emailV.counter))
        subject = "OTP from IT-HUNT"
        message = OTP.at(emailV.counter)
        send_mail(subject, message,
                  'daniyarbekuly@gmail.com', [email])

        return Response({"OTP": OTP.at(emailV.counter)}, status=200)



    @staticmethod
    def post(request, email):
        try:
            emailV = emailModel.objects.get(email=email)
        except ObjectDoesNotExist:
            return Response("Wrong email", status=404)
        err = None
        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(email).encode())
        OTP = pyotp.HOTP(key)
        if OTP.verify(request.data["otp"], emailV.counter):
            emailV.isVerified = True
            emailV.save()
            try:
                account = Users.objects.get(email=email)
                token = Token.objects.get_or_create(user=account)[0].key
                return Response({
                    "Token": token},
                    status=200)
            except BaseException:
                responseBody = {"data": err, "error": "User not found!!!"}
                return Response(responseBody)

        return Response("OTP is wrong", status=400)
