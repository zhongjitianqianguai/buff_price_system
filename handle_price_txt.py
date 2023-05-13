import datetime
import os

txt = os.listdir('linux_arm/txt')
for file in txt:
    with open('linux_arm/txt/' + file, 'r+') as f:
        lines = f.readlines()
        first_line = lines[0]
        url = first_line.split(':')[0]
        expect_price = first_line.split(':')[1]
        lowest_price_in_txt = 100000
        lines.pop(0)
        for line in lines:
            print(line)
            price_data = line.split(';')
            # # 获取对应天数的历史价格
            if lowest_price_in_txt > float(
                    price_data[1].split('¥')[1].replace(" ", "").replace("\n", "")):
                lowest_price_in_txt = float(
                    price_data[1].split('¥')[1].replace(" ", "").replace("\n", ""))
        new_expect_price = str(lowest_price_in_txt/2)
        f.seek(0)
        f.write(url + ":" + new_expect_price + '\n' + ''.join(lines[1:]))
        f.truncate()
