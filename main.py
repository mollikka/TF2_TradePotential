from sys import exit

from tf2_tools import get_trade_potential, get_duplicates
from steam_api import steam_vanity_name_to_id


def main_duplicates():
    p1_name = input("steam name:").strip()
    p1_steamid = steam_vanity_name_to_id(p1_name)
    p1_duplicates = get_duplicates(p1_steamid)

    tipstring_duplicates = "{}'s duplicates"
    tipstring_no_duplicates = "{} has no duplicates"

    if p1_duplicates is None:
        print("Couldn't retrieve item data")
        return

    print()

    if p1_duplicates:
        print(tipstring_duplicates.format(p1_name))
        for i in p1_duplicates:
            print("- {}".format(i))

    if p1_duplicates: print()

def main_duplicate_compare():
    p1_name = input("steam name:").strip()
    p2_name = input("steam name:").strip()
    p1_steamid = steam_vanity_name_to_id(p1_name)
    p2_steamid = steam_vanity_name_to_id(p2_name)

    p2_needs_from_p1, p1_needs_from_p2 = get_trade_potential(p1_steamid, p2_steamid)

    if (p2_needs_from_p1, p1_needs_from_p2) == (None,None):
        print("Couldn't retrieve item data")
        return

    tipstring_need_none = "{} has no duplicates that {} needs"
    tipstring_need_plural = "{} has {} duplicates that {} needs:"
    tipstring_need_singular = "{} has a duplicate that {} needs:"

    print()

    if len(p2_needs_from_p1) == 0:
        print(tipstring_need_none.format(p1_name, p2_name))
    if len(p2_needs_from_p1) == 1:
        print(tipstring_need_singular.format(p1_name, p2_name))
    if len(p2_needs_from_p1) > 1:
        print(tipstring_need_plural.format(p1_name, len(p2_needs_from_p1), p2_name))
    for i in p2_needs_from_p1:
        print("- {}".format(i))

    print()

    if len(p1_needs_from_p2) == 0:
        print(tipstring_need_none.format(p2_name, p1_name))
    if len(p1_needs_from_p2) == 1:
        print(tipstring_need_singular.format(p2_name, p1_name))
    if len(p1_needs_from_p2) > 1:
        print(tipstring_need_plural.format(p2_name, len(p1_needs_from_p2), p1_name))
    for i in p1_needs_from_p2:
        print("- {}".format(i))

    if p1_needs_from_p2 or p2_needs_from_p1: print()

def main():
    while True:
        print("1) duplicate compare")
        print("2) list duplicates")
        print("x) exit")

        choice = input().strip()
        if choice == "1":
            main_duplicate_compare()
        if choice == "2":
            main_duplicates()
        if choice == "x":
            exit()
        print()

if __name__ == "__main__":
    main()
