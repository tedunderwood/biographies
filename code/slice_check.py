import os
import pandas as pd

slice_df = pd.read_csv('media/secure_volume/natalie/slices/slice_0.tsv',sep='\t', header=0)
slice_df.columns = ['a', 'b', 'c', 'd', 'e']
slice_df.head()

file_list = []

for item in slice_df['a']:
    file_list.append(item)

# print(file_list)
print(len(file_list), 'files from slice file.')
# # print(file_list)

copied_list = os.listdir('media/secure_volume/output/')
print(len(copied_list), 'files were copied.')

miss_list = []

clean_copied_list = []

for item1 in copied_list:
    item_name = item1[:-5]
    clean_copied_list.append(item_name)

for item3 in file_list:
    if item3 in clean_copied_list:
        continue
    else:
        miss_list.append(item3)

print(str(len(miss_list)),'files not extracted.')
