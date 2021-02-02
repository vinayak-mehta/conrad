import os

window_width = int(os.popen("stty size", "r").read().split()[1])
max_lengths = {
    "id": 2,
    "Name": 4,
    "Website": 7,
    "City": 4,
    "State": 5,
    "Country": 7,
    "Start Date": 10,
    "End Date": 8,
    "padding": 25,
}

def get_optimal_name_length(events):
    max_lengths = update_max_lengths(events)
    max_width_needed = sum(max_lengths.values())
    length_to_reduce = max_width_needed - window_width
    optimal_name_length = max_lengths["Name"] - length_to_reduce
    optimal_name_length_no_url = optimal_name_length + max_lengths["Website"]
    return optimal_name_length, optimal_name_length_no_url

def update_max_lengths(events):
    for event in events:
        max_lengths["id"] = max(max_lengths["id"], len(event.id))
        max_lengths["Name"] = max(max_lengths["Name"], len(str(event.name)))
        max_lengths["Website"] = max(max_lengths["Website"], len(str(event.url)))
        max_lengths["City"] = max(max_lengths["City"], len(str(event.city)))
        max_lengths["State"] = max(max_lengths["State"], len(str(event.state)))
        max_lengths["Country"] = max(max_lengths["Country"], len(str(event.country)))
        max_lengths["Start Date"] = max(max_lengths["Start Date"], len(event.start_date.strftime("%Y-%m-%d")))
        max_lengths["End Date"] = max(max_lengths["End Date"], len(event.end_date.strftime("%Y-%m-%d")))
    return max_lengths
