from glob import glob



def get_file_name(f_base, DATE, NEW_FILES=False):
    if not NEW_FILES:
        return f_base + '.csv'

    # Split off old date portion
    f_info = f_base.split('2020')
    f_root = f_info[0]
    #print(f_base)
    #print(f_root)
    f_root = f_root.replace('unmet', 'input_unmet')
    #print(f_root)
    f_root += DATE
    #print(f_root)
    if 'constant' in f_root: 
        if '1-' in f_root or '2-' in f_root:
            root_info = f_root.split('/')
            root_info[-1] = root_info[-1].replace('unmet_demand', 'unmet_demand_constant')
            f_root = '/'.join(root_info)
        else:
            f_root = f_root.replace('demand_constant', 'demand-constant')
    f_root = f_root.replace('-only', '')
    #print(f_root)
    files = glob(f_root+'*.csv')
    #print(files)
    assert(len(files) == 1)
    return files[0]
