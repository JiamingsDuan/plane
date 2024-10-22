def find_adjacent_duplicates_index(lst):
    return [i for i in range(len(lst)) if
            i == 0 or lst[i] != lst[i - 1]]


def find_adjacent_duplicates(lst):
    return [lst[i] for i in range(len(lst)) if
            i == 0 or lst[i] != lst[i - 1]]


