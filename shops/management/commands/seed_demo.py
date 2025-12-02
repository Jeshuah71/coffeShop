from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from shops.models import CoffeeShop, MenuItem
from reviews.models import Review, Favorite
from journal.models import JournalEntry
from recommendations.models import Quote
from django.utils import timezone


class Command(BaseCommand):
    help = "Seed demo data for Coffee Compass"

    def handle(self, *args, **options):
        demo_user, _ = User.objects.get_or_create(username="demo", defaults={"email": "demo@example.com"})
        demo_user.set_password("demo1234")
        demo_user.save()

        shops = [
            ("Elm Street Espresso", "123 Elm St", ["cozy", "wifi"], 4.6, (37.77, -122.42)),
            ("Harbor Roasters", "50 Bay Ave", ["patio", "quiet"], 4.4, (37.78, -122.41)),
            ("Sunrise Cafe", "9 Market St", ["matcha", "tea"], 4.2, (37.79, -122.43)),
        ]
        created_shops = []
        for name, addr, tags, rating, coords in shops:
            shop, _ = CoffeeShop.objects.get_or_create(
                name=name,
                defaults={"address": addr, "tags": tags, "avg_rating": rating, "lat": coords[0], "lon": coords[1]},
            )
            created_shops.append(shop)
            MenuItem.objects.get_or_create(shop=shop, name="House Latte", defaults={"price": 4.50, "flavor_tags": ["milk"]})
            MenuItem.objects.get_or_create(shop=shop, name="Cold Brew", defaults={"price": 4.00, "category": "cold"})

        # Quotes
        Quote.objects.get_or_create(text="Sip slowly; the best ideas steep over time.", mood_tag="calm")
        Quote.objects.get_or_create(text="You got this—one espresso shot at a time.", mood_tag="tired")
        Quote.objects.get_or_create(text="Celebrate small wins with a sweet latte.", mood_tag="happy")

        # Journal + favorites
        if created_shops:
            shop = created_shops[0]
            JournalEntry.objects.get_or_create(
                user=demo_user,
                shop=shop,
                visit_date=timezone.now().date(),
                my_rating=5,
                defaults={"notes": "Loved the vibe and fast wifi."},
            )
            Favorite.objects.get_or_create(user=demo_user, shop=shop)
            rev, created = Review.objects.get_or_create(user=demo_user, shop=shop, rating=5, defaults={"comment": "Great espresso!"})
            if created:
                shop.update_rating(rev.rating)

        self.stdout.write(self.style.SUCCESS("Seeded demo data. Login with demo/demo1234"))
