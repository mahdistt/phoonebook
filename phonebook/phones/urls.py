from django.urls import path

from . import views
from .views import AdminLogin

app_name = 'phones'
urlpatterns = [
    path('create/', views.create_entry, name='create'),
    path('find/', views.find_entry, name='find'),
    path('search/', views.show_search_form, name='search'),
    path('', views.show_add_entry_form, name='show-add-entry-form'),
    path('login/', AdminLogin.as_view(), name="login"),
    path('show/', views.show_all_number, name="show_all_number"),
]
