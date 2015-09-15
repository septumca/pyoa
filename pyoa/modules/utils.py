from bs4 import BeautifulSoup
import requests


class DictAttrWrapper(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)

    def __getattr__(self, name):
        return self[name]


def translate_nbs(text):
    return ' '.join(text.replace('\xa0', ' ').split())


def verify_tag(tag, name=None, **kwargs):
    is_target_tag = tag.name == name if name is not None else True
    has_correct_style = sum([1 for attr, value in kwargs.items() if tag.attrs.get(attr, None) != value]) == 0

    return is_target_tag and has_correct_style


def stringify_menu(menu):
    output_str = menu.meal
    if menu.soup is not None:
        output_str += ', ' + menu.soup
    output_str += ' (' + str(menu.price) + ')'

    return output_str


def stringify_lunch(lunch):
    output_str = lunch.name + '\n'
    if len(lunch.soups) > 0:
        output_str += '\tSOUPS:\n\t\t'
        output_str += '\n\t\t'.join(lunch.soups)
        output_str += '\n'

    if len(lunch.menus) > 0:
        output_str += '\tMENUS:\n\t\t'
        output_str += '\n\t\t'.join([stringify_menu(menu) for menu in lunch.menus])
        output_str += '\n'

    return output_str


def get_text_rec(elem):
    if elem.string:
        return elem.string
    elif elem.children:
        for ch in elem.children:
            return get_text_rec(ch)
    else:
        return None


def get_weekday_number(datetime):
    return datetime.weekday()


def get_default_tag_getter(url):
    def getter():
        r = requests.get(url)
        tag = BeautifulSoup(r.content, 'lxml')

        return tag
    return getter
