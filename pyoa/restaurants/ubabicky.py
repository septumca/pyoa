from datetime import datetime
import modules.utils as utils
import modules.datafactories as factories
import modules.manager as reg_mgr


NAME = 'ubabicky'
URL = 'http://ubabicky.sk/'


def _get_current_day_tag(tag):
    current_day = utils.get_weekday_number(datetime.today())
    return tag.table.find_all('tbody')[current_day]


def _get_meals_raw(tag):
    return [utils.get_text_rec(td.next_sibling.next_sibling) for td in tag.find_all('h1')]


def _get_menu_objs(meals_raw):
    return [factories.create_menu(meal, 3) for meal in meals_raw]


def _parse(tag):
    current_day_tag = _get_current_day_tag(tag)
    meals_raw = _get_meals_raw(current_day_tag)
    menu_soup = meals_raw[0]
    menu_objs = _get_menu_objs(meals_raw[1:])
    lunch_obj = factories.create_lunch(NAME, menu_objs, [menu_soup])

    return lunch_obj

reg_mgr.register_restaurant(NAME, utils.get_default_tag_getter(URL), _parse)


if __name__ == "__main__":
    c = utils.get_default_tag_getter(URL)()

    lo = _parse(c)

    print(utils.stringify_lunch(lo))
