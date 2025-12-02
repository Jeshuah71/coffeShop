from __future__ import annotations

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class CatChatbotAgent:
    """
    Coffee-loving cat chatbot using TF-IDF similarity on a small knowledge base.
    """

    def __init__(self):
        self.qa_pairs = [
            ("how do i use coffee corner", "Explore Places to find cafes, tap Save to favorite, use Products to shop featured beans/gear, and log visits in Journal. Your favorites sync when signed in."),
            ("best drink for a tired day", "If you're exhausted, try a double espresso or strong cold brew—pace yourself and hydrate. For a gentler lift, a flat white or cappuccino."),
            ("how to brew better coffee", "Grind fresh, use filtered water, keep a ~1:15 coffee-to-water ratio, and adjust grind for flow time. Purge your grinder and pre-wet filters."),
            ("where to find cozy coffee shop", "Use Places with “cozy” or “remote work” tags, enable location, and look for strong Wi-Fi, outlets, and mellow playlists."),
            ("what is the journal for", "Journal is your coffee diary—log place, date, what you ordered, notes, photos, and set visibility (private/public). Sign in to post."),
            ("how do recommendations work", "We use your saves, moods, and similarity to other shops. Rate/save more to improve recs; use filters for vibe-specific lists."),
            ("how do i save favorites", "Open Places, tap Save on a shop. Signed-in users sync to Saved; guests save locally and can sync after sign-in."),
            ("hola", "¡Hola! Soy el Catbot de Coffee Corner. Pregunta sobre café, recomendaciones o cómo usar la app y te ayudo."),
            ("hi", "Hey there! I'm the Coffee Corner Catbot. Ask me about coffee, shops, gear, or how to use the app."),
            ("how do i reset password", "Go to Sign in, choose “Forgot password,” and use the email link to set a new password."),
            ("how to contact support", "Use the Contact page form or email support@coffeecorner.app. Expect a reply within one business day."),
            ("what is catbot", "I'm a lightweight AI cat focused on Coffee Corner. I answer app how-tos, coffee tips, and recs. No orders, no private data."),
            ("como guardo mis favoritos", "Abre un café en Places y presiona Guardar. Si inicias sesión se sincroniza; si no, se guarda local y luego puedes sincronizar."),
            ("recomendaciones incorrectas", "Califica o guarda algunos cafés que te gusten, cambia tu estado de ánimo, y usa filtros para mejorar las recomendaciones."),
            ("best grinder setting", "For pourover start medium-fine; for espresso finer. Adjust grind: slow flow → coarser, fast flow → finer. Aim for balanced taste."),
            ("espresso tastes sour", "Sour espresso: grind finer, increase temp, lengthen shot slightly. Check your ratio (1:2 in 25-32s) and use fresh beans."),
            ("espresso tastes bitter", "Bitter/ashy: grind coarser, lower temp, shorten shot. Use a 1:2 ratio and avoid very long extractions."),
            ("milk options", "Try oat for creamy/sweet, almond for nutty, whole dairy for classic texture. Steam to ~55-60°C for best sweetness."),
            ("cold brew tips", "Use coarse grind, 1:5-1:8 ratio, 12-16h steep in fridge, then dilute to taste. Filter well for clarity."),
            ("gear to buy", "Start with a burr grinder, good kettle, and a scale. For espresso at home, invest in a stable machine and a precise grinder."),
            ("find beans recommendation", "Look for light-medium roasts for fruity/floral, medium for balanced, darker for chocolatey. Check roast date—fresh within 2–4 weeks."),
        ]
        self.vectorizer = TfidfVectorizer()
        self._fit()

    def _fit(self) -> None:
        questions = [q for q, _ in self.qa_pairs]
        self.question_matrix = self.vectorizer.fit_transform(questions)

    def get_response(self, query: str) -> str:
        if not query.strip():
            return "Meow? Ask me anything about coffee or Coffee Corner!"

        lower = query.lower()
        greetings = ("hi", "hello", "hey", "hola", "buenas")
        if any(lower.startswith(g) for g in greetings) or lower in greetings:
            if "hola" in lower or "buenas" in lower:
                return "¡Hola! Soy el Catbot de Coffee Corner. Pregúntame sobre café, recomendaciones o cómo usar la app y te ayudo."
            return "Hey there! I'm the Coffee Corner Catbot. Ask me about coffee tips, shop recs, or using the app."

        spanish_cues = ("como", "recomendacion", "favoritos", "cafe", "contraseña", "correo", "ayuda", "hola")
        prefers_spanish = any(word in lower for word in spanish_cues)

        q_vec = self.vectorizer.transform([query])
        sims = cosine_similarity(q_vec, self.question_matrix)[0]
        best_idx = sims.argmax()
        best_score = sims[best_idx]
        if best_score < 0.1:
            if prefers_spanish:
                return "No estoy seguro, pero puedo ayudar con café, recomendaciones o cómo usar Coffee Corner. Pide consejos de espresso, cold brew, moliendas o usa la página de Contacto."
            return "I’m just a little coffee cat—ask me about brewing, grinders, espresso fixes, shop recs, or how to use Coffee Corner. If you’re stuck, try the Contact page for a human."
        return self.qa_pairs[best_idx][1]
