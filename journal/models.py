from django.db import models
from django.contrib.auth.models import User
from shops.models import CoffeeShop, MenuItem

class JournalEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="journal_entries")
    shop = models.ForeignKey(CoffeeShop, on_delete=models.CASCADE, related_name="journal_entries")
    item = models.ForeignKey(MenuItem, null=True, blank=True, on_delete=models.SET_NULL)
    visit_date = models.DateField()
    my_rating = models.IntegerField()    # 1..5
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def summary(self) -> str:
        return f"{self.shop.name} on {self.visit_date} — {self.my_rating}/5"

    def short_notes(self, length:int=80) -> str:
        return (self.notes or "")[:length]
