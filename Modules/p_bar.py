import time, logging
from pyrogram.errors import FloodWait
from datetime import timedelta


class Timer:
    def __init__(self, time_between=5):
        self.start_time = time.time()
        self.time_between = time_between

    def can_send(self):
        if time.time() > (self.start_time + self.time_between):
            self.start_time = time.time()
            return True
        return False


#lets do calculations
def hrb(value, digits= 2, delim= "", postfix=""):
    """Return a human-readable file size.
    """
    if value is None:
        return None
    chosen_unit = "B"
    for unit in ("𝐊𝐁", "𝐌𝐁", "𝐆𝐁", "𝐓𝐁"):
        if value > 1000:
            value /= 1024
            chosen_unit = unit
        else:
            break
    return f"{value:.{digits}f}" + delim + chosen_unit + postfix

def hrt(seconds, precision = 0):
    """Return a human-readable time delta as a string.
    """
    pieces = []
    value = timedelta(seconds=seconds)
    

    if value.days:
        pieces.append(f"{value.days}d")

    seconds = value.seconds

    if seconds >= 3600:
        hours = int(seconds / 3600)
        pieces.append(f"{hours}h")
        seconds -= hours * 3600

    if seconds >= 60:
        minutes = int(seconds / 60)
        pieces.append(f"{minutes}m")
        seconds -= minutes * 60

    if seconds > 0 or not pieces:
        pieces.append(f"{seconds}s")

    if not precision:
        return "".join(pieces)

    return "".join(pieces[:precision])


timer = Timer()

# designed by https://t.me/Stormy_thor
async def progress_bar(current, total, reply, start, CreditName):
    if timer.can_send():
        now = time.time()
        diff = now - start
        if diff < 1:
            return
        else:
            perc = f"{current * 100 / total:.1f}%"
            elapsed_time = round(diff)
            speed = current / elapsed_time
            

            remaining_bytes = total - current
            if speed > 0:
                speed += 7 * 1024 * 1024  # Adding extra 7 MB to the speed
                eta_seconds = remaining_bytes / speed
                eta = hrt(eta_seconds, precision=1)
            else:
                eta = "-"
            
            sp = str(hrb(speed)) + "/s"
            tot = hrb(total)
            cur = hrb(current)
            
            bar_length = 10
            completed_length = int(current * 10 / total)
            remaining_length = bar_length - completed_length
            progress_bar = "▰" * completed_length + "▱" * remaining_length
            
            try:
                text =(
                    f"╭━━━ 𝙐𝙥𝙡𝙤𝙖𝙙𝙞𝙣𝙜 ━━➣\n"
                    f"┃  {progress_bar} <b>({perc})</b>\n"
                    f"┣⪼ 𝙎𝙥𝙚𝙚𝙙 ⚡ ➠ {sp}\n"
                    f"┣⪼ 𝙇𝙤𝙖𝙙𝙚𝙙 🗂️ ➠ {cur}\n"
                    f"┣⪼ 𝙎𝙞𝙯𝙚 🧲 ➠ {tot}\n"
                    f"┣⪼ 𝙀𝙏𝘼 ⏳ ➠ {eta}\n"
                    f"┣⪼ <b>{CreditName}</b>\n"
                    f"╰━━━━━━━━━━━━━━━➣")
                await reply.edit(text=text, disable_web_page_preview=True)
            except FloodWait as e:
                logging.info(e.value)
                time.sleep(e.value)
                
