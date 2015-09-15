import modules.utils as utils


def create_lunch(name, menus=[], soups=[]):
    return utils.DictAttrWrapper(name=name, soups=soups, menus=menus)


def create_menu(meal, price, soup=None):
    return utils.DictAttrWrapper(meal=meal, soup=soup, price=price)


def create_restaurant(name, url, parse_callback):
    return utils.DictAttrWrapper(name=name, url=url, parse_callback=parse_callback)

if __name__ == "__main__":
    m = create_menu('M', 1, 'S')
    assert(m.meal == 'M')
