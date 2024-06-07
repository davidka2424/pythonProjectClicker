from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from backend.forms import UserForm
from backend.models import Core, Boost
from backend.serializers import CoreSerializer, BoostSerializer


class Register(APIView):
    def get(self, request):
        form = UserForm()
        return render(request, 'registration.html', {'form': form})

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            core = Core(user=user)  # Создаем экземпляр класса Core и пихаем в него модель юзера
            core.save()  # Сохраняем изменения в базу
            return redirect('index')

        return render(request, 'registration.html', {'form': form})


class Login(APIView):
    form = UserForm()

    def get(self, request):
        return render(request, 'login.html', {'form': self.form})

    def post(self, request):
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            return redirect('index')
        return render(request, 'login.html', {'form': self.form, 'invalid': True})

@api_view(['GET'])
@login_required
def call_click(request):
    core = Core.objects.get(user=request.user)
    is_levelup = core.click()  # Труе если буст создался
    if is_levelup:
        Boost.objects.create(core=core, price=core.coins, power=core.level * 2)  # Создание буста
    core.save()

    return Response({'core': CoreSerializer(core).data, 'is_levelup': is_levelup})

@api_view(['GET'])
@login_required
def buy_boost(request, id):
    core = Core.objects.get(user=request.user)
    boost = Boost.objects.get(id=id)
    if core.coins > 0:
        core.click_power += boost.power
        core.coins -= boost.price
        core.save()
        return Response({'coins': core.coins})
    return Response("Not enough money", status=400)

@login_required
def index(request):
    core = Core.objects.get(user=request.user)  # Получаем объект игры текущего пользователя
    boosts = Boost.objects.filter(core=core).all()

    return render(request, 'index.html', {
        'core': core,
        'boosts': boosts
    })

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


class BoostViewSet(ModelViewSet):
    queryset = Boost.objects.all()
    serializer_class = BoostSerializer

    # Переопределение метода get_queryset для получения бустов, привязанных к определенному ядру
    def get_queryset(self):
        core = Core.objects.get(user=self.request.user)  # Получение ядра пользователя
        boosts = Boost.objects.filter(core=core)  # Получение бустов ядра
        return boosts

    def partial_update(self, request, pk):
        coins = request.data['coins']  # Получаем количество монет из тела запроса.
        boost = self.queryset.get(pk=pk)

        is_levelup = boost.levelup(
            coins)  # Передадим количество монет в метод. Этот метод мы скоро немного подкорректируем.
        if not is_levelup:
            return Response({"error": "Не хватает денег"})
        old_boost_stats, new_boost_stats = is_levelup

        return Response({
            "old_boost_stats": self.serializer_class(old_boost_stats).data,
            "new_boost_stats": self.serializer_class(new_boost_stats).data,
        })


@api_view(['POST'])
def update_coins(request):
    coins = request.data['current_coins']  # Значение current_coins будем присылать в теле запроса.
    core = Core.objects.get(user=request.user)

    is_levelup, boost_type = core.set_coins(
        coins)  # Метод set_coins скоро добавим в модель. Добавили boost_type для создания буста.

    # Дальнейшая логика осталась прежней, как в call_click
    if is_levelup:
        Boost.objects.create(core=core, price=core.coins, power=core.level * 2,
                             type=boost_type)  # Создание буста. Добавили атрибут type.
    core.save()

    return Response({
        'core': CoreSerializer(core).data,
        'is_levelup': is_levelup,
    })


@api_view(['GET'])
def get_core(request):
    core = Core.objects.get(user=request.user)
    return Response({'core': CoreSerializer(core).data})