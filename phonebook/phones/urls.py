from django.urls import path
from . import views

app_name = 'phones'
urlpatterns = [
    path('create/', views.create_entry, name='create'),
    path('find/', views.find_entry, name='find'),
    path('search/', views.show_search_form, name='search'),
    path('', views.show_add_entry_form, name='show-add-entry-form'),
]
