# // SELECT * from times WHERE month == 3 AND day >= 10 OR month > 3 AND month < 11;

# how to check if dst
# target_date = datetime.datetime.strptime(arg_date, "%Y-%m-%d")
# time_zone = pytz.timezone('US/Eastern')
# dst_date = time_zone.localize(target_date, is_dst=None)
# est_hour = 24
# if bool(dst_date.dst()) is True:
#     est_hour -= 4
# else:
#     est_hour -= 5

# https://github.com/achaudhry/adhan