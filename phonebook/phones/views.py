from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET

from . import forms, models
from .models import Entry


@csrf_exempt
@require_POST
def create_entry(request):
    """
    Creates an entry via AJAX
    """
    form_instance = forms.EntryForm(data=request.POST)
    if form_instance.is_valid():
        entry_object = form_instance.save()
        return JsonResponse(data={
            'success': True,
            'pk': entry_object.pk,
            'name': entry_object.name,
            'last_name': entry_object.last_name,
            'phone_number': entry_object.phone_number
        }, status=201)
    else:
        return JsonResponse(data={
            'success': False,
        }, status=400)


@csrf_exempt
@require_GET
def show_add_entry_form(request):
    """
    Show the add entry form page
    """
    return render(request, 'phones/add_entry.html', {
        'form': forms.EntryForm()
    })


def show_all_number(request):
    if request.user.is_authenticated:
        my_number = models.Entry.objects.filter(name=request.user)

    return render(request=request,
                  context={
                      'object_list': my_number,
                      'page_title': 'show phone book',
                  },
                  template_name='phones/show_all.html'
                  )


@require_GET
def show_search_form(request):
    """
    Show the search form page
    """
    return render(request, 'phones/search.html')


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
