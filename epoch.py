import datetime
from dateutil.relativedelta import relativedelta
today = datetime.datetime.today()

# Gets previous date 
def getlastdate(day, month, epoch=True) :
    """Day is day of the month, month is how many 
    months ago, epoch returns as unix epoch time"""
    day = today.replace(day=day,hour=0, minute=0)
    date = day - relativedelta(months=month)
    if epoch :
        date = to_epoch(date)
    return date

# Converts to Epoch time in Miliseconds
def to_epoch(month):
    epoch = month.timestamp()
    return int(epoch  * 1000)

# Convert SDP Request Value Time to Seconds
def to_seconds(date_value):
    date_value = int(date_value) // 1000