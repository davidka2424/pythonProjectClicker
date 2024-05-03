from rest_framework.serializers import ModelSerializer
from .models import Core


class CoreSerializer(ModelSerializer):
    class Meta:
        model = Core
        fields = ['coins', 'click_power']

    def click(self):
        self.coins += self.click_power
        return self

