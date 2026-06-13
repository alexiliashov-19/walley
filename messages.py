"""
All bot messages in Romanian (RO) and Russian (RU).
Uses Telegram MarkdownV2 — special chars are pre-escaped with raw strings (r"...").
To edit text — change only the strings here, never touch bot.py.
"""

# Shown before language is chosen — keep it neutral
LANG_SELECT_TEXT = (
    "👋 Bună ziua / Здравствуйте!\n\n"
    "Alegeți limba / Выберите язык:"
)

MESSAGES = {

    # ─────────────────────────────────────────────
    # ROMANIAN
    # ─────────────────────────────────────────────
    "RO": {

        "btn_get_video":        "▶️ Primește video-ul",
        "btn_watched":          "✅ Am urmărit",
        "btn_consultation":     "📅 Vreau consultație",
        "btn_reminder_consult": "📅 Analizez cu Victor",

        "topics": [
            ("😰 Frica de a mă exprima",             "topic_1"),
            ("🙅 Frica de refuz sau evaluare",        "topic_2"),
            ("💬 Dificultatea de a cere mai mult",    "topic_3"),
            ("⏳ Amânarea acțiunilor importante",     "topic_4"),
            ("🔁 Scenarii repetitive legate de bani", "topic_5"),
        ],

        "welcome": (
            "Bună ziua. 👋\n\n"
            "Ai accesat video-ul gratuit de la Victor Bologan:\n\n"
            "🎬 *Cum am ajutat beneficiarii mei să își crească veniturile "
            "de până la 9X prin hipnoterapie și reprogramarea subconștientului*\n\n"
            "În acest material vei vedea un studiu de caz și 5 blocaje interioare "
            "care pot influența veniturile, vânzările și capacitatea de a acționa."
        ),

        "video": (
            "🎥 Iată video-ul gratuit:\n\n"
            "👉 {video_url}\n\n"
            "Îți recomandăm să îl urmărești într-un moment liniștit.\n"
            "⏱ *Durată: aproximativ 20 de minute.*\n\n"
            "La final vei primi câteva întrebări care te pot ajuta să înțelegi "
            "mai clar propriul tău blocaj interior."
        ),

        "after_video": (
            "✅ Mulțumesc că ai urmărit video-ul!\n\n"
            "Ce temă ți-a atras cel mai mult atenția?"
        ),

        "warmup": (
            "Mulțumesc pentru răspuns. 🙏\n\n"
            "În multe cazuri, limita de venit nu este legată doar de strategii sau cunoștințe.\n\n"
            "Uneori, omul are instrumente, dar în interior apare *rezistența*: "
            "frica de a fi văzut, frica de refuz, sentimentul că nu merită mai mult "
            "sau tensiunea înaintea unei decizii importante.\n\n"
            "În lucrul individual, aceste mecanisme pot fi explorate mai profund și mai calm."
        ),

        "consultation": (
            "Dacă ai recunoscut în video un blocaj care se repetă în viața, vânzările, "
            "veniturile sau manifestarea ta — poți începe cu o *consultație individuală* cu Victor. 💼\n\n"
            "În consultație:\n"
            "• Analizăm cererea ta\n"
            "• Vedem unde apare rezistența\n"
            "• Înțelegem ce poate fi lucrat mai profund\n\n"
            "Formatul este calm, confidențial și fără presiune."
        ),

        "reminder_24h": (
            "👋 Bună ziua!\n\n"
            "Ieri ai primit video-ul despre blocajele interioare care pot influența "
            "veniturile și acțiunea.\n\n"
            "O întrebare utilă pentru reflecție:\n\n"
            '💭 *"Unde știu ce trebuie să fac, dar totuși amân sau evit?"*\n\n'
            "Dacă vrei, poți analiza acest subiect individual cu Victor."
        ),

        "final_cta": (
            "Dacă simți că tema este actuală pentru tine — poți lăsa o cerere "
            "pentru o *consultație individuală*. 🌿\n\n"
            "Formatul este calm, confidențial și fără presiune."
        ),

        "thanks_choice": "Mulțumesc. Iată câteva gânduri în legătură cu acest subiect...",
        "received":      "✅ Cererea ta a fost primită! Victor te va contacta în curând. 🙏",
        "use_buttons":   "Apasă *Am urmărit* când ești gata. 😊",
        "use_start":     "Folosește butoanele de mai sus sau scrie /start pentru a reporni. 🔄",
    },

    # ─────────────────────────────────────────────
    # RUSSIAN
    # ─────────────────────────────────────────────
    "RU": {

        "btn_get_video":        "▶️ Получить видео",
        "btn_watched":          "✅ Я посмотрел(а)",
        "btn_consultation":     "📅 Хочу консультацию",
        "btn_reminder_consult": "📅 Разобраться с Виктором",

        "topics": [
            ("😰 Страх выражать себя",                "topic_1"),
            ("🙅 Страх отказа или оценки",            "topic_2"),
            ("💬 Сложность просить больше",           "topic_3"),
            ("⏳ Откладывание важных действий",       "topic_4"),
            ("🔁 Повторяющиеся сценарии с деньгами",  "topic_5"),
        ],

        "welcome": (
            "Добрый день. 👋\n\n"
            "Вы получили доступ к бесплатному видео от Виктора Бологана:\n\n"
            "🎬 *Как я помог своим клиентам увеличить доходы до 9X "
            "через гипнотерапию и перепрограммирование подсознания*\n\n"
            "В этом материале вы увидите реальный кейс и 5 внутренних блоков, "
            "которые влияют на доход, продажи и способность действовать."
        ),

        "video": (
            "🎥 Вот ваше бесплатное видео:\n\n"
            "👉 {video_url}\n\n"
            "Рекомендуем смотреть в спокойной обстановке.\n"
            "⏱ *Длительность: около 20 минут.*\n\n"
            "После просмотра вы получите несколько вопросов, "
            "которые помогут глубже понять свой внутренний блок."
        ),

        "after_video": (
            "✅ Спасибо, что посмотрели!\n\n"
            "Какая тема отозвалась больше всего?"
        ),

        "warmup": (
            "Спасибо за ответ. 🙏\n\n"
            "Во многих случаях ограничение дохода связано не только со стратегиями или знаниями.\n\n"
            "Иногда у человека есть все инструменты, но внутри появляется *сопротивление*: "
            "страх быть замеченным, страх отказа, ощущение что не заслуживает большего, "
            "или напряжение перед важным решением.\n\n"
            "В индивидуальной работе эти механизмы можно исследовать глубже и спокойнее."
        ),

        "consultation": (
            "Если вы узнали в видео блок, который повторяется в вашей жизни, "
            "продажах, доходах или проявлении себя — можно начать с "
            "*индивидуальной консультации* с Виктором. 💼\n\n"
            "На консультации:\n"
            "• Разбираем ваш запрос\n"
            "• Видим, где появляется сопротивление\n"
            "• Понимаем, что можно проработать глубже\n\n"
            "Формат спокойный, конфиденциальный и без давления."
        ),

        "reminder_24h": (
            "👋 Добрый день!\n\n"
            "Вчера вы получили видео о внутренних блоках, которые влияют на доход и действия.\n\n"
            "Полезный вопрос для размышления:\n\n"
            "💭 *«Где я знаю, что нужно делать, но всё равно откладываю или избегаю?»*\n\n"
            "Если хотите, можете разобрать эту тему индивидуально с Виктором."
        ),

        "final_cta": (
            "Если тема актуальна для вас — вы можете оставить заявку "
            "на *индивидуальную консультацию*. 🌿\n\n"
            "Формат спокойный, конфиденциальный и без давления."
        ),

        "thanks_choice": "Спасибо. Вот несколько мыслей по этой теме...",
        "received":      "✅ Ваша заявка получена! Виктор свяжется с вами в ближайшее время. 🙏",
        "use_buttons":   "Нажмите *Я посмотрел(а)*, когда будете готовы. 😊",
        "use_start":     "Используйте кнопки выше или напишите /start, чтобы начать заново. 🔄",
    },
}
