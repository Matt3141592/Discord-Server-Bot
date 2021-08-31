import datetime, discord

def time_ago_readable(input_days):
    difference_days  = (datetime.datetime.today() - input_days).days
    times = {
        "year":difference_days//365,
        "month":(difference_days%365)//30,
        "day":(difference_days%365)%30
    }
    times_list = []
    for i in times:
        if times[i] != 0:
            if times[i] != 1:
                times_list.append(f"{times[i]} {i}s")
            else:
                times_list.append(f"{times[i]} {i}")
    
    return ", ".join(times_list)


async def get_id_from_thread(channel):
    async for message in channel.history(oldest_first=True, limit=1):
        try:
            user_id = message.content.split("**")[3]
        except IndexError as e:
            return None
    return int(user_id)
