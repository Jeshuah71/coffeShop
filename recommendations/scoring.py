def score_shop(shop, tagset:set)->float:
    overlap = len(set(shop.tags or []) & tagset)
    return 0.6*float(shop.avg_rating or 0) + 0.4*overlap

def to_reason(shop, tagset:set)->str:
    hits = list(set(shop.tags or []) & tagset)
    return (f"Matches: {', '.join(hits)} • Rating {shop.avg_rating:.1f}"
            if hits else f"Rating {shop.avg_rating:.1f}")
