from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
import os, requests, time, re, requests
from transliterate import translit
from .models import Product, condition, Type4Heavy, price, style, typeof, size, color
from .serializer import ProductSerializer
from django.conf import settings

class AllProductView(APIView):

    def get(self, request):
        List = Product.objects.all().values()
        return Response(List)

class SortAll(APIView):

    def get(self, request):
        try:
            lookup = request.data['sort_by']
            products = Product.objects.all()
            if 'From' in request.data and 'To' in request.data:
                up = lookup+'__gt'
                low = lookup+'__lt'
                products = products.filter(**{up: request.data['From']})
                products = products.filter(**{low: request.data['To']})
            else:
                products = products.filter(**{lookup: request.data['key']})
            if request.data['Price'] == 'False':
                return Response(products.values())
            elif request.data['Price'] == 'True' and request.data['reverse'] == 'True':
                sorted = products.order_by('Price').values()
                return Response(sorted.reverse())
            elif request.data['Price'] == 'True' and request.data['reverse'] == 'False':
                sorted = products.order_by('Price').values()
                return Response(sorted)
            else:
                return Response('Неправильно указаны аргументы сортировки')
        except:
            return Response('Неправильно указаны аргументы')


class TopView(APIView):

    def get(self, request):
        ListTop = list(Product.objects.filter(Top=True).values())
        return Response(ListTop)

class ListUsr(APIView):

    def get(self, request):
        List = Product.objects.filter(Phone=request.data['Phone'])
        return Response(List.values())
# Create your views here.

class Product(APIView): # запросы для персональных данных
    def get(self, request, pk):

        AdsList = get_object_or_404(Product.objects.filter(IdProduct=request['ID']).values())
        return Response({"AdsList": AdsList}) # вывели получившуюся форму

    def post(self, request):
        countPhotos = 0
        personal = request.data
        serializerAd = ProductSerializer(data=personal)
        if serializerAd.is_valid(raise_exception=True):
            for c in range(1, 9):
                if str('Photo_' + str(c)) in personal:
                    countPhotos += 1
                    serializerAd.validated_data[str('Photo_' + str(countPhotos))] = personal[
                        str('Photo_' + str(c))]
        if serializerAd.is_valid(raise_exception=True):
            serializerAd.validated_data['IdProduct'] = (re.sub(r'(?i)[^a-z]', '_', translit(str(serializerAd.validated_data.get('HeaderAd')), language_code='ru', reversed=True))).replace('__', '_') + '_' + str(serializerAd.validated_data.get('Phone'))
            loca = requests.get(
                'https://maps.googleapis.com/maps/api/geocode/json?address='+str(serializerAd.validated_data['Location'])+'&key=AIzaSyBpN6a2q-0Dv9YUp-RfcE-gr2R33KFXLe4').json()[
                'results'][0]['geometry']['location']
            serializerAd.validated_data['Location'] = str(loca['lat']) + ', ' + str(loca['lng'])
            adSaved = serializerAd.save()
            CarAds.objects.filter(IdAd=adSaved.IdAd).update(
                category=Category.objects.get(title=request.data['category']))
        return Response({"success": "AdsList '{}' created successfully".format(adSaved.IdAd)})

    def put(self, request, pk):
        countPhotos = 0
        saved_personal = get_object_or_404(Product.objects.filter(IdProduct=pk))
        ListCarAds = get_object_or_404(Product.objects.filter(IdProduct=pk).values())
        data = request.data
        serializer = ProductSerializer(instance=saved_personal, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            loca = requests.get(
                'https://maps.googleapis.com/maps/api/geocode/json?address=' + str(
                    serializer.validated_data['Location']) + '&key=AIzaSyBpN6a2q-0Dv9YUp-RfcE-gr2R33KFXLe4').json()[
                'results'][0]['geometry']['location']
            serializer.validated_data['Location'] = str(loca['lat']) + ', ' + str(loca['lng'])
            if str(data).count('Photo') >= 3:
                for c in range(1, 9):
                    try:
                        os.remove(str(settings.BASE_DIR) + '/' + str(ListCarAds['Photo_' + str(c)]))
                    except:
                        pass
                for c in range(1, 9):
                    if str('Photo_' + str(c)) in data:
                        countPhotos += 1
                        serializer.validated_data[str('Photo_' + str(countPhotos))] = data[
                            str('Photo_' + str(c))]
            serializer.validated_data['IdProduct'] = (re.sub(r'(?i)[^a-z]', '_',
                                                        translit(str(serializer.validated_data.get('HeaderAd')),
                                                                 language_code='ru', reversed=True))).replace('__',
                                                                                                              '_') + '_' + str(
                serializer.validated_data.get('Phone'))
            adSaved = serializer.save()
        return Response({
            "success": "AdsList '{}' updated successfully".format(adSaved.IdAd)
        })

    def delete(self, request, pk):
        ListCarAds = get_object_or_404(Product.objects.filter(IdAd=pk).values())
        for c in range(1, 9):
            try:
                os.remove(str(settings.BASE_DIR) + '/' + str(ListCarAds['Photo_' + str(c)]))
            except:
                pass
        Product.objects.filter(IdAd=pk).delete() # выбрали необходимый объект и сразу удалили его
        return Response({
            "message": "AdsList with id `{}` has been deleted.".format(pk) # вывели сообщение об удалении
        }, status=204)

paramsnames = ['condition', 'Type4Heavy', 'price', 'style', 'typeof', 'size', 'color']
params = [condition, Type4Heavy, price, style, typeof, size, color]

class Params(APIView):
    def get(self, request):
        if request.data['Name'] in paramsnames:
            return Response(params[paramsnames.index(request.data['Name'])].objects.all().values())
        return Response('OK')

    def post(self, request):
            try:
                if request.data['Name'] in paramsnames:
                    params[paramsnames.index(request.data['Name'])].objects.create(value = request.data['title'].values())
            except:
                return Response('Не добавлено')
            return Response('Создано')
    def delete(self, request):
        try:
            params[paramsnames.index(request.data['Name'])].objects.get(value = request.data['title']).delete()
            return Response('Удалено')
        except:
            return Response('Невозможно удалить')
