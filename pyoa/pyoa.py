import modules.manager as mgr
import modules.utils as utils
from restaurants import ubabicky, beniczky, fishmen, penzionboca


if __name__ == "__main__":
    restaurants_dict = mgr.get_restaurants()
    lunch_objs = [h() for h in restaurants_dict.values()]
    delimeter = '\n' + ''.join(['-' for _ in range(80)]) + '\n'

    output = delimeter.join([utils.stringify_lunch(l) for l in lunch_objs if l is not None])

    print(output)
