"""
All bot messages — Romanian only 🇷🇴
Edit text here. Never touch bot.py.
{video_url_1}, {video_url_2}, {video_url_3} are filled automatically in the video messages.
"""

MSG = {

    # ── Mesaj 1: Bun venit (afișat la /start) ─────────────────────────
    "welcome": (
        "Bună ziua.\n\n"
        "Ai accesat video-ul gratuit de la Victor Bologan: "
        "\"Cum am ajutat beneficiarii mei să își crească veniturile de până la 9X "
        "prin hipnoterapie și reprogramarea subconștientului\".\n\n"
        "În acest material vei vedea un studiu de caz și 5 blocaje interioare "
        "care pot influența veniturile, vânzările și capacitatea de a acționa."
    ),

    # ── Mesaj 2a: Video 1 ─────────────────────────────────────────────
    # {video_url_1} replaced automatically
    "video_1": (
        "🎬 Video 1 din 3\n\n"
        "Îți recomandăm să îl urmărești într-un moment liniștit. "
        "Durata: aproximativ 20 de minute.\n\n"
        "{video_url_1}\n\n"
        "Apasă «Am urmărit» când ești gata pentru video-ul următor."
    ),

    # ── Mesaj 2b: Video 2 ─────────────────────────────────────────────
    # {video_url_2} replaced automatically
    "video_2": (
        "🎬 Video 2 din 3\n\n"
        "Continuăm. Îți recomandăm să îl urmărești tot într-un moment liniștit. "
        "Durata: aproximativ 20 de minute.\n\n"
        "{video_url_2}\n\n"
        "Apasă «Am urmărit» când ești gata pentru ultimul video."
    ),

    # ── Mesaj 2c: Video 3 ─────────────────────────────────────────────
    # {video_url_3} replaced automatically
    "video_3": (
        "🎬 Video 3 din 3\n\n"
        "Ultimul video din serie. "
        "La final vei primi câteva întrebări care te pot ajuta să înțelegi "
        "mai clar propriul tău blocaj interior.\n\n"
        "{video_url_3}\n\n"
        "Apasă «Am urmărit» când ai terminat."
    ),

    # ── Mesaj 3: Întrebare după vizionare ─────────────────────────────
    "after_video": (
        "Ce temă ți-a atras cel mai mult atenția în video?"
    ),

    # ── Butoane teme ──────────────────────────────────────────────────
    "topics": [
        ("Frica de a mă exprima",                   "topic_1"),
        ("Frica de refuz sau evaluare",              "topic_2"),
        ("Dificultatea de a cere mai mult",          "topic_3"),
        ("Amânarea acțiunilor importante",           "topic_4"),
        ("Scenarii repetitive legate de bani sau valoare", "topic_5"),
    ],

    # ── Mesaj 4: Prегрев (warmup) ─────────────────────────────────────
    "warmup": (
        "Mulțumim pentru răspuns.\n\n"
        "În multe cazuri, limita de venit nu este legată doar de strategii sau cunoștințe. "
        "Uneori, omul are instrumente, dar în interior apare rezistența: "
        "frica de a fi văzut, frica de refuz, sentimentul că nu merită mai mult "
        "sau tensiunea înaintea unei decizii importante.\n\n"
        "În lucrul individual, aceste mecanisme pot fi explorate mai profund și mai calm."
    ),

    # ── Mesaj 5: Ofertă consultație ───────────────────────────────────
    "consultation": (
        "Dacă ai recunoscut în video un blocaj care se repetă în viața, "
        "vânzările, veniturile sau manifestarea ta, poți începe cu o "
        "consultație individuală cu Victor.\n\n"
        "În consultație analizăm cererea ta, vedem unde apare rezistența "
        "și înțelegem ce poate fi lucrat mai profund."
    ),

    # ── Mesaj 6: Reminder 24h ─────────────────────────────────────────
    "reminder_24h": (
        "Ieri ai primit video-ul despre blocajele interioare care pot "
        "influența veniturile și acțiunea.\n\n"
        "O întrebare utilă pentru reflecție: "
        "\"Unde știu ce trebuie să fac, dar totuși amân sau evit?\"\n\n"
        "Dacă vrei, poți analiza acest subiect individual cu Victor."
    ),

    # ── Mesaj 7: Final CTA (trimis la 48h după video) ─────────────────
    "final_cta": (
        "Dacă simți că tema este actuală pentru tine, poți lăsa o cerere "
        "pentru o consultație individuală.\n\n"
        "Formatul este calm, confidențial și fără presiune."
    ),

    # ── Confirmare cerere primită ──────────────────────────────────────
    "received": (
        "✅ Cererea ta a fost primită!\n\n"
        "Victor te va contacta în curând. 🙏"
    ),
}
