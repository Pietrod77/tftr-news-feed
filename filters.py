INCLUDE_KEYWORDS = [
    "fabric", "textile", "material", "materials", "weave", "weaving",
    "knit", "knitting", "denim", "leather", "dye", "dyeing",
    "pattern-making", "patternmaking", "tailoring", "craftsmanship",
    "atelier", "manufactur", "3d print", "3d-print", "biofabricat",
    "recycled", "recycling", "sustainable material", "textile innovation",
    "garment construction", "embroidery", "print technique",
    "digital fashion", "wearable tech", "innovation",
]

EXCLUDE_KEYWORDS = [
    "red carpet", "wore", "dating", "wedding", "divorce", "engagement",
    "kardashian", "awards show", "stock price", "shares", "acquisition",
    "merger", "ipo", "lawsuit", "layoffs", "ceo", "earnings", "revenue",
    "quarterly", "appoint",
]


def passes_filter(title: str, summary: str) -> bool:
    text = f"{title} {summary}".lower()
    if any(bad in text for bad in EXCLUDE_KEYWORDS):
        return False
    return any(good in text for good in INCLUDE_KEYWORDS)
