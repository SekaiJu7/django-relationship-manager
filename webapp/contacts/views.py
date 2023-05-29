from django.shortcuts import render, redirect
from crmAPI import get_users, User


def index(request):
    return render(request, "contacts/index.html", {'users': get_users()})


def add_contacts(request):
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    phone_number = request.POST.get('phone_number')
    adress = request.POST.get('adress')
    user = User(fname=first_name, lname=last_name, address=adress, phone_number=phone_number)
    user.save()
    return redirect('index')


def delete_contact(request):
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    user = User(first_name, last_name)
    user.delete()

    return redirect('index')
