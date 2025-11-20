from django.shortcuts import render


def home(request):
    return render(request, "home.html")


def places(request):
    # Point to the namespaced template under templates/pages
    return render(request, "pages/places.html")


def products(request):
    return render(request, "pages/products.html")


def saved(request):
    return render(request, "pages/saved.html")


def blog(request):
    return render(request, "pages/blog.html")


def help_center(request):
    return render(request, "pages/help.html")


def contact(request):
    return render(request, "pages/contact.html")


def sign_in(request):
    return render(request, "pages/signin.html")


def get_started(request):
    return render(request, "pages/get_started.html")
