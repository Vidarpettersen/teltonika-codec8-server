from datetime import datetime, timezone, timedelta
import os

def Log(message):
    timezone(timedelta(hours=2))
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_date = now.date()
    msg = f"{current_time} {message}"

    if not os.path.isdir("log/"):
        os.mkdir("log/")

    with open(f'log/{current_date}.log', 'a') as fo:
        fo.write(f'{msg}\n')
    print(msg)