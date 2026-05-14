import time

SECONDS_PER_DAY = 86400

def calculate_mining(balance, speed, last_claim):

    now = int(time.time())

    passed = now - last_claim

    earned = passed * speed

    return round(balance + earned, 6), now
