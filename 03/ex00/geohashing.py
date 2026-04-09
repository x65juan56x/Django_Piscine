import sys
from antigravity import geohash
# geohash(latitude, longitude, datedow)
# geohash(37.421542, -122.085589, b'2005-05-26-10458.68')


def geohashing():
    if len(sys.argv) != 4:
        raise Exception(
            "Wrong number of arguments.\n"
            "Usage: python3 geohashing.py <latitude> <longitude> <date-dow>\n"
            "Example: python3 geohashing.py 37.421542 -122.085589 2005-05-26-10458.68\n"
        )
    latitude = float(sys.argv[1])
    longitude = float(sys.argv[2])

    datedow_str = sys.argv[3]
    datedow_parts = datedow_str.split('-')
    if (
        len(datedow_parts) != 4 or
        len(datedow_parts[0]) != 4 or not datedow_parts[0].isdigit() or
        len(datedow_parts[1]) != 2 or not datedow_parts[1].isdigit() or
        not (1 <= int(datedow_parts[1]) <= 12) or
        len(datedow_parts[2]) != 2 or not datedow_parts[2].isdigit() or
        not (1 <= int(datedow_parts[2]) <= 31)
    ):
        raise Exception(
            "Invalid datedow format.\n"
            "Expected format: YYYY-MM-DD-DOW (e.g., 2005-05-26-10458.68).\n"
        )
    float(datedow_parts[3])
    datedow = datedow_str.encode("utf-8")
    geohash(latitude, longitude, datedow)


if __name__ == '__main__':
    try:
        geohashing()
    except ValueError:
        print("Error: Latitude, Longitude and DowJones must be valid numbers.")
    except Exception as error:
        print(f"Unexpected error: {error}")

# python3
# >>> import antigravity
# >>> dir(antigravity)
# >>> help(antigravity.geohash)
