from django.shortcuts import render

# Create your views here.
from django.contrib.auth import login
from django.shortcuts import render, redirect

from rest_framework.views import APIView
from rest_framework.response import Response

from api.models import Note
from backend.forms import UserForm
from .serializers import NoteSerializer
from rest_framework import viewsets


class NoteView(APIView):
    def get(self, request):
        id = request.query_params.get("id")
        if id:
            note = Note.objects.get(pk=id)  # Получаем заметку из базы по primary key
            serializer = NoteSerializer(note)  # Засовываем заметку в сериализатор, преобразуем данные
            return Response(serializer.data)  # serializer.data вернет красивый json на фронт

        notes = Note.objects.all()  # Получаем все заметки из базы данных

        # Засовываем полученные данные в сериалайзер, чтобы
        # он автоматически превратил все данные в красивый json формат
        # и ставим аргумент many=True, чтобы он достал множество заметок, а не одну
        serializer = NoteSerializer(notes, many=True)

        return Response(serializer.data)  # serializer.data вернет красивый json на фронт

    def post(self, request):
        serializer = NoteSerializer(data=request.data)  # request.data - это данные, которые прилетают в запросе

        # Функция позволяет проверить, валидны ли данные
        if serializer.is_valid():
            note = serializer.save()  # Сохраняем в базу данных. С помощью сериализаторов это тоже можно делать
            note_serialized = NoteSerializer(
                note)  # Т.к. из базы возвращается объект, сериализуем его, чтобы вернуть на фронт
            return Response(note_serialized.data)

        return Response('Ah, shit. Here we go again')

    def put(self, request):
        id = request.data.get('id')  # Получение id из тела запроса
        if not id:
            return Response({"error": 'Нету id'})

        """
        Поиск заметки.
        Метод filter используется потому, что метод update (ниже) работает только по списку объектов.
        """
        note = Note.objects.filter(pk=id)
        if not note:
            return Response({"error": 'Нету такой заметки'})
        title = request.data.get('title')
        text = request.data.get('text')
        note.update(title=title, text=text)  # Обновление заметки

        updated_note = Note.objects.get(pk=id)  # Получение обновленной заметки
        return Response({
            "id": updated_note.id,
            "title": updated_note.title,
            "text": updated_note.text
        })

    def delete(self, request):
        id = request.query_params.get('id')  # Получение id из параметров запроса
        if not id:
            return Response({"error": 'Нету id'})
        note = Note.objects.get(pk=id)  # Получение заметки
        if not note:
            return Response({"error": 'Нету такой заметки'})
        note.delete()  # Удаление заметки

        return Response({
            "success": 'Заметка успешно удалена'
        })


# Или более реальный пример. Переписанная функция регистрации из прошлой лекции.
class Register(APIView):
    def get(self, request):
        form = UserForm()
        return render(request, 'registration.html', {'form': form})

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')

        return render(request, 'registration.html', {'form': form})


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer