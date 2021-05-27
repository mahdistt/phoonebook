from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET

from . import forms
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
    select = request.GET.get('selecttt', None)
    # if not phone_number:
    #     return JsonResponse({'success': False, 'error': 'No number specified.'}, status=400)
    if select == 1:
        qs = Entry.objects.filter(phone_number=phone_number)
    elif select == 2:
        qs = Entry.objects.filter(phone_number__startswith=phone_number)
    elif select == 3:
        qs = Entry.objects.filter(phone_number__endswith=phone_number)
    else:
        qs = Entry.objects.filter(phone_number__contains=phone_number)
    if qs:
        return JsonResponse(
            {
                'results': list(
                    qs.values()
                ),
                'count': qs.count()
            }
        )
    else:
        return JsonResponse(
            {
                'result': 'error'
            }
        )
