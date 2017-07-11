import os

copied_list = os.listdir('/media/secure_volume/output/')

hold_list = os.listdir('/media/secure_volume/holding_folder/')

miss_list = []

clean_copied_list = []

clean_hold_list = []

for item in copied_list:
    item_name = item[:-5]
    clean_copied_list.append(item_name)

for item in hold_list:
    hold_item_name = item[:-4]
    clean_hold_list.append(hold_item_name)

for item in clean_copied_list:
    if item in clean_hold_list:
        continue
    else:
        miss_list.append(item)

print(str(len(miss_list)),'files not extracted.')
