from django.urls import path

from api import views

notes_list = views.NoteViewSet.as_view({
    'get': 'list', # получить список всех заметок
    'post': 'create', # создать заметку
})
notes_detail = views.NoteViewSet.as_view({
    'get': 'retrieve', # получить данные об одной заметке
    'put': 'update', # обновить все поля заметки
    'patch': 'partial_update', # обновить несколько полей заметки
    'delete': 'destroy' # ремувнуть, уничтожить, удалить, разрушить, зарезать заметку
})

urlpatterns = [
    path('notes_viewset/', notes_list, name='notes_viewset'),
    path('notes_viewset/<int:pk>/', notes_detail, name='notes_viewset'),
    path('note/', views.NoteView.as_view(), name='note'),
    path('reg/', views.Register.as_view(), name='reg')
]