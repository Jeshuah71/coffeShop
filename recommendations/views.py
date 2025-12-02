from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .services import ShopRecommender
from .agent import CatChatbotAgent
from .services import QuoteRecommender
from .ml_sentiment import SentimentAnalyzer
from .models import Quote

@api_view(["POST"])
@permission_classes([AllowAny])
def recommend(request):
    text = (request.data.get("text") or "").strip()
    if not text: return Response({"detail":"text required"}, status=400)
    recommender = ShopRecommender()
    items = recommender.recommend(text)
    return Response({"items": items})


@api_view(["POST"])
@permission_classes([AllowAny])
def catbot(request):
    prompt = (request.data.get("message") or "").strip()
    agent = CatChatbotAgent()
    reply = agent.get_response(prompt)
    return Response({"reply": reply, "prompt": prompt})
