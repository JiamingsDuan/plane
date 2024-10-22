# second function: A algorithm to slice the [1, -1]


def find_sub_list(lst):
    sub_list = []
    indices = []
    i = 0
    while i < len(lst):
        if lst[i] == 1:
            start = i
            while i < len(lst) and lst[i] != -1:
                i += 1
            end = i
            sub_list.append(lst[start:end+1])
            indices.append((start, end))
        i += 1
    return sub_list, indices


def find_segments(lst):
    segments = []
    start = None
    for i, value in enumerate(lst):
        if value == '1' and start is None:
            start = i
        elif value == '-1' and start is not None:
            segments.append((start, i))
            start = None
    return segments
