from django.db import models


class CoffeeShop(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=255, blank=True)
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)
    price_level = models.IntegerField(default=2)  # 1..4
    avg_rating = models.FloatField(default=0)
    rating_count = models.PositiveIntegerField(default=0)
    hours = models.CharField(max_length=200, blank=True)
    tags = models.JSONField(default=list, blank=True)  # ["quiet","wifi","cozy"]
    def __str__(self): return self.name

    def update_rating(self, new_rating: float) -> None:
        """
        Update average rating and count using a streaming formula.
        """
        count = self.rating_count or 0
        current = self.avg_rating or 0
        new_count = count + 1
        self.avg_rating = round(((current * count) + new_rating) / new_count, 2)
        self.rating_count = new_count
        self.save(update_fields=["avg_rating", "rating_count"])

class MenuItem(models.Model):
    shop = models.ForeignKey(CoffeeShop, on_delete=models.CASCADE, related_name="menu_items")
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, default="coffee")
    seasonal = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    flavor_tags = models.JSONField(default=list, blank=True)
    def __str__(self): return f"{self.name} @ {self.shop.name}"
