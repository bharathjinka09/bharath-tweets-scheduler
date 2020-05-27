import gspread

gc = gspread.service_account(filename='../sheets.json')
sh = gc.open_by_key('1TzIUmBSEVeLQjCkTnZ4cr2Y8oWQPSGgYFEUQrGGcSGY')
worksheet = sh.sheet1

# get data
res = worksheet.get_all_records()
print(res)

rows = worksheet.get_all_values()
print(rows)

first_row = worksheet.row_values(1)
print(first_row)

first_column = worksheet.col_values(1)
print(first_column)

cell_value = worksheet.get('A2')
print(cell_value)

cell_value_range = worksheet.get('A2:C2')
print(cell_value_range)

# create data
user = ['Prabhas', 35, 'Italy']
# worksheet.insert_row(user, 3)

# append row
# worksheet.append_row(user)

# update cell
worksheet.update_cell(6,2,40)

# delete rows
worksheet.delete_rows(3)
