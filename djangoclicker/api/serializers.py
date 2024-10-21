from rest_framework import serializers  # Имортируем модуль с сериализаторами
from .models import Note  # Импортируем модель Note

# Наследуемся от класса serializer.ModelSerializer
# Это нужно для того, чтобы в классе были доступны методы сериализаторов
class NoteSerializer(serializers.ModelSerializer):

    # Подробно об этой конструкции говорить не будем, слишком долго
    # Во внимание стоит принять то, что model - это модель, которую мы делали для базы данных
    # А fields = '__all__' означает, что мы берём абсолютно все поля из этой модели
    class Meta:
        model = Note
        fields = '__all__'