from rest_framework.decorators import api_view
from rest_framework.response import Response
from shops.models import CoffeeShop
from shops.serializers import CoffeeShopSerializer
from .tags import text_to_tags
from .scoring import score_shop, to_reason

@api_view(["POST"])
def recommend(request):
    text = (request.data.get("text") or "").strip()
    if not text: return Response({"detail":"text required"}, status=400)
    tagset = text_to_tags(text)
    shops = list(CoffeeShop.objects.all())
    scored = sorted(shops, key=lambda s: score_shop(s, tagset), reverse=True)[:3]
    items = [{"shop":CoffeeShopSerializer(s).data,
              "reason":to_reason(s, tagset),
              "score": round(score_shop(s, tagset),3)} for s in scored]
    return Response({"tags": sorted(tagset), "items": items})
