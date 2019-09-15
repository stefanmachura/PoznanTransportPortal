def natural_minutes(m):
    """
    function checking the last digit of a number in order to return the right case of the word minuta
    """
    if m % 10 in (2, 3, 4):
        return "minuty"
    else:
        return "minut"


def natural_hours(h):
    if h % 10 in (2, 3, 4):
        return "godziny"
    else:
        return "godzin"


def natural_time(m):
    if m < 60:
        return str(m) + " " + natural_minutes(m)
    else:
        h = 0
        while m > 60:
            h += 1
            m -= 60
        return f"{str(h)} {natural_hours(h)} {str(m)} {natural_minutes(m)}"
