from copy import copy

from django.contrib.auth.models import User
from django.db import models


from .constants import *



# Create your models here.
class Core(models.Model):
    auto_click_power = models.IntegerField(default=0)

    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE)
    coins = models.IntegerField(default=0)
    click_power = models.IntegerField(default=1)
    level = models.IntegerField(default=1)  # От уровня зависит количество бустов

    def click(self):
        self.coins += self.click_power

        if self.coins >= self.check_level_price():  # Проверка на достаточное количество монет
            self.level += 1  # для создания буста

            return True  # Труе если буст создался
        return False  # Фалсе если буст не создался

    def check_level_price(self):  # Функция вычисления количества монет для повышения уровня
        return (self.level ** 3) * 10  # Формулу можно поменять в зависимости от баланса игры

    # Метод для установки текущего количества монет пользователя.
    def set_coins(self, coins, commit=True):
        self.coins = coins # Теперь мы просто присваиваем входящее значение монет.
        is_levelupdated = self.is_levelup() # Проверка на повышение уровня.
        boost_type = self.get_boost_type() # Получение типа буста, который будет создан при повышении уровня.

        if is_levelupdated:
            self.level += 1

        if commit:
            self.save()

        return is_levelupdated, boost_type

    # Выделили проверку на повышение уровня в отдельный метод для чистоты кода.
    def is_levelup(self):
        return self.coins >= self.calculate_next_level_price()

    # Выделили получение типа буста в отдельный метод для удобства.
    def get_boost_type(self):
        boost_type = 0
        if self.level % 3 == 0:
            boost_type = 1
        return boost_type

    # Поменяли название с check_level_price, потому что теперь так гораздо больше подходит по смыслу.
    def calculate_next_level_price(self):
        return self.level**2 * 127


class Boost(models.Model):
    type = models.PositiveSmallIntegerField(default=0, choices=BOOST_TYPE_CHOICES)

    core = models.ForeignKey(Core, null=False, on_delete=models.CASCADE)
    level = models.IntegerField(default=0)
    price = models.IntegerField(default=10)
    power = models.IntegerField(default=1)

    def levelup(self, current_coins):
        if self.price > current_coins:
            return False

        old_boost_values = copy(self)

        self.core.coins = current_coins - self.price
        self.core.click_power += self.power * BOOST_TYPE_VALUES[self.type][
            'click_power_scale']  # Умножаем силу клика на константу.
        self.core.auto_click_power += self.power * BOOST_TYPE_VALUES[self.type][
            'auto_click_power_scale']  # Умножаем силу автоклика на константу.
        self.core.save()

        self.level += 1
        self.power *= 2
        self.price = self.price * BOOST_TYPE_VALUES[self.type]['price_scale']  # Умножаем ценник на константу.
        self.save()

        return old_boost_values, self