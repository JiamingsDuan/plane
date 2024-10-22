"""初版的基础路径判断函数"""


# first function determine the route belong to label
def determine_label(starting, ending):
    if starting == '042E0102' and ending == '042E0117':
        label = 'BRT_0401'
    # 042E0115-042E0117
    elif starting == '042E0115' and ending == '042E0117':
        label = 'BRT_0402'
    # 042E0211-042E0223
    elif starting == '042E0211' and ending == '042E0223':
        label = 'BRT_0403'
    # 042E0212-042E0223
    elif starting == '042E0212' and ending == '042E0223':
        label = 'BRT_0404'
    # 042E0102-01010915
    elif starting == '042E0102' and ending == '01010915':
        label = 'BRT_0405'
    # 042E0102-01010916
    elif starting == '042E0102' and ending == '01010916':
        label = 'BRT_0406'
    # 042E0102-01010917
    elif starting == '042E0102' and ending == '01010917':
        label = 'BRT_0407'
    # 042E0115-01010915
    elif starting == '042E0115' and ending == '01010915':
        label = 'BRT_0408'
    # 042E0115-01010916
    elif starting == '042E0115' and ending == '01010916':
        label = 'BRT_0409'
    # 042E0115-01010917
    elif starting == '042E0115' and ending == '01010917':
        label = 'BRT_040A'
    # 042E0211-01010915
    elif starting == '042E0211' and ending == '01010915':
        label = 'BRT_040B'
    # 042E0211-01010916
    elif starting == '042E0211' and ending == '01010916':
        label = 'BRT_040C'
    # 042E0211-01010917
    elif starting == '042E0211' and ending == '01010917':
        label = 'BRT_040D'
    # 042E0212-01010915
    elif starting == '042E0212' and ending == '01010915':
        label = 'BRT_040E'
    # 042E0212-01010916
    elif starting == '042E0212' and ending == '01010916':
        label = 'BRT_040F'
    # 042E0212-01010917
    elif starting == '042E0212' and ending == '01010917':
        label = 'BRT_040G'
    # 042E0102-01010903
    elif starting == '042E0102' and ending == '01010903':
        label = 'BRT_040H'
    # 042E0115-01010903
    elif starting == '042E0115' and ending == '01010903':
        label = 'BRT_040I'
    # 042E0211-01010903
    elif starting == '042E0211' and ending == '01010903':
        label = 'BRT_040J'
    # 042E0212-01010903
    elif starting == '042E0212' and ending == '01010903':
        label = 'BRT_040K'
    # 042E0105-042E0117
    elif starting == '042E0105' and ending == '042E0117':
        label = 'BRT_040L'
    # 042E0105-042E0223
    elif starting == '042E0105' and ending == '042E0223':
        label = 'BRT_040M'
    # 042E0105-01010915
    elif starting == '042E0105' and ending == '01010915':
        label = 'BRT_040N'
    # 042E0105-01010916
    elif starting == '042E0105' and ending == '01010916':
        label = 'BRT_040O'
    # 042E0105-01010917
    elif starting == '042E0105' and ending == '01010917':
        label = 'BRT_040P'
    # 162R0300-01010915
    elif starting == '162R0300' and ending == '01010915':
        label = 'BRT_040Q'
    # 162R0300-01010916
    elif starting == '162R0300' and ending == '01010916':
        label = 'BRT_040R'
    # 042E0200-042E0224
    elif starting == '042E0200' and ending == '042E0224':
        label = 'BRT_040S'
    # 042E0212-042E0224
    elif starting == '042E0212' and ending == '042E0224':
        label = 'BRT_040T'
    # 042E0211-042E0224
    elif starting == '042E0211' and ending == '042E0224':
        label = 'BRT_040U'
    # 042E0200-01010903
    elif starting == '042E0200' and ending == '01010903':
        label = 'BRT_040V'
    # 042E0105-042E0224
    elif starting == '042E0105' and ending == '042E0224':
        label = 'BRT_040W'
    # 042E0200-01010600
    elif starting == '042E0200' and ending == '01010600':
        label = 'BRT_040X'
    # 042E0219-042E0224
    elif starting == '042E0219' and ending == '042E0224':
        label = 'BRT_040Y'
    # 042E0201-042E0224
    elif starting == '042E0201' and ending == '042E0224':
        label = 'BRT_040Z'
    # 162R0300-01010903
    elif starting == '162R0300' and ending == '01010903':
        label = 'BRT_0410'
    # 16200100-01010915
    elif starting == '16200100' and ending == '01010915':
        label = 'BRT_0411'
    # 16200100-01010916
    elif starting == '16200100' and ending == '01010916':
        label = 'BRT_0412'
    # 16240100-01010915
    elif starting == '16200100' and ending == '01010915':
        label = 'BRT_0413'
    # 16240100-01010916
    elif starting == '16240100' and ending == '01010916':
        label = 'BRT_0414'
    # 162R0101-01010915
    elif starting == '162R0101' and ending == '01010915':
        label = 'BRT_0415'
    # 162R0101-01010916
    elif starting == '162R0101' and ending == '01010916':
        label = 'BRT_0416'
    # 162R0101-01010917
    elif starting == '162R0101' and ending == '01010917':
        label = 'BRT_0417'
    # startID-nav
    elif starting in start_list and ending == 'nav':
        label = 'BRT_040Other'
    else:
        # print(starting, ending)
        label = '-'

    return label


start_list = ['042E0102', '042E0105', '042E0115',
              '042E0200', '042E0201', '042E0211',
              '042E0212', '042E0219', '162R0300',
              '16200100', '16200101', '16240100', '162R0101']
