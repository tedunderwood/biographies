import os

copied_list = os.listdir('/media/secure_volume/output/')

hold_list = os.listdir('/media/secure_volume/holding_folder/')

miss_list = []

for item in copied_list:
    # print(item)
    if item in hold_list:
        continue
    else:
        miss_list.append(item)

print(len(miss_list),'files not extracted.')
