from steam_api import steam_item_data
from steam_api import steam_player_items

TF2 = 440
TF2_IRRELEVANT_ITEMS = ( "saxxy", "class_token", "slot_token", "tf_wearable",
            "no_entity", "map_token", "tool", "tf_powerup_bottle",
                    "upgrade", "craft_item", "bundle", "supply_crate", "")

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

