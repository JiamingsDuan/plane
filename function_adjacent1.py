"""找到相邻business_id的索引"""


def find_adjacent_duplicates(lst):
    result = []
    for i in range(len(lst) - 1):
        if lst[i] == lst[i + 1]:
            result.append((i, i + 1))
    return result
