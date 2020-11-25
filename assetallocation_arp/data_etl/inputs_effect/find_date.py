"""
Find a date in a range of dates as Excel does
"""


def find_date(dates_set, pivot):
    flag = False
    # Initialization to start the while loop
    counter = 0
    date = dates_set[0]

    while pivot > date:
        counter += 1
        if counter >= len(dates_set):
            # Reach the end of the dates_set list
            flag = True
            break
        date = dates_set[counter]
    else:
        if pivot == date:
            t_start = pivot
        else:
            t_start = dates_set[counter - 1]

    # End of the list, we set the date to the last date
    if flag:
        t_start = dates_set[-1]

    return t_start