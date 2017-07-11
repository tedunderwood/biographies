import os

cop_list = os.listdir('/media/secure_volume/output/')

hold_list = os.listdir('/media/secure_volume/2holding_folder/')

miss_list = []

clean_cop_list = []

clean_hold_list = []

for cop_item in cop_list:
    # file suffix is .book for these files
    cop_item_name = str(cop_item[:-5]) # removing extension
    clean_cop_list.append(cop_item_name)

for hold_item in hold_list:
    # file suffix is .zip for these fiels
    hold_item_name = str(hold_item[:-4]) # removing file extension
    clean_hold_list.append(hold_item_name)

for check_item in clean_hold_list:
    if check_item in clean_cop_list:
        continue
    else:
        miss_list.append(check_item)

print(str(len(miss_list)),'files not extracted.')
