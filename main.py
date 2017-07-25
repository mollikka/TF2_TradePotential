from steam_api import steam_item_data, steam_vanity_name_to_id
from steam_api import steam_player_items

TF2 = 440
TF2_IRRELEVANT_ITEMS = ( "saxxy", "classy_token", "slot_token", "tf_wearable",
            "no_entity", "map_token", "tool", "tf_powerup_bottle",
                    "upgrade", "craft_item", "bundle", "supply_crate", "")

def get_trade_potential(steamid1, steamid2):

    item_data = steam_item_data(TF2)
    item_names = {item["defindex"]: item["name"] for item in item_data}
    item_types = {item["defindex"]: item["item_class"] for item in item_data}

    p1_items = steam_player_items(steamid1, TF2)
    p2_items = steam_player_items(steamid2, TF2)

    if p1_items is None or p2_items is None:
        return None, None

    p1_items_filtered = [item["defindex"] for item in p1_items
                             if not item_types[item["defindex"]] in TF2_IRRELEVANT_ITEMS]
    p2_items_filtered = [item["defindex"] for item in p2_items
                             if not item_types[item["defindex"]] in TF2_IRRELEVANT_ITEMS]

    p1_itemset = set(p1_items_filtered)
    p2_itemset = set(p2_items_filtered)

    p1_duplicates = set(i for i in p1_items_filtered
                            if p1_items_filtered.count(i) > 1)
    p2_duplicates = set(i for i in p2_items_filtered
                            if p2_items_filtered.count(i) > 1)

    p2_needs_from_p1 = p1_duplicates - p2_itemset
    p1_needs_from_p2 = p2_duplicates - p1_itemset

    p2_needs_from_p1_names = [item_names[i] for i in p2_needs_from_p1]
    p1_needs_from_p2_names = [item_names[i] for i in p1_needs_from_p2]

    return p2_needs_from_p1_names, p1_needs_from_p2_names

def get_duplicates(steamid):

    item_data = steam_item_data(TF2)
    item_names = {item["defindex"]: item["name"] for item in item_data}
    item_types = {item["defindex"]: item["item_class"] for item in item_data}

    items = steam_player_items(steamid, TF2)
    if items is None: return None

    items_filtered = [item["defindex"] for item in items
                             if not item_types[item["defindex"]] in TF2_IRRELEVANT_ITEMS]
    duplicates = set(i for i in items_filtered
                            if items_filtered.count(i) > 1)

    return [item_names[i] for i in duplicates]

def main():
    p1_name = input("steam name:").strip()
    p2_name = input("steam name:").strip()
    p1_steamid = steam_vanity_name_to_id(p1_name)
    p2_steamid = steam_vanity_name_to_id(p2_name)

    p1_duplicates = get_duplicates(p1_steamid)
    p2_duplicates = get_duplicates(p2_steamid)

    p2_needs_from_p1, p1_needs_from_p2 = get_trade_potential(p1_steamid, p2_steamid)

    if (p2_needs_from_p1, p1_needs_from_p2) == (None,None):
        print("Couldn't retrieve item data")
        return



    tipstring_duplicates = "{}'s duplicates"

    tipstring_need_plural = "{} has {} duplicates that {} needs:"
    tipstring_need_singular = "{} has a duplicate that {} needs:"

    print()

    if p1_duplicates:
        print(tipstring_duplicates.format(p1_name))
        for i in get_duplicates(p1_steamid):
            print("- {}".format(i))

    if p1_duplicates and p2_duplicates: print()

    if p2_duplicates:
        print(tipstring_duplicates.format(p2_name))
        for i in get_duplicates(p2_steamid):
            print("- {}".format(i))

    if p1_needs_from_p2 or p2_needs_from_p1: print()

    if len(p2_needs_from_p1) == 1:
        print(tipstring_need_singular.format(p1_name, p2_name))
    if len(p2_needs_from_p1) > 1:
        print(tipstring_need_plural.format(p1_name, len(p2_needs_from_p1), p2_name))
    for i in p2_needs_from_p1:
        print("- {}".format(i))

    if p1_needs_from_p2 and p2_needs_from_p1: print()

    if len(p1_needs_from_p2) == 1:
        print(tipstring_need_singular.format(p2_name, p1_name))
    if len(p1_needs_from_p2) > 1:
        print(tipstring_need_plural.format(p2_name, len(p1_needs_from_p2), p1_name))
    for i in p1_needs_from_p2:
        print("- {}".format(i))

if __name__ == "__main__":
    main()
