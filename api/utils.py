def text_to_slug(name: str):
    slug_name = ""
    name_split = name.split()

    for i in name_split:
        slug_name += i.capitalize()
    return slug_name
