from django.urls import path
from .views import list_entries, create_entry
urlpatterns = [ path("", list_entries), path("create", create_entry) ]
