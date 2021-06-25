from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.views.generic import UpdateView
from rest_framework import generics
import itertools
from django.core.paginator import Paginator

from . import forms, models
from . import serializers
from .models import Entry


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
    #     return JsonResponse(data={
    #         'success': True,
    #         'pk': entry_object.pk,
    #         'name': entry_object.name,
    #         'last_name': entry_object.last_name,
    #         'phone_number': entry_object.phone_number,
    #     }, status=201)
    # else:
    #     return JsonResponse(data={
    #         'success': False,
    #     }, status=400)


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
        other_number=[]
    # my_number = models.Entry.objects.all()
    # Combine two querysets into one list
    qs = list(itertools.chain(my_number, other_number))

    # Paginate by using pagination class
    paginated = Paginator(qs, 4)

    # Now which page are you looking for?
    paginated_page = paginated.get_page(request.GET.get('page', 1))
    return render(request=request,
                  context={
                      'object_list': paginated_page,
                      'page_obj': 'paginated',
                      'page_title': 'Show all posts'
                  },
                  template_name='phones/show_all.html'
                  )


@require_GET
def show_search_form(request):
    """
    Show the search form page
    """
    return render(request, 'phones/search.html')


@login_required(login_url='/accounts/login/')
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
            qs = Entry.objects.filter(phone_number__contains=phone_number)
        elif mode_search == 'end-with':
            qs = Entry.objects.filter(phone_number__endswith=phone_number)
        elif mode_search == 'start-with':
            qs = Entry.objects.filter(phone_number__startswith=phone_number)
        else:
            qs = Entry.objects.filter(phone_number=phone_number)

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
