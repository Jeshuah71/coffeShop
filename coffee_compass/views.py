from django.shortcuts import render
from django.conf import settings


def home(request):
    return render(
        request,
        "home.html",
        {"google_maps_api_key": getattr(settings, "GOOGLE_MAPS_API_KEY", "")},
    )


def places(request):
    return render(
        request,
        "pages/places.html",
        {"google_maps_api_key": getattr(settings, "GOOGLE_MAPS_API_KEY", "")},
    )


def products(request):
    return render(request, "pages/products.html")


def saved(request):
    return render(request, "pages/saved.html")


def blog(request):
    return render(request, "pages/blog.html")

def journal_page(request):
    return render(request, "pages/journal.html")


def help_center(request):
    return render(request, "pages/help.html")


def contact(request):
    return render(request, "pages/contact.html")


def sign_in(request):
    return render(request, "pages/signin.html")

def sign_up(request):
    return render(request, "pages/signup.html")

def get_started(request):
    return render(request, "pages/get_started.html")


def catbot(request):
    return render(request, "pages/catbot.html")
