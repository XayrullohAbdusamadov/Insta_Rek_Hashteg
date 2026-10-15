"""
Instagram Reels va Postlar uchun eng kuchli heshteglar bazasi.
Kategoriyalar, mikro-nishlar, auditoriya teglari va Rek triggerlari.
"""

# Instagram tavsiyalariga (Rek / Explore) turtki beruvchi maxsus trigger-teglar
REK_TRIGGERS = {
    "uz": [
        "reelsuzb", "reelsuzbekistan", "rekuz", "rekuzb", "trenduz",
        "topuzb", "uzbekistan_inst", "toshkentcity", "uzbekvideo",
        "rekkachiq", "rekomendatsiya", "trendlar", "uz_reels", "uzbekistan"
    ],
    "ru": [
        "рилс", "рекомендации", "рек", "тренды", "топконтент",
        "рилсинстаграм", "рилсыкаждыйдень", "втопе", "рекомендация",
        "трендырилс", "хочуврек", "популярное", "вирусноевидео"
    ],
    "en": [
        "reels", "reelsinstagram", "viralreels", "trendingreels",
        "explorepage", "instareels", "foryou", "viralvideos", "fyp",
        "explore", "trendingnow", "reelsviral", "contentcreator"
    ]
}

# Mavzular bo'yicha boyitilgan bazalar
# Har bir toifada:
# - niche: mikro va aniq yo'nalish teglari (raqobat kam, tez ko'tariladi)
# - audience: auditoriya va hamjamiyat teglari
# - general: keng qamrovli ommabop teglar
CATEGORIES = {
    "biznes": {
        "title": "💼 Biznes & Tadbirkorlik",
        "keywords": ["biznes", "pul", "daromad", "tadbirkor", "savdo", "marketing", "sotuv", "startap", "investitsiya"],
        "uz": {
            "niche": ["biznes_uz", "tadbirkorlik", "daromad_topish", "savdo_siri", "biznes_reja", "investitsiya_uz", "pul_ishlash", "biznesmen_uz", "sotuv_marketing"],
            "audience": ["uzb_biznes", "tadbirkorlar", "yosh_tadbirkor", "uzbekistan_business", "daromad", "investorlar_uz", "biznesklub"],
            "general": ["biznes", "pul", "muvaffaqiyat", "boylik", "rivojlanish", "maqsad"]
        },
        "ru": {
            "niche": ["бизнес_идеи", "доходвинтернете", "продажионлайн", "стартапы", "инвестициидляначинающих", "маркетингвсоцсетях", "финансоваяграмотность"],
            "audience": ["бизнесмены", "предприниматели", "клубпредпринимателей", "инвесторы", "сообществобизнеса"],
            "general": ["бизнес", "деньги", "доход", "инвестиции", "успех", "мотивациякдействию"]
        },
        "en": {
            "niche": ["businessgrowth", "startupstrategy", "makemoneyonline", "salescoach", "businesstips101", "investingtips", "entrepreneurmindset"],
            "audience": ["youngentrepreneurs", "smallbusinessclub", "creatorscommunity", "digitalbusinessowner"],
            "general": ["business", "money", "entrepreneur", "success", "marketing", "wealth"]
        }
    },
    "motivatsiya": {
        "title": "🔥 Motivatsiya & Psixologiya",
        "keywords": ["motivatsiya", "hayot", "maqsad", "intizom", "psixologiya", "fikr", "kuch", "sabr", "muvaffaqiyat"],
        "uz": {
            "niche": ["motivatsiya_uz", "hayotiy_haqiqatlar", "intizom", "kuchli_fikrlar", "muvaffaqiyat_sirlari", "hayotiy_sozlar", "ibratli_sozlar", "maqsadlar"],
            "audience": ["uzbmotivatsiya", "ruhiy_rivojlanish", "motivatsiyauz", "yoshlar_uchun", "aqlli_sozlar", "hayot_darsi"],
            "general": ["motivatsiya", "hayot", "maqsad", "sabr", "baxt", "orzu", "intilish"]
        },
        "ru": {
            "niche": ["мотивациянауспех", "психологияжизни", "силамысли", "самодисциплина", "мысливслух", "цитатысосмыслом", "мудрыеслова"],
            "audience": ["мотивациякаждыйдень", "психологияличности", "личностныйрост", "клубмотивации"],
            "general": ["мотивация", "психология", "жизнь", "успех", "цель", "счастье"]
        },
        "en": {
            "niche": ["dailymotivation", "disciplineovermotivation", "mindsetmatters", "stoicquotes", "selfgrowthtips", "successmindset", "nevergiveup"],
            "audience": ["motivationcommunity", "highachievers", "growthmindsetcrew", "dailyinspiration"],
            "general": ["motivation", "mindset", "quotes", "goals", "lifestyle", "wisdom"]
        }
    },
    "it_texnologiya": {
        "title": "💻 IT, Dasturlash & AI",
        "keywords": ["it", "dasturlash", "kod", "python", "ai", "texnologiya", "gadjet", "kompyuter", "frontend", "backend"],
        "uz": {
            "niche": ["dasturlash_uz", "it_uzbekistan", "python_uz", "kod_yozish", "dasturchilar", "it_sohasi", "suniy_intellekt", "frontend_uz", "dasturiy_ta'minot"],
            "audience": ["uzb_dev", "dasturchi_hayoti", "toshkent_it", "dasturlash_darslari", "texnologiyalar_uz", "uzdevs"],
            "general": ["dasturlash", "texnologiya", "itpark", "kod", "kompyuter", "bilim"]
        },
        "ru": {
            "niche": ["программированиеснуля", "pythonразработка", "искусственныйинтеллект", "будниитишника", "коддня", "вебразработка", "нейросеть"],
            "audience": ["сообществопрограммистов", "айтишники", "вебразработчики", "техномир"],
            "general": ["программирование", "технологии", "it", "компьютеры", "нейросети", "разработка"]
        },
        "en": {
            "niche": ["codinglife", "pythonprogramming", "webdeveloper", "artificialintelligence", "machinelearning", "learntocode", "techreview", "aiagents"],
            "audience": ["developercommunity", "programmerhumor", "techies", "softwareengineers"],
            "general": ["coding", "programming", "technology", "tech", "software", "ai"]
        }
    },
    "avto": {
        "title": "🚗 Avto, Mashinalar & Tuning",
        "keywords": ["avto", "mashina", "inomarka", "gentra", "malibu", "byd", "tuning", "drift", "avtobozor", "avto_narxlar"],
        "uz": {
            "niche": ["avtouz", "gentra_tuning", "malibu2", "byduzbekistan", "inomarkauz", "avtobozortoshkent", "avto_tuning_uz", "moshinabozor", "tezlik"],
            "audience": ["uzb_avto", "mashinalar_olami", "avtosevarlar", "toshkent_avto", "driver_uz", "avtouzb"],
            "general": ["avto", "mashina", "tuning", "tezlik", "avtomobil", "track"]
        },
        "ru": {
            "niche": ["автообзор", "тюнингтачек", "тестдрайв", "машинымечты", "автоподбор", "гонкипогороду", "звуквыхлопа"],
            "audience": ["автолюбители", "клубавто", "пацанскиетачки", "автосообщество"],
            "general": ["авто", "машины", "тачки", "тюнинг", "скорость", "автомобили"]
        },
        "en": {
            "niche": ["carsofinstagram", "carmodification", "supercarspotting", "turbocars", "cartuning", "driftculture", "carreels"],
            "audience": ["petrolheads", "carcommunity", "carenthusiasts", "cargram"],
            "general": ["cars", "car", "tuning", "speed", "motorsport", "auto"]
        }
    },
    "sport_fitness": {
        "title": "🏋️ Sport & Fitness",
        "keywords": ["sport", "fitness", "zal", "trenirovka", "bodibilding", "vazn", "parhez", "mashq", "muskul"],
        "uz": {
            "niche": ["sport_uz", "zal_mashqlari", "fitness_uzb", "bodibilding_uz", "vazn_tashlash", "togri_ovqatlanish", "mashg_mashqlari", "sport_zali"],
            "audience": ["uzb_sport", "sportsevarlar", "soglom_turmush", "zal_motivatsiyasi", "sportchilar_uz"],
            "general": ["sport", "fitness", "mashq", "soglik", "kuch", "chidam"]
        },
        "ru": {
            "niche": ["тренировкивзале", "фитнесдома", "похудениебездиет", "набормассы", "программатренировок", "правильноепитание", "качалка"],
            "audience": ["фитнессообщество", "спортсмены", "зожники", "любителифитнеса"],
            "general": ["спорт", "фитнес", "тренировка", "зож", "здоровье", "теломечты"]
        },
        "en": {
            "niche": ["gymworkout", "calisthenicsmovement", "weightlosstransformation", "fitnesstipsdaily", "hypertrophy", "strengthtraining"],
            "audience": ["fitnesscommunity", "gymrat", "fitfam", "athleteslife"],
            "general": ["fitness", "workout", "gym", "bodybuilding", "health", "exercise"]
        }
    },
    "retsept_taomlar": {
        "title": "🍳 Retseptlar & Pazandachilik",
        "keywords": ["retsept", "taom", "pazanda", "oshxona", "shirinlik", "pishiriq", "mazzali", "fastfood", "milliy"],
        "uz": {
            "niche": ["oson_retsept", "milliy_taomlar", "pazandachilik_sirlari", "shirinliklar_retsepti", "mazzali_taom", "oshxona_uz", "uy_retsepti", "pishiriqlar_uz"],
            "audience": ["uzb_pazandalar", "shirinliklar", "uy_bekalari", "retseptlaruz", "taomlar_olami"],
            "general": ["retsept", "taom", "pazandachilik", "oshxona", "mazzali", "pishiriq"]
        },
        "ru": {
            "niche": ["простыерецепты", "готовимдомавкусно", "быстрыйужин", "рецептыза5минут", "выпечкадомашняя", "кулинарныелайфхаки", "вкуснаяеда"],
            "audience": ["кулинарныйклуб", "фудблогеры", "любителиготовить", "домашняякухня"],
            "general": ["рецепты", "еда", "кулинария", "вкусно", "ужин", "десерт"]
        },
        "en": {
            "niche": ["easyrecipesathome", "quickdinnerideas", "bakingrecipes", "streetfoodlover", "healthycooking", "foodhacks", "cookwithme"],
            "audience": ["foodiegram", "homechefs", "recipeshare", "foodlovers"],
            "general": ["recipes", "food", "cooking", "delicious", "foodporn", "yummy"]
        }
    },
    "yumor_vayn": {
        "title": "😂 Yumor, Prikol & Vayn",
        "keywords": ["prikol", "kulgili", "vayn", "kulgu", "hazil", "kayfiyat", "kulgi", "hazillar", "mem"],
        "uz": {
            "niche": ["vaynuz", "prikoluz", "kulgilivideo", "qiziqarli_videolar", "kayfiyatni_kotaramiz", "kulgu_vaqti", "uzbvayn", "hazil_dunyosi"],
            "audience": ["uzb_prikollar", "kulgu_uz", "vaynchilar", "toshkent_prikol", "kayfiyatuz"],
            "general": ["kulgili", "prikol", "vayn", "kayfiyat", "hazil", "kulgu"]
        },
        "ru": {
            "niche": ["смешныевидео", "жизненныемемы", "вайны2026", "приколыдня", "юморю", "угарныевидео", "смехдослез"],
            "audience": ["мемоманы", "клубюмора", "любителипосмеяться", "смешнойконтент"],
            "general": ["юмор", "прикол", "смешно", "мемы", "смех", "вайны"]
        },
        "en": {
            "niche": ["funnyreels", "relatablehumor", "comedyvideo", "memeoftheday", "lolvideos", "hilariousclips", "funnymoments"],
            "audience": ["comedyclub", "memepage", "laughdaily", "entertainingreels"],
            "general": ["funny", "comedy", "memes", "humor", "lol", "laugh"]
        }
    },
    "kiyim_moda": {
        "title": "👗 Moda, Kiyim & Style",
        "keywords": ["kiyim", "moda", "uslub", "style", "trend", "fashion", "look", "oyoqkiyim", "garderob"],
        "uz": {
            "niche": ["uzb_fashion", "kiyimlar_toshkent", "uslubiy_look", "erkaklar_kiyimi", "ayollar_kiyimi", "trend_kiyimlar", "garderob_tanlash"],
            "audience": ["toshkent_moda", "uslubsevarlar", "kiyim_do'koni", "uzbek_style"],
            "general": ["moda", "kiyim", "style", "uslub", "trend", "fashion"]
        },
        "ru": {
            "niche": ["стильныеобразы", "модныесоветы", "капсульныйгардероб", "трендыодежды", "базовыйгардероб", "лукдня"],
            "audience": ["модныйклуб", "любителистиля", "фэшнблогеры"],
            "general": ["мода", "стиль", "одежда", "образ", "тренды", "шопинг"]
        },
        "en": {
            "niche": ["outfitoftheday", "styleinspo", "capsulewardrobe", "fashionhacks", "streetwearstyle", "aestheticoutfits"],
            "audience": ["fashioncommunity", "stylecreators", "fashionlovers"],
            "general": ["fashion", "style", "outfit", "ootd", "clothing", "trends"]
        }
    },
    "gozallik_parvarish": {
        "title": "💄 Go'zallik & Parvarish",
        "keywords": ["makiyaj", "kosmetika", "parvarish", "teri", "gozallik", "soch", "salon", "estetika"],
        "uz": {
            "niche": ["makiyaj_darslari", "teri_parvarishi", "gozallik_sirlari", "soch_parvarishi", "kosmetika_uz", "salon_toshkent"],
            "audience": ["uzb_beauty", "gozallik_olami", "makiyaj_uz", "estetika_uz"],
            "general": ["gozallik", "makiyaj", "kosmetika", "parvarish", "estetika"]
        },
        "ru": {
            "niche": ["уходзакожейлица", "макияжобучение", "секретыкрасоты", "уходзаволосами", "косметикадня", "эстетикалица"],
            "audience": ["бьютисообщество", "бьютиблогеры", "клубкрасоты"],
            "general": ["красота", "макияж", "уход", "косметика", "бьюти", "эстетика"]
        },
        "en": {
            "niche": ["skincareroutine", "makeuptutorial", "glassskintips", "haircarejourney", "cleanbeauty", "beautyhacks"],
            "audience": ["beautycommunity", "skincarelovers", "muasfeaturing"],
            "general": ["beauty", "makeup", "skincare", "cosmetics", "glow", "selfcare"]
        }
    },
    "mobilografiya_smm": {
        "title": "📱 Mobilografiya, SMM & Montaj",
        "keywords": ["mobilografiya", "montaj", "capcut", "smm", "kontent", "video", "reels_montaj", "kamera", "kadr"],
        "uz": {
            "niche": ["mobilografiya_uz", "video_montaj", "capcut_darslari", "smm_mutaxassis", "kontent_yaratish", "kadr_siri", "reels_video_uz"],
            "audience": ["uzb_mobilograflar", "smm_uzbekistan", "kontentmeykerlar", "videograflar_uz"],
            "general": ["mobilografiya", "montaj", "smm", "video", "kontent", "capcut"]
        },
        "ru": {
            "niche": ["мобилографияобучение", "монтажвидеонателефоне", "фишкикапкат", "сммпродвижение", "съемкавидео", "трендовыймонтаж"],
            "audience": ["мобилографы", "сммщики", "контентмейкеры", "видеографы"],
            "general": ["мобилография", "монтаж", "смм", "видео", "контент", "рилсы"]
        },
        "en": {
            "niche": ["mobilevideography", "capcuttutorial", "contentcreationtips", "reelsediting", "cinematicmobile", "videohacks"],
            "audience": ["contentcreators", "videographersclub", "creatorcommunity"],
            "general": ["videography", "editing", "content", "creative", "camera", "visuals"]
        }
    },
    "sayohat_turizm": {
        "title": "✈️ Sayohat & Turizm",
        "keywords": ["sayohat", "turizm", "samolyot", "tog", "tabiat", "dubay", "antaliya", "samarqand", "dengiz"],
        "uz": {
            "niche": ["sayohat_uz", "toglar_bagrida", "samarqand_sayri", "chet_elga_sayohat", "arzon_sayohat", "tabiat_manzaralari"],
            "audience": ["uzb_sayohatchilar", "sayohatsevarlar", "dunyo_boylab", "toshkent_turizm"],
            "general": ["sayohat", "turizm", "tabiat", "damolish", "dunyo", "manzara"]
        },
        "ru": {
            "niche": ["путешествияпомиру", "красивыеместапланеты", "лайфхакипутешественников", "горыиморе", "туризм2026"],
            "audience": ["клубпутешественников", "тревелблогеры", "любителипутешествий"],
            "general": ["путешествия", "туризм", "горы", "море", "отдых", "природа"]
        },
        "en": {
            "niche": ["travelbucketlist", "hiddenplacesonearth", "budgettraveltips", "mountainviews", "wanderlustvibes"],
            "audience": ["travelcommunity", "wanderlusttribe", "globetrotters"],
            "general": ["travel", "tourism", "nature", "vacation", "explore", "adventure"]
        }
    },
    "talim_til": {
        "title": "📚 Ta'lim, Til & IELTS",
        "keywords": ["talim", "ielts", "ingliztili", "til", "grant", "universitet", "dars", "kitob", "talaba"],
        "uz": {
            "niche": ["ingliz_tili_uz", "ielts_toshkent", "til_organamiz", "talabalar_hayoti", "chetelda_oqish", "kitoblar_olami", "grantlar_uz"],
            "audience": ["uzb_talabalar", "ielts_tayyorgarlik", "ingliz_tili_darslari", "oqish_motivatsiyasi"],
            "general": ["talim", "ielts", "til", "kitob", "bilim", "talaba"]
        },
        "ru": {
            "niche": ["английскийснуля", "подготовкакиелтс", "учебазаграницей", "полезныекниги", "студенческаяжизнь"],
            "audience": ["клубстудентов", "изучениеязыков", "читатели"],
            "general": ["образование", "языки", "книги", "знания", "учеба", "саморазвитие"]
        },
        "en": {
            "niche": ["learnenglishdaily", "ieltspreparation", "studyhacks", "bookrecommendations", "studentmotivation"],
            "audience": ["studygram", "languagelearners", "bookloversclub"],
            "general": ["education", "learning", "english", "books", "study", "knowledge"]
        }
    }
}
