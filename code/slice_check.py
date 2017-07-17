import os
import pandas as pd

slice_df = pd.read_csv('/Users/rdubnic2/Documents/underwood-research/test_slice.tsv',sep='\t', header=0)
slice_df.columns = ['a', 'b', 'c', 'd', 'e']
slice_df.head()

temp_list = []

for item in slice_df['a']:
    temp_list.append(item)

print(temp_list)

file_list = []
    
for file in temp_list:
    file = file + '.zip'
    file_list.append(file)
    
# print(file_list)
print(len(file_list), 'files from slice file.')
# # print(file_list)

copied_list = os.listdir('/Users/rdubnic2/Documents/underwood-research/output/')
print(len(copied_list), 'files were copied.')

miss_list = []

clean_file_list = []
clean_copied_list = []

for item1 in copied_list:
    item_name = item1[:-5]
    clean_copied_list.append(item_name)

for item2 in file_list:
    hold_item_name = item2[:-4]
    clean_file_list.append(hold_item_name)

for item3 in clean_file_list:
    if item3 in clean_copied_list:
        continue
    else:
        miss_list.append(item3)

print(str(len(miss_list)),'files not extracted.')
