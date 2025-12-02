from django.urls import path
from .views import list_entries, create_entry
urlpatterns = [ path("", list_entries, name="journal_list"), path("create", create_entry, name="journal_create") ]
