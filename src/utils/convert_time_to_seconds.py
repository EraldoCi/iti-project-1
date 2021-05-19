def convert_time_to_seconds(time):
    minutes, seconds = time.split(":")
    return round(int(minutes) * 60 + int(seconds), 2)
