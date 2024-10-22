import random


def generate_hex_colors(num_colors):
    hex_chars = '0123456789abcdef'
    color_list = []
    for _ in range(num_colors):
        color = '#' + ''.join(random.choice(hex_chars) for _ in range(6))
        color_list.append(color)
    return color_list


def generate_random_coordinates(num_points, x1, x2, y1, y2):
    x_range, y_range = (x1, x2), (y1, y2)
    coordinates = []
    for _ in range(num_points):
        x = random.uniform(x_range[0], x_range[1])
        y = random.uniform(y_range[0], y_range[1])
        coordinates.append((x, y))
    return coordinates


def slice_data(df, refer_col, slice_col, ids):
    index_list = df[df[refer_col] == ids].index.to_list()
    business_time_list = df.loc[index_list, slice_col].to_list()
    return {ids: sorted(business_time_list)}
