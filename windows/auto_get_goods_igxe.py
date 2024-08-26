from selenium import webdriver
from selenium.common import NoSuchElementException, StaleElementReferenceException, WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import buff_sql

options = webdriver.FirefoxOptions()
# 去掉"chrome正受到自动化测试软件的控制"的提示条
# options.add_argument('--headless')
options.add_argument("--lang=zh_CN")
options.binary_location = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
driver = webdriver.Firefox(service=Service('webdriver/geckodriver.exe'),
                           options=options)
driver.set_page_load_timeout(300)
driver.get('https://www.igxe.cn/market/csgo')
driver.implicitly_wait(10)
all_goods_id = buff_sql.get_all_goods_id()

max_page = 0

bu = ["AK-47", "M4A4", "加利尔", "AUG", "SG 553", "AWP", "SSG 08", "M4A1", "SCAR-20", "G3SG1", "法玛斯"]
knifes = ["蝴蝶刀", "M9刺刀", "爪子刀", "廓尔喀刀", "刺刀", "锯齿爪刀", "流浪者匕首", "折叠刀", "短剑", "海豹短刀",
          "熊刀", "猎杀者匕首", "系绳匕首", "求生匕首", "弯刀", "暗影双匕", "鲍伊猎刀", "穿肠刀", "折刀"]
hands = ["手套", "运动手套", "专业手套", "摩托手套", "裹手", "狂牙手套", "九头蛇手套", "血猎手套"]
pistols = ["沙漠之鹰", "USP 消音版", "格洛克 18 型", "P2000", "P250", "FN57", "R8 左轮手枪", "Tec-9", "双持贝瑞塔",
           "CZ75", "电击枪", "", "", "", ]
smg = ["MP9", "MAC-10", "UMP-45", "P90", "MP7", "PP-野牛", "MP5-SD"]
shotguns = ["XM1014", "MAG-7", "截短霰弹枪", "新星", ]
machinegun = ["M249", "内格夫", ]
driver.implicitly_wait(10)
pages = driver.find_element(By.CLASS_NAME, "el-pager").find_elements(By.TAG_NAME, "li")
max_page = int(pages[-1].text)
print("max_page: " + str(max_page))
page = 2
if max_page > 0:
    for i in range(1, max_page):
        print("page: " + str(i))
        while True:
            try:
                li_cards = driver.find_element(By.CLASS_NAME, "card_csgo").find_elements(By.TAG_NAME, "li")
                for li in li_cards:
                    url = li.find_element(By.TAG_NAME, "a").get_attribute("href").split("?")[0]
                    if 'page' not in url:
                        goods_id = url.split("/")[-1]
                        if goods_id not in all_goods_id:
                            price = float(
                                li.find_element(By.TAG_NAME, "p").find_element(By.TAG_NAME, "strong").text.replace("¥ ",
                                                                                                                   ""))
                            # print("price: " + str(price))
                            name = li.find_element(By.TAG_NAME, "h3").find_element(By.TAG_NAME, "a").text
                            # print("name: " + name)
                            img_url = li.find_element(By.TAG_NAME, "img").get_attribute("src")
                            # print("image_url: " + img_url)
                            category = ""
                            if "（全息）" in name:
                                category = "全息"
                            if "（金色）" in name:
                                category = "金色"
                            if "武器箱" in name:
                                category = "武器箱"
                            if "音乐盒" in name:
                                category = "音乐盒"
                            if "胶囊" in name:
                                category = "胶囊"
                            for gun in bu:
                                if gun in name:
                                    category = "步枪"
                                    break
                            for knife in knifes:
                                if knife in name:
                                    category = "匕首"
                                    break
                            for hand in hands:
                                if hand in name:
                                    category = "手套"
                                    break
                            for sm in smg:
                                if sm in name:
                                    category = "微型冲锋枪"
                                    break
                            for shotgun in shotguns:
                                if shotgun in name:
                                    category = "霰弹枪"
                                    break
                            for machin in machinegun:
                                if machin in name:
                                    category = "机枪"
                                    break
                            sale_count = (li.find_element(By.TAG_NAME, "p").find_element(By.TAG_NAME,
                                                                                         "span").text
                            .replace("+件在售",
                                     "").replace(
                                "件在售", ""))
                            if category == "":
                                break
                            elif category == "步枪" and price < 10 or int(sale_count) < 1:
                                break
                            elif category == "手套" and price > 50000 or int(sale_count) < 5:
                                break
                            elif category == "匕首" and price > 50000 or int(sale_count) < 1:
                                break
                            elif category == "手枪" and price < 10 or int(sale_count) < 2:
                                break
                            elif category == "狙击步枪" and price < 10 or int(sale_count) < 2:
                                break
                            elif category == "微型冲锋枪" and int(sale_count) < 2:
                                break
                            elif category == "机枪" and price < 20 or int(sale_count) < 5:
                                break
                            elif category == "霰弹枪" and price < 10 or int(sale_count) < 2:
                                break
                            elif category == "金色" and int(sale_count) < 1:
                                break
                            elif category == "全息" and int(sale_count) < 1:
                                break
                            elif category == "武器箱" and int(sale_count) < 2:
                                break
                            elif category == "音乐盒" and int(sale_count) < 2:
                                break
                            # elif category == "胶囊" and int(sale_count) < 2:
                            #     break
                            buff_sql.add_new_good(name, goods_id, category, img_url, price, price)
                            buff_sql.create_new_record_table(goods_id)
                            print("添加 name: " + name)
                time.sleep(2)
                pages = driver.find_element(By.CLASS_NAME,
                                            "pager.card-pager.light-theme.simple-pagination").find_elements(By.TAG_NAME,
                                                                                                            "li")
                for page in pages:
                    if page.text.replace("\n", "") == "下一页":
                        page.find_element(By.TAG_NAME, "a").click()
                        break
                time.sleep(3)
                break
            except NoSuchElementException:
                continue
            except StaleElementReferenceException:
                continue
