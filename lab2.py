import pandas as pd

def table(path):
        df = pd.read_csv(path,index_col=False, header=1,
             names=['year', 'week', 'provinceID', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI'])
        print('Sorted by ID of the region')
        print ('ID is {}'.format(ident))
        print (df)

for ident in range(1, 28):
    path='2018_06_12-02h_vhi_id_%02d.csv' % ident
    table(path)
