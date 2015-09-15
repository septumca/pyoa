from datetime import datetime
import modules.utils as utils
import modules.datafactories as factories
import modules.manager as reg_mgr
import re


NAME = 'beniczky'
URL = 'http://www.cateringbb.sk/'

ALERGENS_REGEXP = re.compile('\(\s*\d+\s*(,\s*\d+\s*)*\)')


def _get_meals_section(tag):
    return tag.has_attr('id') and tag['id'] == 'page_denne-menu'


def _get_meals_div(tag):
    tag_contents = [c for c in tag.contents if c.name is not None]
    return tag.name == u'div' and len(tag_contents) > 0 and tag_contents[0].name == u'address'


def _get_meals_start_address_tag(tag):
    tag_contents = [c for c in tag.contents if c.name is not None]
    return tag.name == u'address' and len(tag_contents) == 1 and tag_contents[0].name == u'strong'


def _move_to_next_address(tag):
    return tag.next_sibling.next_sibling


def _get_all_meals_addresses(start_tag):
    act_tag = _move_to_next_address(start_tag)

    while not _get_meals_start_address_tag(act_tag):
        yield act_tag
        act_tag = _move_to_next_address(act_tag)


def _get_current_day_tag(tag):
    current_day = utils.get_weekday_number(datetime.today())

    meal_section = tag.find_all(_get_meals_section)[0]
    meal_div = meal_section.find_all(_get_meals_div)[0]
    meals_start_tag = meal_div.find_all(_get_meals_start_address_tag)

    return meals_start_tag[current_day]


def _process_meal_string(meal_str):
    meal_wo_alergen_text = ALERGENS_REGEXP.sub('', meal_str)

    price_text = meal_wo_alergen_text.split()[-1]
    meal_text = ' '.join(meal_wo_alergen_text.split()[1:-1])

    return meal_text.strip(), price_text.strip().replace(',', '.').replace('€', '')


def _process_soup_string(soup_str):
    soup_wo_alergen_text = ALERGENS_REGEXP.sub('', soup_str)
    return ' '.join(soup_wo_alergen_text.split()[3:])


def _get_meals_raw(tag):
    return [_process_meal_string(m.get_text()) for m in _get_all_meals_addresses(tag) if len(m.get_text().split()) > 0]


def _get_menu_objs(meals_raw):
    return [factories.create_menu(*meal) for meal in meals_raw]


def _parse(tag):
    current_day_tag = _get_current_day_tag(tag)

    soup_raw = _process_soup_string(current_day_tag.get_text())
    meals_raw = _get_meals_raw(current_day_tag)
    menu_soups = [s.strip() for s in soup_raw.split('/')]
    menu_objs = _get_menu_objs(meals_raw)

    lunch_obj = factories.create_lunch(NAME, menu_objs, menu_soups)

    return lunch_obj

reg_mgr.register_restaurant(NAME, utils.get_default_tag_getter(URL), _parse)


if __name__ == "__main__":
    c = utils.get_default_tag_getter(URL)()

    lo = _parse(c)

    print(utils.stringify_lunch(lo))
