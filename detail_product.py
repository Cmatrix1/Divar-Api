from requests import get


def get_section(sections, section_name: str, index: int) -> dict:
    section = list(filter(lambda x: x["section_name"] == section_name, sections))
    try:
        return section[0]['widgets'][index]['data'] if section else {}
    except KeyError:
        return {}

def get_attr(sections):
    section = list(filter(lambda x: x["section_name"] == 'LIST_DATA', sections))[0]

    attributes = []
    for i in section["widgets"]:
        data = i.get("data", {})

        if data.get("@type") == "type.googleapis.com/widgets.GroupFeatureRow":
            items = list(map(lambda x: {x["title"]:x.get("available", False)}, data["items"]))
            attributes.extend(items)

        elif data.get("@type") == "type.googleapis.com/widgets.UnexpandableRowData":
            attributes.append({data["title"]:data["value"]})

        elif data.get("@type") == "type.googleapis.com/widgets.GroupInfoRow":
            attributes.extend(data["items"])

        else:
            continue
    return attributes

def extract_detail_product(post_id:str) -> dict:
    response = get(f"https://api.divar.ir/v8/posts-v2/web/{post_id}").json()
    sections = response["sections"]
    titleinfo = get_section(sections, "TITLE", 0)
    title = titleinfo.get('title')
    subtitle = titleinfo.get('subtitle')
    images = get_section(sections, "IMAGE", 0).get('items')
    description = get_section(sections, "DESCRIPTION", 1).get('text') or response["seo"].get("description")
    location = get_section(sections, "MAP", 0).get("location", {}).get('exact_data', {}).get('point')
    return {
        "title": title,
        "subtitle": subtitle,
        "images": images,
        "description": description,
        "location": location,
        "attributes": get_attr(sections)
    }
        

agahis = ['AZVdzuJv', 'AZVSVRUc', 'AZVS1TX7', 'AZVSFDaZ', 'AZ1JbQV9', 'AZQexa7M', 'AZ5hvatY', 'AZVSVNdn', 'AZ_tI5hy', 'AZIODl9d', 'gYnGjAcr', 'AZVS1fKx', 'AZ31XrZ1', 'AZVSlIV3', 'AZVS1Gsl', 'AZQixUAb', 'AZVSFB-K', 'AZVSVCjw', 'AZVSVAZh', 'AZ75WT35']
for i in agahis:
    data = extract_detail_product(i)
    print(data)