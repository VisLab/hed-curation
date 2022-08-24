def is_number(variable):
    """ Checks if a variable is either a float of int."""
    return isinstance(variable, int) or isinstance(variable, float)


def match_label(lst, label):
    for option in label:
        if option[1] == lst:
            return option[0]


def get_indices(df, column, start, stop):
    start_event = [i for (i, v) in enumerate(df[column].tolist())
                   if v in start]
    end_event = [i for (i, v) in enumerate(df[column].tolist())
                 if v in stop]

    lst = []

    next_start = start_event[0]
    while 1:
        try:
            next_end = find_next(next_start, end_event)
            lst.append((next_start, next_end))
            next_start = find_next_start(next_end, start_event)
        except IndexError:
            break

    return lst


def split_consecutive_parts(lst):
    """From a list of indexes, create a list of list with each sublist
    containing a consecutive series in the original list"""
    new_list = []
    consecutive_list = []
    for i in range(0, len(lst)-1):
        if lst[i]+1 == lst[i+1]:
            consecutive_list.append(lst[i])
        else:
            consecutive_list.append(lst[i])
            new_list.append(consecutive_list)
            consecutive_list = []
    new_list.append(consecutive_list)
    return new_list


def tuple_to_range(tuple_list, inclusion):
    # change normal range inclusion behaviour based on user input
    [k, m] = [0, 0]
    if inclusion[0] == 'exclude':
        k += 1
    if inclusion[1] == 'include':
        m += 1

    range_list = []
    for tup in tuple_list:
        range_list.append([*range(tup[0] + k, tup[1] + m)])
    return range_list


def find_next(v, lst):
    return [x for x in sorted(lst) if x > v][0]


def find_next_start(v, lst):
    return [x for x in sorted(lst) if x >= v][0]