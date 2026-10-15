import random
import re
from typing import List, Dict, Any, Tuple
from database.hashtags_data import CATEGORIES, REK_TRIGGERS


def clean_text_to_tag(text: str) -> str:
    """Matnni toza heshteg formatiga o'tkazish"""
    # Maxsus belgilarni olib tashlash va pastki chiziqqa aylantirish
    cleaned = re.sub(r"[^\w\s]", "", text)
    cleaned = re.sub(r"\s+", "_", cleaned.strip().lower())
    return cleaned


def find_matching_category(query: str) -> Tuple[str, Dict[str, Any]]:
    """Foydalanuvchi yozgan matn qaysi toifaga mos kelishini aniqlash"""
    query_lower = query.lower()
    
    # 1. To'g'ridan-to'g'ri toifa kalitiga tekshirish
    if query_lower in CATEGORIES:
        return query_lower, CATEGORIES[query_lower]
        
    # 2. Kalit so'zlar bo'yicha qidirish
    best_cat = None
    max_matches = 0
    
    for cat_id, cat_data in CATEGORIES.items():
        matches = 0
        for kw in cat_data.get("keywords", []):
            if kw in query_lower:
                matches += 1
        if matches > max_matches:
            max_matches = matches
            best_cat = (cat_id, cat_data)
            
    if best_cat and max_matches > 0:
        return best_cat
        
    # Agar aniq toifa topilmasa, umumiy biznes/lifestyle asos qilib olinadi
    return "custom", {}


def generate_custom_tags(query: str, lang: str = "uz") -> List[str]:
    """Maxsus kiritilgan so'zlar uchun dinamik heshteglar yaratish"""
    words = [w for w in re.split(r"[\s,._-]+", query) if len(w) > 2]
    tags = set()
    
    # Har bir so'zdan teglar
    for w in words:
        w_clean = clean_text_to_tag(w)
        if w_clean:
            tags.add(w_clean)
            tags.add(f"{w_clean}_uz")
            tags.add(f"{w_clean}uzb")
            tags.add(f"{w_clean}_toshkent")
            tags.add(f"{w_clean}_reels")
            
    # 2-3 so'zli birikmalardan teglar
    if len(words) >= 2:
        combined = "".join(words[:2])
        combined_underscore = "_".join(words[:2])
        tags.add(combined)
        tags.add(combined_underscore)
        tags.add(f"{combined}_uz")
        
    return list(tags)


def generate_hashtags(
    category_id: str = "custom",
    custom_query: str = "",
    size: str = "medium",       # "small" (5-8), "medium" (15-18), "large" (25-30)
    lang: str = "mix",          # "uz", "ru", "en", "mix"
    post_type: str = "reels"    # "reels", "post"
) -> Dict[str, Any]:
    """
    Instagram Rek algoritmlariga moslashtirilgan aqlli heshteg generatori.
    Zinapoya (Ladder) strategiyasidan foydalanadi:
    - Niche (aniq mikro-teglar)
    - Audience (auditoriya teglari)
    - General (keng qamrov)
    - Rek triggers (algoritm signallari)
    """
    # 1. Hajm limitlarini belgilash
    if size == "small":
        total_target = random.randint(6, 8)
        counts = {"niche": 3, "audience": 2, "general": 1, "trigger": 2}
    elif size == "large":
        total_target = random.randint(26, 30)
        counts = {"niche": 12, "audience": 7, "general": 5, "trigger": 5}
    else:  # medium - Oltin oraliq
        total_target = random.randint(15, 18)
        counts = {"niche": 7, "audience": 4, "general": 3, "trigger": 3}

    # 2. Toifani aniqlash
    cat_data = {}
    if category_id in CATEGORIES:
        cat_data = CATEGORIES[category_id]
    elif custom_query:
        found_id, found_data = find_matching_category(custom_query)
        if found_data:
            cat_data = found_data
            category_id = found_id

    # 3. Teglar hovuzini yig'ish (Tilga qarab)
    niche_pool = []
    audience_pool = []
    general_pool = []
    
    # Tillarni taqsimlash
    if lang == "mix":
        primary_langs = ["uz", "en"]
    elif lang in ["uz", "ru", "en"]:
        primary_langs = [lang]
    else:
        primary_langs = ["uz"]

    for l in primary_langs:
        if cat_data and l in cat_data:
            niche_pool.extend(cat_data[l].get("niche", []))
            audience_pool.extend(cat_data[l].get("audience", []))
            general_pool.extend(cat_data[l].get("general", []))

    # Agar maxsus so'rov bo'lsa, dinamik teglarni qo'shish
    if custom_query:
        dynamic_tags = generate_custom_tags(custom_query, lang="uz")
        niche_pool = list(set(dynamic_tags + niche_pool))

    # 4. Triggerlar hovuzi
    trigger_pool = []
    if lang == "mix":
        trigger_pool.extend(REK_TRIGGERS.get("uz", []))
        trigger_pool.extend(REK_TRIGGERS.get("en", []))
    else:
        trigger_pool.extend(REK_TRIGGERS.get(lang, REK_TRIGGERS["uz"]))

    if post_type == "post":
        # Post uchun qo'shimcha teglar
        post_extra = ["instapost", "instagrampost", "fotouzb", "uzb_photos"]
        trigger_pool.extend(post_extra)

    # 5. Tasodifiy tanlash va aralashtirish
    random.shuffle(niche_pool)
    random.shuffle(audience_pool)
    random.shuffle(general_pool)
    random.shuffle(trigger_pool)

    selected_niche = niche_pool[:counts["niche"]]
    selected_audience = audience_pool[:counts["audience"]]
    selected_general = general_pool[:counts["general"]]
    selected_trigger = trigger_pool[:counts["trigger"]]

    # Birlashtirish
    all_selected = []
    seen = set()

    for tag in selected_niche + selected_audience + selected_general + selected_trigger:
        tag_clean = tag.strip().replace("#", "").lower()
        if tag_clean and tag_clean not in seen:
            seen.add(tag_clean)
            all_selected.append(tag_clean)

    # Agar kam bo'lib qolsa, trigger va general bilan to'ldirish
    while len(all_selected) < total_target and trigger_pool:
        extra_tag = trigger_pool.pop().strip().replace("#", "").lower()
        if extra_tag not in seen:
            seen.add(extra_tag)
            all_selected.append(extra_tag)

    # Formatlash
    hashtags_list = [f"#{tag}" for tag in all_selected]
    hashtags_string = " ".join(hashtags_list)

    category_title = cat_data.get("title", f"🎯 {custom_query.title() if custom_query else 'Universal'}")

    return {
        "tags_list": hashtags_list,
        "tags_string": hashtags_string,
        "count": len(hashtags_list),
        "category_title": category_title,
        "size": size,
        "lang": lang,
        "post_type": post_type,
        "details": {
            "niche_count": len(selected_niche),
            "audience_count": len(selected_audience),
            "general_count": len(selected_general),
            "trigger_count": len(selected_trigger)
        }
    }
