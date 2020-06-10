sql_results = ['FE_Lot_ID', 'BE_Lot_ID', 'Assembly_Config', 'Picking_Sorts', '#01']
columnNames = (('BKE051000', 'BKE051E60', 'x16', '01~11, 16~21', '1'), ('BKE051000', 'BKE051E61', 'x16', '16~21', None), ('BKE051000', 'BKE051E81', 'x8', '01~11', None))
for col in columnNames:
    if col[len(col) - 1] == '1':
        print(col)