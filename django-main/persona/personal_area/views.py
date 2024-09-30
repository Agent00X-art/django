from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
import random, requests, os
from datetime import datetime
from django.conf import settings
import uuid

from .models import PersonalData, Message, CreateGiftCard, CreateLoyaltyCard
from .serializer import PersonalDataSerializer, PhoneCode_ValidationSend, PhoneCode_Validate, DialogCreate, MessagesSerializer
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

class GetOnePersonalView(APIView): # запросы для персональных данных
    def get(self, request):
        personal = get_object_or_404(PersonalData.objects.filter(Phone=request.data['Phone']).values())
        return Response({"Personals": personal}) # вывели получившуюся форму

class PersonalDataView(APIView): # запросы для персональных данных
    def get(self, request):
        personals = PersonalData.objects.all() # собрали данные с модели
        serializerPerson = PersonalDataSerializer(personals, many=True) # создали форму для вывода
        return Response({"Personals": serializerPerson.data}) # вывели получившуюся форму

    def post(self, request):
        personal = request.data
        serializerPerson = PersonalDataSerializer(data=personal)
        if serializerPerson.is_valid(raise_exception=True):
            loca = requests.get(
                'https://maps.googleapis.com/maps/api/geocode/json?address=' + str(serializerPerson.validated_data[
                                                                                       'Location']) + '&key=AIzaSyBpN6a2q-0Dv9YUp-RfcE-gr2R33KFXLe4').json()[
                'results'][0]['geometry']['location']
            # serializerPerson.validated_data['Location'] = str(loca['lat']) + ', ' + str(loca['lng'])
            password = serializerPerson.validated_data.get('password')
            serializerPerson.validated_data['password'] = make_password(password)
            new_user = serializerPerson.save()
            return Response({"success": "Personals '{}' created successfully".format(new_user.email)})

    def put(self, request, pk):
        saved_personal = get_object_or_404(PersonalData.objects.filter(Phone=pk))
        ListPersonal = get_object_or_404(PersonalData.objects.filter(Phone=pk).values())
        data = request.data
        serializer = PersonalDataSerializer(instance=saved_personal, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            loca = requests.get(
                'https://maps.googleapis.com/maps/api/geocode/json?address=' + str(serializer.validated_data[
                                                                                       'Location']) + '&key=AIzaSyBpN6a2q-0Dv9YUp-RfcE-gr2R33KFXLe4').json()[
                'results'][0]['geometry']['location']
            if str(data['Avatar']) != '':
                os.remove(str(settings.BASE_DIR) + '/' + str(ListPersonal['Avatar']))
            # serializer.validated_data['Location'] = str(loca['lat']) + ', ' + str(loca['lng'])
            password = serializer.validated_data.get('password')
            serializer.validated_data['password'] = make_password(password)
            personal_saved = serializer.save()
        return Response({
            "success": "Personals '{}' updated successfully".format(personal_saved.Phone)
        })

    def delete(self, request, pk):
        ListPersonal = get_object_or_404(PersonalData.objects.filter(Phone=pk).values())
        os.remove(str(settings.BASE_DIR) + '/' + str(ListPersonal['Avatar']))
        PersonalData.objects.filter(Phone=pk).delete() # выбрали необходимый объект и сразу удалили его
        return Response({
            "message": "Personals with id `{}` has been deleted.".format(pk) # вывели сообщение об удалении
        }, status=204)

class PhoneCode_ValidationSendView(APIView): # запросы для персональных данных
    def get(self, request):
        personals = PersonalData.objects.all() # собрали данные с модели
        serializerPerson = PhoneCode_ValidationSend(personals, many=True) # создали форму для вывода
        return Response({"Personals": serializerPerson.data}) # вывели получившуюся форму

    def put(self, request, pk):
        saved_personal = get_object_or_404(PersonalData.objects.filter(Phone=pk))
        data = request.data
        serializer = PhoneCode_ValidationSend(instance=saved_personal, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            code = ''
            for i in range(4):
                code += str(random.randint(0, 9))
            saved_personal.PhoneCode = code
            message = 'Код+подтверждения+для+Persona:+'+code
            msgtok = 'AE3867AA-436F-A761-7257-85F5FC9031F8'
            requests.get(str('https://sms.ru/sms/send?api_id='+msgtok+'&to='+str(data['Phone'])+'&msg='+message+'&json=1')).json()
            saved_personal = serializer.save()
            return Response({
                "success": "Code is send to '{}':".format(saved_personal.Phone)
            })
        else:
            return Response({
                "failed": "Code is no sent to '{}'".format(saved_personal.Phone)
            })

class PhoneCode_ValidateView(APIView): # запросы для персональных данных

    def put(self, request, pk):
        saved_personal = get_object_or_404(PersonalData.objects.filter(Phone=pk))
        data = request.data
        serializer = PhoneCode_Validate(instance=saved_personal, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            if saved_personal.PhoneCode == str(data['PhoneCode']):
                Password = str(uuid.uuid4())[0:8]
                message = 'Пароль+для+входа+на+Persona:+' + str(Password)
                msgtok = 'AE3867AA-436F-A761-7257-85F5FC9031F8'
                requests.get(str('https://sms.ru/sms/send?api_id=' + msgtok + '&to=' + str(
                    data['Phone']) + '&msg=' + message + '&json=1')).json()
                saved_personal.password = make_password(Password)
                saved_personal.PhoneValidate = True
                serializer.save()
                saved_personal.PhoneCode = ''
                saved_personal.save()
                return Response({
                    "success": "На номер '{}' был отправлен пароль.".format(saved_personal.Phone)
                })
            else:
                saved_personal.PhoneCode = ''
                saved_personal.save()
                return Response({
                    "failed": "Phone '{}' is not validate. Please, try again.".format(saved_personal.Phone)
                })
        else:
            return Response({
                "error": "Phone '{}'. Please, try again.".format(saved_personal.Phone)
            })

class LoginView(APIView): # запросы для персональных данных
    def post(self, request):
        try:
            m = PersonalData.objects.get(email=request.POST['email'])
            if m.check_password(request.POST['password']):
                request.session['Phone'] = m.Phone
                return Response("Вы авторизованы.")
            else:
                return Response("Ваши логин и пароль не соответствуют.")
        except:
            return Response("Ваши логин и пароль не соответствуют.")

class LogoutView(APIView):
    def post(self, request):
        try:
            del(request.session['Phone'])
        except:
            pass
        return Response("Вы вышли.")

class EmailSendCode(APIView):

    def post(self, request):
        saved_personal = get_object_or_404(PersonalData.objects.filter(email=request.data['email']))
        msg = MIMEMultipart()

        code = ''
        for i in range(4):
            code += str(random.randint(0, 9))
        saved_personal.EmailCode = code
        saved_personal.save()
        message = 'Код подтверждения для Persona: ' + code
        # setup the parameters of the message
        password = "J0RttyGk4eVkeMSTZLv3"
        msg['From'] = "test_for_sendcode@mail.ru"
        msg['To'] = str(request.data['email'])
        msg['Subject'] = "Код подтверждения для persona"

        # add in the message body
        msg.attach(MIMEText(message, 'plain'))

        # create server
        server = smtplib.SMTP('smtp.mail.ru:587')

        server.starttls()

        # Login Credentials for sending the mail
        server.login(msg['From'], password)

        # send the message via the server.
        server.sendmail(msg['From'], msg['To'], msg.as_string())

        server.quit()
        return Response('Код отправлен')

class EmailCodeValidate(APIView):
    def post(self, request):
        saved_personal = get_object_or_404(PersonalData.objects.filter(email=request.data['email']))
        code = request.data['code']
        if saved_personal.EmailCode == code:
            msg = MIMEMultipart()
            Password = str(uuid.uuid4())[0:8]
            message = 'Пароль для входа на Persona: ' + str(Password)
            # setup the parameters of the message
            password = "J0RttyGk4eVkeMSTZLv3"
            msg['From'] = "test_for_sendcode@mail.ru"
            msg['To'] = str(request.data['email'])
            msg['Subject'] = "Пароль для persona"
            # add in the message body
            msg.attach(MIMEText(message, 'plain'))
            # create server
            server = smtplib.SMTP('smtp.mail.ru:587')
            server.starttls()
            # Login Credentials for sending the mail
            server.login(msg['From'], password)
            # send the message via the server.
            server.sendmail(msg['From'], msg['To'], msg.as_string())
            server.quit()
            saved_personal.EmailValidate = True
            saved_personal.EmailCode = ''
            saved_personal.password = make_password(Password)
            saved_personal.save()
            return Response({
                "success": "На email '{}' был отправлен пароль.".format(saved_personal.email)
            })
        else:
            saved_personal.EmailCode = ''
            saved_personal.save()
            return Response({
                "failed": "Email '{}' is not validate. Please, try again.".format(saved_personal.email)
            })

class DialogCreateView(APIView):
    def post(self, request):
        message = request.data
        messages = list(request.data.values())
        serializerMessage = DialogCreate(data=message)
        if serializerMessage.is_valid(raise_exception=True):
            serializerMessage.validated_data['IdChat'] = request.data['FirstPhone'] + request.data['SecondPhone']
            serializerMessage.save()
            return Response('True')

class MessageViews(APIView):
    def get(self, request, pk):
        saved_personal = get_object_or_404(Message.objects.filter(IdChat=pk).values())
        return Response({"IdChat": saved_personal.values()})

    def post(self, request, pk):
        message = request.data
        messages = list(request.data.values())
        saved_personal = get_object_or_404(Message.objects.filter(IdChat=pk))
        serializerMessage = MessagesSerializer(instance=saved_personal, data=message, partial=True)
        if serializerMessage.is_valid(raise_exception=True):
            serializerMessage.validated_data['Chat'] = str(saved_personal.Chat) + str(datetime.now())[:19] + str('\n') + request.data['FirstPhone'] + str('\n') + request.data['Chat'] + str('\n')
            serializerMessage.save()
        return Response({"message": "Send message in `{}` successfully.".format(saved_personal.IdChat)})

class GetChatsViews(APIView):
    def get(self, request):
        list_chats = list(Message.objects.filter(FirstPhone=request.data['FirstPhone']).values())
        list_chats += list(Message.objects.filter(SecondPhone=request.data['FirstPhone']).values())
        return Response(list_chats)

class CreateLoyaltyCardView(APIView):

    def get(self, request):
        return Response(CreateLoyaltyCard.objects.all().values())

    def post(self, request):
        if 'Phone' in request.data:
            try:
                newid = str(int(CreateLoyaltyCard.objects.order_by('IdCard').values().reverse()[0]['IdCard'])+1)[::-1]
                while len(newid) < 16:
                    newid += str(0)
                code = ''
                for i in range(4):
                    code += str(random.randint(0, 9))
                CreateLoyaltyCard.objects.create(IdCard=newid[::-1], Phone=request.data['Phone'], PIN=code)
                message = 'PIN+от+вашей+карты+лояльности+Persona:+' + str(code)
                msgtok = 'AE3867AA-436F-A761-7257-85F5FC9031F8'
                requests.get(str('https://sms.ru/sms/send?api_id=' + msgtok + '&to=' + str(
                    request.data['Phone']) + '&msg=' + message + '&json=1')).json()
                return Response('Карта лояльности с номером: '+str(newid[::-1])+' создана.')
            except:
                code = ''
                for i in range(4):
                    code += str(random.randint(0, 9))
                CreateLoyaltyCard.objects.create(Phone=request.data['Phone'], PIN=code)
                message = 'PIN+от+вашей+карты+лояльности+Persona:+' + str(code)
                msgtok = 'AE3867AA-436F-A761-7257-85F5FC9031F8'
                requests.get(str('https://sms.ru/sms/send?api_id=' + msgtok + '&to=' + str(
                    request.data['Phone']) + '&msg=' + message + '&json=1')).json()
                return Response('Карта лояльности с номером: ' + str(CreateLoyaltyCard.objects.all().values().reverse()[0]['IdCard']) + ' создана.')
        else:
            return Response('Неверно указаны аргументы')

class CreateGiftCardView(APIView):

    def get(self, request):
        return Response(CreateGiftCard.objects.all().values())

    def post(self, request):
        if 'Phone' in request.data and 'email' in request.data:
            try:
                newid = str(int(CreateGiftCard.objects.order_by('IdCard').values().reverse()[0]['IdCard'])+1)[::-1]
                while len(newid) < 16:
                    newid += str(0)
                code = ''
                for i in range(4):
                    code += str(random.randint(0, 9))
                CreateGiftCard.objects.create(IdCard=newid[::-1], Phone=request.data['Phone'], PIN=code, email=request.data['email'])
                message = 'PIN+от+вашей+подарочной+карты+Persona:+' + str(code)
                msgtok = 'AE3867AA-436F-A761-7257-85F5FC9031F8'
                requests.get(str('https://sms.ru/sms/send?api_id=' + msgtok + '&to=' + str(
                    request.data['Phone']) + '&msg=' + message + '&json=1')).json()
                msg = MIMEMultipart()
                message = 'Номер подарочной карты Persona: ' + str(newid[::-1])
                # setup the parameters of the message
                password = "J0RttyGk4eVkeMSTZLv3"
                msg['From'] = "test_for_sendcode@mail.ru"
                msg['To'] = str(request.data['email'])
                msg['Subject'] = "Подарочная карта Persona"
                # add in the message body
                msg.attach(MIMEText(message, 'plain'))
                # create server
                server = smtplib.SMTP('smtp.mail.ru:587')
                server.starttls()
                # Login Credentials for sending the mail
                server.login(msg['From'], password)
                # send the message via the server.
                server.sendmail(msg['From'], msg['To'], msg.as_string())
                server.quit()
                return Response('Подарочная карта с номером: '+str(newid[::-1])+' создана.')
            except:
                code = ''
                for i in range(4):
                    code += str(random.randint(0, 9))
                CreateGiftCard.objects.create(Phone=request.data['Phone'], PIN=code, email=request.data['email'])
                message = 'PIN+от+вашей+подарочной+карты+Persona:+' + str(code)
                msgtok = 'AE3867AA-436F-A761-7257-85F5FC9031F8'
                requests.get(str('https://sms.ru/sms/send?api_id=' + msgtok + '&to=' + str(
                    request.data['Phone']) + '&msg=' + message + '&json=1')).json()
                msg = MIMEMultipart()
                message = 'Номер подарочной карты Persona: ' + str('0000000000000001')
                # setup the parameters of the message
                password = "J0RttyGk4eVkeMSTZLv3"
                msg['From'] = "test_for_sendcode@mail.ru"
                msg['To'] = str(request.data['email'])
                msg['Subject'] = "Подарочная карта Persona"
                # add in the message body
                msg.attach(MIMEText(message, 'plain'))
                # create server
                server = smtplib.SMTP('smtp.mail.ru:587')
                server.starttls()
                # Login Credentials for sending the mail
                server.login(msg['From'], password)
                # send the message via the server.
                server.sendmail(msg['From'], msg['To'], msg.as_string())
                server.quit()
                return Response('Подарочная карта с номером: ' + str(CreateGiftCard.objects.all().values().reverse()[0]['IdCard']) + ' создана.')
        else:
            return Response('Неверно указаны аргументы')

# Create your views here.
