import os

copied_list = os.listdir('/media/secure_volume/output/')

hold_list = os.listdir('/media/secure_volume/holding_folder/')

miss_list = []

clean_copied_list = []

clean_hold_list = []

for item1 in copied_list:
    item_name = item1[:-5]
    clean_copied_list.append(item_name)

for item2 in hold_list:
    hold_item_name = item2[:-4]
    clean_hold_list.append(hold_item_name)

for item3 in clean_hold_list:
    if item3 in clean_copied_list:
        continue
    else:
        miss_list.append(item3)

print(str(len(miss_list)),'files not extracted.')
