from datetime import datetime
import modules.utils as utils
import modules.datafactories as factories
import modules.manager as reg_mgr


NAME = 'fishmen'
URL = 'http://www.restaurantfishmen.sk/index.php/denne-menu'


def _lunches_tag(tag):
    target_style = u'font-family: times new roman,times; font-size: 12pt;'
    return utils.verify_tag(tag, u'span', style=target_style)


def _get_current_day_tag(tag):
    current_day = utils.get_weekday_number(datetime.today())
    return tag.find_all(_lunches_tag)[current_day].parent


def _move_to_next_p(tag):
    return tag.next_sibling.next_sibling


def _get_soup_raw(soup_raw_text):
    return ' '.join(soup_raw_text.split()[2:])


def _get_price_raw(meal_text, alegrens_text):
    return meal_text[-1].replace(alegrens_text, '').replace(',', '.').replace('€', '')


def _get_meal_raw(meal_text):
    return ' '.join(meal_text[3:-2])


def _raw_meals_generator(tag):  # TODO rework with regexps
    act_tag = tag
    for i in range(4):
        act_tag = _move_to_next_p(act_tag)
        if i == 0:
            yield _get_soup_raw(utils.get_text_rec(act_tag.span))
        else:
            meal_text = act_tag.span.get_text().split()
            alegrens_text = act_tag.span.sub.get_text()

            price_raw = _get_price_raw(meal_text, alegrens_text)  # price can be squished with other text
            meal_raw = _get_meal_raw(meal_text)

            yield meal_raw, price_raw


def _get_meals_raw(tag):
    return [m for m in _raw_meals_generator(tag)]


def _get_menu_objs(meals_raw):
    return [factories.create_menu(*meal) for meal in meals_raw]


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
