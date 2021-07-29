import itertools

from django.contrib.auth import logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.management import BaseCommand
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.views.generic import UpdateView, ListView
from rest_framework import generics

from . import forms, models
from . import serializers
from .models import Entry
from .serializers import LoginSerializer


@csrf_exempt
@login_required
def create_entry(request):
    """
    Creates an entry via AJAX
    """
    form_instance = forms.EntryForm(data=request.POST)
    if form_instance.is_valid():
        form_instance.instance.creator = request.user
        form_instance.save()
        return render(request, 'phones/show_all.html')


@csrf_exempt
@require_GET
@login_required
def show_add_entry_form(request):
    """
    Show the add entry form page
    """
    return render(request, 'phones/add_entry.html', {
        'form': forms.EntryForm(),
    })


@login_required
def show_all_number(request):
    if request.user.is_authenticated:
        my_number = models.Entry.objects.filter(creator=request.user)
        other_number = []
        qs = list(itertools.chain(my_number, other_number))
        paginated = Paginator(qs, 4)
        paginated_page = paginated.get_page(request.GET.get('page', 1))
        return render(request=request,
                      context={
                          'object_list': paginated_page,
                          'page_obj': 'paginated',
                          'page_title': 'Show all posts'
                      },
                      template_name='phones/show_all.html'
                      )
    else:
        reverse_lazy('phones:login')


@require_GET
@login_required()
def show_search_form(request):
    """
    Show the search form page
    """
    return render(request, 'phones/search.html')


# class find (generic.view):
#     @method_decorator(login_required)
#     def get(self,*args,**kwargs):
#         pass
#     based view for find_entry

@login_required(login_url='/phones/login/')
def find_entry(request):
    """
    Finds a phonebook entry
    """
    phone_number = request.GET.get('phonenum', None)
    mode_search = request.GET.get('mode_search', None)

    if not phone_number:
        return JsonResponse({'success': False, 'error': 'No number specified.'}, status=200)
    if phone_number:
        if mode_search == 'contain':
            qs = Entry.objects.filter(phone_number__contains=phone_number, creator=request.user)
        elif mode_search == 'end-with':
            qs = Entry.objects.filter(phone_number__endswith=phone_number, creator=request.user)
        elif mode_search == 'start-with':
            qs = Entry.objects.filter(phone_number__startswith=phone_number, creator=request.user)
        else:
            qs = Entry.objects.filter(phone_number=phone_number, creator=request.user)

    return JsonResponse(
        {
            'results': list(
                qs.values()
            ),
            'count': qs.count()
        },

    )


class AdminLogin(LoginView):
    template_name = 'LoginView_form.html'
    success_url = reverse_lazy('phones:home')


class EditPhone(UpdateView, LoginRequiredMixin):
    model = Entry
    fields = (
        'name',
        'last_name',
        'phone_number',
    )
    template_name = 'phones/entry_form.html'
    success_url = reverse_lazy('phones:show_all_number')


"""
Rest 
"""


class ListPhonebook(generics.ListAPIView):
    """
    rest view for phonebook
    """
    queryset = models.Entry.objects.all()
    serializer_class = serializers.ProductSerializer


def show_home_page(request):
    """
    Show the search form page
    """
    return render(request, 'phones/homepage.html')


def logout_view(request):
    logout(request)
    return render(request, 'phones/homepage.html')


# class EditProfile(LoginRequiredMixin, generic.UpdateView):
#     model = Entry
#     form_class = forms.ProfileFrom
#     template_name = 'phones/edit_profile.html'
#     success_url = reverse_lazy('phones:home')


class EditProfile(LoginRequiredMixin, UpdateView):
    """
    Updates a user profile
    """
    model = get_user_model()
    fields = (
        'first_name',
        'last_name',
        'email'
    )
    template_name = 'phones/edit_profile.html'
    success_url = reverse_lazy('phones:home')

    def get_object(self, queryset=None):
        return self.request.user


class Command(BaseCommand):
    pass
    # def handle(self, *args, **kwargs):
    #
    #
    #     self.items = []
    #
    #     for arg in args:
    #         app_label, model, ids = arg.split('.')
    #         Model = Entry(app_label, model)
    #         for id in ids.split(','):
    #             self.dump_object(Model.objects.filter(pk=id))
    #
    #     serializers.serialize('json',
    #                           self.items,
    #
    #                        )


class PrintPhonebook(LoginRequiredMixin, ListView):
    model = models.Entry
    template_name = 'phones/entry_detail.html'


from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView


# class ProfileList(APIView):
#     renderer_classes = [TemplateHTMLRenderer]
#     template_name = 'phones/show_all.html'
#
#     def get(self, request):
#         if request.user.is_authenticated:
#             queryset = Entry.objects.filter(creator=request.user)
#             return Response({'profiles': queryset})


from django.shortcuts import get_object_or_404

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView


class ProfileDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'profile_detail.html'

    def get(self, request, pk):
        profile = get_object_or_404(Entry, pk=pk)
        serializer = LoginSerializer(profile)
        return Response({'serializer': serializer, 'profile': profile})

    def post(self, request, pk):
        profile = get_object_or_404(Entry, pk=pk)
        serializer = LoginSerializer(profile, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'profile': profile})
        serializer.save()
        return redirect('profile-list')
