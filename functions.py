def filter_names(fighter_list, text):
    filtered_fighters1 = [fighter for fighter in fighter_list if text.lower() in fighter.lower()]
    return filtered_fighters1