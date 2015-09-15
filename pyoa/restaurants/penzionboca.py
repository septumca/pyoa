from datetime import datetime
import modules.utils as utils
import modules.datafactories as factories
import modules.manager as reg_mgr


NAME = 'penzion boca'
URL = 'http://www.penzion-boca.sk/index.php/tydenne-menu'


def _get_current_day_tag(tag):
    current_day = utils.get_weekday_number(datetime.today())

    start_slice = current_day * 9 + 1  # first tr is name of day
    stop_slice = start_slice + 8  # 8 meals in total, so we need process 7 more

    return tag.find_all('table')[2].find('tbody').find_all('tr')[start_slice:stop_slice]


def _get_price_string(price_tag):
    return price_tag.split('/')[1].strip().split()[0].replace(',', '.')


def _process_trs(trs):
    price_raw = utils.translate_nbs(trs[0].find_all('td')[0].get_text().strip())
    soup_raw = utils.translate_nbs(trs[0].find_all('td')[1].get_text().strip())
    meal_raw = utils.translate_nbs(trs[1].find_all('td')[1].get_text().strip())

    return meal_raw, _get_price_string(price_raw), soup_raw


def _get_meals_raw(tag):
    return [_process_trs(tag[i * 2: i * 2 + 2]) for i in range(0, 4)]


def _get_menu_objs(meals_raw):
    return [factories.create_menu(*meal) for meal in meals_raw]


def _parse(tag):
    current_day_tag = _get_current_day_tag(tag)
    meals_raw = _get_meals_raw(current_day_tag)
    menu_objs = _get_menu_objs(meals_raw)
    lunch_obj = factories.create_lunch(NAME, menu_objs)

    return lunch_obj

reg_mgr.register_restaurant(NAME, utils.get_default_tag_getter(URL), _parse)


if __name__ == "__main__":
    c = utils.get_default_tag_getter(URL)()

    lo = _parse(c)

    print(utils.stringify_lunch(lo))
