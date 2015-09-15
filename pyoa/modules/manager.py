_restaurants = {}


def _create_handler(parse_content_getter, parse_callback):
    content = parse_content_getter()

    def handler():
        try:
            return parse_callback(content)
        except Exception as e:
            print('Exception', str(e))  # TODO better logging
            return None

    return handler


def register_restaurant(name, parse_content_getter, parse_callback):
    handler = _create_handler(parse_content_getter, parse_callback)
    _restaurants[name] = handler


def unregister_restaurant(name):
    del _restaurants[name]


def get_restaurants():
    return _restaurants
