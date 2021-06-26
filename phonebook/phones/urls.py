from django.urls import path

from . import views
from .views import AdminLogin, logout_view

app_name = 'phones'
urlpatterns = [
    path('create/', views.create_entry, name='create'),
    path('find/', views.find_entry, name='find'),
    path('search/', views.show_search_form, name='search'),
    path('', views.show_home_page, name='home'),
    path('add', views.show_add_entry_form, name='show-add-entry-form'),
    path('login/', AdminLogin.as_view(), name="login"),
    path('logout/', logout_view, name="logout_view"),
    path('show/', views.show_all_number, name="show_all_number"),
    path('edit/<int:pk>', views.EditPhone.as_view(), name="edit-phone"),
    path('api/v1/', views.ListPhonebook.as_view()),
    path('profile/edit/', views.EditProfile.as_view(), name='edit-profile'),

]
