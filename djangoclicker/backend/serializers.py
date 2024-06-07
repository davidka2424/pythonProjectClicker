from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from .models import Core, Boost


class CoreSerializer(ModelSerializer):
    next_level_price = SerializerMethodField() # Поле, которое соответствует вычисляемому значению.

    # Метод вычисления значения для поля next_level_price.
    def get_next_level_price(self, obj):
        return obj.calculate_next_level_price()  # obj - экземпляр модели Core.

    class Meta:
        model = Core
        fields = ['coins', 'click_power', 'auto_click_power',
                  'next_level_price', 'level']  # Не возвращаем пользователя потому что а зачем


class BoostSerializer(ModelSerializer):
    class Meta:
        model = Boost
        fields = '__all__'