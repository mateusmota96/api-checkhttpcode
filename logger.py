import datetime


def ErrorLog(type, errormessage):
    type = "["+ type +"]-"
    timenow = datetime.datetime.now()
    day = timenow.strftime("%d")
    month = timenow.strftime("%m")
    year = timenow.strftime("%Y")
    str_log = str(year) + "-" + str(day) + "-" + str(month) + ".log"
    file = open(str_log, "a")
    date_time_now = "["+timenow.strftime("%X")+"]-"
    errormessage = "[" + errormessage + "]"
    file.write(type + date_time_now + errormessage + "\n")
    file.close()