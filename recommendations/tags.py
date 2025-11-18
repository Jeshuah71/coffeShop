BASIC_TAGS = {
    "cozy":["cozy","quiet"],
    "study":["quiet","outlets","wifi"],
    "vanilla":["vanilla","milk"],
    "strong":["strong"],
    "iced":["iced"],
    "matcha":["matcha","tea"],
}
def text_to_tags(text:str)->set:
    t = text.lower()
    tags=set()
    for k, vals in BASIC_TAGS.items():
        if k in t: tags.update(vals)
    if "quiet" in t: tags.add("quiet")
    if "wifi" in t: tags.add("wifi")
    if "latte" in t: tags.add("milk")
    return tags
