import time
import json
import threading
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# 讀取 JSON 配置文件
with open('config.json', 'r', encoding='utf-8') as config_file:
    config = json.load(config_file)

def format_time(time_str):
    # 取得小時數和分鐘數
    hour = int(time_str[:2])  # 提取前兩位作為小時
    minute = int(time_str[2:])  # 提取後兩位作為分鐘

    if minute == 0:  # 如果分鐘是0，不顯示「分」
        minute_str = ''
    else:
        minute_str = f'{minute}分'

    if hour < 12:  # 上午
        formatted_time = f'上午{hour}時{minute_str}'
    else:  # 下午
        formatted_hour = hour - 12 if hour > 12 else hour  # 將下午的時間轉換為12小時制
        formatted_time = f'下午{formatted_hour}時{minute_str}'

    return formatted_time


def book_facility(booking):
    Time = booking['選取時段']
    Account = booking['帳號']
    Password = booking['密碼']
    Venue = booking['體育館']
    Venue_Type = booking['設施']
    Payment = booking['付款方式']
    nameOnCard = booking['持卡人姓名']
    number = booking['卡號']
    expiryMonth = booking['到期月']
    expiryYear = booking['到期年']
    securityCode = booking['安全碼']

    # 為每個 WebDriver 創建一個新的用戶配置
    options = webdriver.FirefoxOptions()
    options.add_argument(f"--user-data-dir={Account}")  # 使用帳號作為資料夾名稱

    driver = webdriver.Firefox(options=options)
    driver.get('https://www.smartplay.lcsd.gov.hk/home?lang=tc')
    wait = WebDriverWait(driver, 10)

    def Login():
        # 等待并找到帐号输入框（第一个 el-input__inner）
        account_element = wait.until(EC.visibility_of_element_located((By.XPATH, '(//input[@class="el-input__inner"])[1]')))
        account_element.send_keys(Account)

        # 等待并找到密码输入框（第二个 el-input__inner）
        password_element = wait.until(EC.visibility_of_element_located((By.XPATH, '(//input[@class="el-input__inner"])[2]')))
        password_element.send_keys(Password)

        # 使用按钮的文本来定位
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '登錄')]"))).click()


    def Search_Facility():
        Venue_elem = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), '設施')]")))
        driver.execute_script("arguments[0].click();", Venue_elem)
        time.sleep(1.2)
        Venue_elem = wait.until(EC.visibility_of_element_located((By.XPATH, "(//div[@class='text'])")))
        driver.execute_script("arguments[0].click();", Venue_elem)

        input_element = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@data-v-21e43f8c]//input")))
        input_element.send_keys(Venue)

        time.sleep(2)
        wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div/div[2]/div[2]/div[2]/div/div/div/div/div/div[3]/div[1]/div[2]/div[2]/div/div/div[3]/div/div'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div/div[2]/div[2]/div[2]/div/div/div/div/div/div[3]/div[3]/div'))).click()

    def select_time():
        morning = ['0700','0730','0800','0830','0900','0930','1000','1030','1100','1130']
        afternoon = ['1200','1300','1400','1500','1600','1700','1230','1330','1430','1530','1630','1730']
        night = ['1800','1900','2000','2100','2200','1830','1930','2030','2130','2230']

        if Time in morning:
            pass
        elif Time in afternoon:
            time.sleep(1.5)
            afternoon_button = wait.until(EC.visibility_of_element_located((By.XPATH, "(//div[@class='t-center'])[2]")))
            driver.execute_script("arguments[0].click();", afternoon_button)
        elif Time in night:
            time.sleep(1.5)
            night_button = wait.until(EC.visibility_of_element_located((By.XPATH, "(//div[@class='t-center'])[3]")))
            driver.execute_script("arguments[0].click();", night_button)
        else:
            print('Error Time Set')
    
    def select_Payment(Payment):
        
        payment_methods_element = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[1]/div/div/div/div[2]')
        payment_methods = payment_methods_element.find_elements(By.XPATH, ".//div[@class='payment-method-box']")
        
        for method in payment_methods:
            span_elements = method.find_elements(By.XPATH, './/span')
            for span in span_elements:
                if span.text == Payment:
                    method.find_element(By.XPATH, ".//img[@class='mr10 pointer' and @alt='smartplay']").click()
    
    def google_pay():
        pass

    def visa_master_jcb_pay():
        name_iframe_element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="#name-on-card-exactly-shown-on-card"]')))
        driver.switch_to.frame(name_iframe_element)
        nameOnCard_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="nameOnCard"]')))
        nameOnCard_element.send_keys(nameOnCard)
        driver.switch_to.default_content()  # Switch back to the main content

        # Switch to the iframe for the card number
        number_iframe_element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="#card-number"]')))
        driver.switch_to.frame(number_iframe_element)
        number_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="number"]')))
        number_element.send_keys(number)
        driver.switch_to.default_content()  # Switch back to the main content

        # Switch to the iframe for the expiry month
        expiryMonth_iframe_element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="#expiry-month"]')))
        driver.switch_to.frame(expiryMonth_iframe_element)
        expiryMonth_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="expiryMonth"]')))
        expiryMonth_element.send_keys(expiryMonth)
        driver.switch_to.default_content()  # Switch back to the main content

        # Switch to the iframe for the expiry year
        expiryYear_iframe_element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="#expiry-year"]')))
        driver.switch_to.frame(expiryYear_iframe_element)
        expiryYear_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="expiryYear"]')))
        expiryYear_element.send_keys(expiryYear)
        driver.switch_to.default_content()  # Switch back to the main content

        # Switch to the iframe for the security code
        securityCode_iframe_element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="#security-code"]')))
        driver.switch_to.frame(securityCode_iframe_element)
        securityCode_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="securityCode"]')))
        securityCode_element.send_keys(securityCode)
        driver.switch_to.default_content()  # Switch back to the main content

    def unionpay():
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="pay-button"]'))).click()
        number_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="cardNumber"]')))
        number_element.send_keys(number)

    def pps_pay():
        nameOnCard_element = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@name='ACCOUNTNO']")))
        nameOnCard_element.send_keys(number)
        securityCode_element = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@name='PIN']")))
        securityCode_element.send_keys(securityCode)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='TNC']"))).click()

    Login()
    Search_Facility()
    select_time()

    # 選擇設施並進行預定
    list_XPATH = '/html/body/div/div[2]/div[4]/div[2]/div/div/div[2]/div[2]/div/div[2]/div[3]'
    divs = wait.until(EC.visibility_of_all_elements_located((By.XPATH, f'{list_XPATH}/div')))

    for index, div in enumerate(divs, start=1):
        element = wait.until(EC.visibility_of_element_located((By.XPATH, f'{list_XPATH}/div[{index}]/div[1]')))
        if element.text == Venue_Type:
            available_times = []
            time_element = wait.until(EC.visibility_of_element_located((By.XPATH, f'{list_XPATH}/div[{index}]/div[2]/div/div[2]/div')))

            # 拆分字符串並去除空字符串
            time_data = [line for line in time_element.text.split('\n') if line.strip()]

            # 將時間和數量組合成新的列表，並去除重複項
            for i in range(0, len(time_data), 2):
                new_entry = [time_data[i], f"{time_data[i + 1]}張"]
                
                # 檢查新的條目是否已存在於 available_times 中
                if new_entry not in available_times:
                    available_times.append(new_entry)

            wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "el-loading-mask")))
            time.sleep(1)
            # 點擊3次，每次可能會有新數據
            for _ in range(3):
                wait.until(EC.visibility_of_element_located((By.XPATH, f'{list_XPATH}/div[{index}]/div[2]/div/div[3]/div[2]/div/img'))).click()
                
                # 再次獲取新的時間數據
                time_element = wait.until(EC.visibility_of_element_located((By.XPATH, f'{list_XPATH}/div[{index}]/div[2]/div/div[2]/div')))
                time_data = [line for line in time_element.text.split('\n') if line.strip()]
                
                # 將新的時間和數量添加到列表，並避免重複
                for i in range(0, len(time_data), 2):
                    new_entry = [time_data[i], f"{time_data[i + 1]}張"]
                    if new_entry not in available_times:
                        available_times.append(new_entry)
            
            for sub_index, (time_str, count) in enumerate(available_times):
                if time_str == format_time(Time):
                # 根據 index 構建正確的 XPath
                    if count == '0張':
                        print(f'預定失敗原因：非常抱歉，但【{Venue}】的【{Venue_Type}】在{Time}點沒有票了')
                        break
                    else:
                        time_xpath = f"{sub_index + 1}"  # 這裡用 index + 1，因為 XPath 是從1開始計數
                        if sub_index + 1 < 5:
                            for _ in range(3):
                                wait.until(EC.visibility_of_element_located((By.XPATH, f'{list_XPATH}/div[{index}]/div[2]/div/div[1]/div[2]/div/img'))).click()
                                #f'{list_XPATH}/div[7]/div[2]/div/div[1]/div[2]/div/img
                        Time_Selector = wait.until(EC.visibility_of_element_located((By.XPATH, f'{list_XPATH}/div[{index}]/div[2]/div/div[2]/div/div[{time_xpath}]/div')))
                        driver.execute_script("arguments[0].click();", Time_Selector)

                        continue_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '繼續')]")))
                        time.sleep(0.8)
                        driver.execute_script("arguments[0].click();", continue_button)

                        #檢查是否有出現error_elements
                        try:
                            error_elements = wait.until(EC.visibility_of_element_located((By.XPATH, f'/html/body/div[2]/div/div[1]/div/p')))

                            if error_elements.text == "是否需要預訂其他設施？":
                                wait.until(EC.visibility_of_element_located((By.XPATH, "(//div[@class='cancel-button'])"))).click()
                            elif error_elements:
                                print("預定失敗原因：" + error_elements.text )
                                break
                            else:
                                break
                            
                        except Exception as e:
                            pass

                        continue_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '繼續')]")))
                        driver.execute_script("arguments[0].click();", continue_button)
                        time.sleep(0.5)
                        Check_Box_1 = wait.until(EC.element_to_be_clickable((By.XPATH, "(//img[@alt='smartplay'])[2]")))
                        driver.execute_script("arguments[0].click();", Check_Box_1)
                        Check_Box_2 = wait.until(EC.element_to_be_clickable((By.XPATH, "(//img[@alt='smartplay'])[3]")))
                        driver.execute_script("arguments[0].click();", Check_Box_2)

                        #檢查是否有第三個Check_Box
                        Check_Box_3_elements = driver.find_elements(By.XPATH, "/html/body/div/div[2]/div[3]/div/div/div/div[1]/div[2]/div/div[3]/div/div[1]/img")
                        if Check_Box_3_elements:
                            Check_Box_3 = Check_Box_3_elements[0]
                            if Check_Box_3.is_displayed() and Check_Box_3.is_enabled():
                                driver.execute_script("arguments[0].click();", Check_Box_3)
                        else:
                            pass


                        time.sleep(0.8)
                        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '確認並同意')]"))).click()
                        
                        #檢查是否需要付費，若為返回設施則無須付費
                        wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "el-loading-mask")))
                        return_facility_element = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@role='button' and (contains(text(), '確認付款') or contains(text(), '返回設施'))]")))
                        return_facility_text = return_facility_element.text.strip()
                        if return_facility_text == '返回設施':
                            print(f'成功預定【{Venue}】的【{Venue_Type}】！')
                            break
                        else:
                            wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '確認付款')]"))).click()
                        
                        #選擇付款方式
                        time.sleep(0.5)
                        select_Payment(Payment)

                        if Payment != 'Google Pay':
                            wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '確認付款')]"))).click()
                        else:
                            wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[2]/div[1]/div/div/div/div[4]/img"))).click()
                        time.sleep(10)
                        
                        if Payment == 'FPS':
                            print('請掃描QR-Code')
                        elif Payment == 'Google Pay':
                            print('請輸入Google帳號')
                        elif Payment == 'JCB' or Payment == 'MasterCard' or Payment == 'Visa':
                            visa_master_jcb_pay()
                        elif Payment == 'UnionPay':
                            unionpay()
                        elif Payment == 'PPS':
                            pps_pay()
                        else:
                            print('預定失敗：此付款方式尚未建立')
                            break                    
                        
                        print(f'成功預定【{Venue}】的【{Venue_Type}】！')
                else:
                    continue
            break

# 創建線程以同時預定
threads = []
for booking in config['預訂'][1:]:
#     # 獲取預訂的運行時間
#     booking_run_time = config['預訂'][0]['運行時間']
#     booking_run_time_dt = datetime.strptime(booking_run_time, "%H%M").time()
    
#     # 創建包含當前日期和運行時間的 datetime 對象
#     now = datetime.now()
#     booking_run_time_full = datetime.combine(now.date(), booking_run_time_dt)

#     # 計算延遲時間
#     delay_seconds = (booking_run_time_full - now).total_seconds()
#     if delay_seconds > 0:
#         time.sleep(delay_seconds)

    thread = threading.Thread(target=book_facility, args=(booking,))
    threads.append(thread)
    thread.start()

# 等待所有線程完成
for thread in threads:
    thread.join()

# 22222222222222222222222222222222222222222221b31@@@@@@13b22222222222222222222222222222222222222222222
# 22222222222222222222222222222222222222222b2#.          .%1a22222222222222222222222222222222222222222
# 222222222222222222222222222222222222222a@.    ........     #2122222222222222222222222222222222222222
# 2222222222222222222222222222222222222c1   .....******.....   *21222222222222222222222222222222222222
# 222222222222222222222222222222222222a*  ....***......***....   #322222222222222222222222222222222222
# 222222222222222222222222222222222222+ ....**............***...   @c22222222cba33a1222222222222222222
# 222222222222222222222222222222222c@  ...**.................**...  #b222cb31:----.%b22222222222222222
# 22222222222222222222222222222222c%  ...**...................**...  *aa1:-.---::::-%c2222222222222222
# 2222222222222222222222222222222c%  ..**.......................**...  .--::::%1@:::.22222222222222222
# 222222222222222222222222222222c% ...**.........................**...  #%%%@2@13::::-b222222222222222
# 222222222222222222222222222221@  ..**............................***. +:+**%#2@::::-1222222222222222
# 222222222222222222222222222222  ..**................................*+ .%=%:::::::::-b22222222222222
# 22222222222222222222222222223+ ..**..................................*  *::%::::::::-122222222222222
# 222222222222222222222222222b* ...*....................................*  -::%%%%%%::::b2222222222222
# 2222222222222b3122222222222@ ...*......................................* .%::::::%%::-22222222222222
# 2222222222223* a22222222223  ..**......................................*. *:::::::%:::%1222222222222
# 2222222222c@   12222222221# ..**........................................*  %:::::::%::#@222222222222
# 222222222a#  . %2222222222 ...*..........................................* *:::::%:%::#%222222222222
# 2222222c1   .. +@22222221* ..*...........................................*  %:::%-:%::-3222222222222
# 222222a#  ..... 222222222 ...*............................................* *:::#-:#::-2222222222222
# 222211+  ...... #1222221* ..*.............................................*  ::%----::-2222222222222
# 222b%  ...***..  3222221 ...*..............................................* ###--##::-2222222222222
# 223+  ...**..*.. #1222b+ ...**.............................................* +-#-------3222222222222
# 22@  ..**....*..  122b# ......**.......******..............................*  -*------*#222222222222
# 221 ...*......*.. +@2*  .......********......******........................*. +:*-----*%222222222222
# 222 ..+.......**..     ............................**......................*. *@@.----*@222222222222
# 223  ..+.......**... ..................    .........**.....................*. +@1#.---#1222222222222
# 22b  ..+........***.......-#%:-......  *##**+   ......**.....***...........*..=#2a#.-.12222222222222
# 22c. ..+...........*.....#@##1%-.... *2%%%%##1%*  .....**....*.*...........*.. @22b@#@b2222222222222
# 222% ..+...........+....-1@1112:.... 21111111@@%2%  ....**....**....**.....*.. #22221122222222222222
# 2221 ...+..........+....%@1111@@-.. %1%212@11111@@3%  ....**.......*.......*.. *12222222222222222222
# 222a  ..+.........+....-21111112-..+#*+   @1111111@@2*  ...**.......**.....*...+%2222222222222222222
# 222c. ..+.........+....#%1b2a113-. #1%    %1111111111a@  ...**.............*... 32222222222222222222
# 2222% ..+.........+....%@13:@@13-. 212*+#1a11111111111@1+ ...**............*... 12222222222222222222
# 22222  ..+........+....@@12:%#12- *@1b@@1111111111b%%3113* ...*.............*.. @2222222222222222222
# 2222b  . +........+...*+@1b@:#@1. @11b1211111111113  +1113* ...*............*.. %2222222222222222222
# 2222c-   +........+...*+@@13:a@@. 3111 +3111111111a*  +2113+ ..*............*.. #2222222222222222222
# 222221   +        +.. *+@@@a+@3- #11b.  111111111112+  +%111 ..*............*.. #1222222222222222222
# 22222a    +       +.. .@%%@a%#+:%311a   1111111111112+ =#11@# .*............*.. *1222222222222222222
# 22222c.   ++      +... %%%%31+3@@@@13.+ 311111111@2%13*%@111@ ..*...........*.. *1222222222222222222
# 2222221    +       +   ##%3=*b1@@@@@a..#@1aab111b% *@1@@1111@ ..+...........*.. +@222222222222222222
# 222222a    +       +   **3=*c1@@a3a@11*31%#%#@111  =#1111111# ..+.****......*.. +@222222222222222222
# 2222cc2%    +      +   +=+=b1@@%2:@@@1@1b#@1@#c@-  +%111111a  ........**....*.. +%222222222222222222
# 222c**#2    ++     +    -:311@@@3-#%@111b#b1@#c%.: *@1111111 ..........**...*... 2222222222222222222
# 22c#*a#1-    +   +++    .@@11@@@1  11111b#*%*%1a.+ @111111@# ...........++..*... 1222222222222222222
# 2b2+a22@1.    +++       -21111@b:  #31111b3*311@* #b1111112  ...#%%#.....+...+.. %222222222222222222
# b*#a#122%@             .%%11111a.   %a1111111111a2b111111@# . *1%@@#1#....+..+.. *122222222222222222
# #*c2c#@223-            .%@111112     %ac111111111111@@@@12   *21111@%@....+..+..  a22222222222222222
# *32221#12@@            .@@111111     *+#b111111111b2a@@@11  .211111@@2:...+..+... @22222222222cab222
# #*c222b%c22.     #@@%. .@@1111b:   +32b++abcc111@3%.1@%@@a* 11111111@a:...+...+.. *12222222222a 1222
# b+acc2c@@2%%    %2@@2% .111111b-   2222c+=+*#321%. -1%%@@1a1b111aa@1@a=...+...+..  1222222222a* %222
# %+*#@c22@1131- -212211..111111a-  #1222c=ab3#:     %3%%@@@111112=:11@a=...+...+... +322222223*  *122
# *@2b#%221122b2:@@22222..@@1111a-. .a222a-c222@     1@%%@@11111a:::11@3:. .+....+... +22222b@  . +@22
# 2122c%@211222b**222211 .@@1111a-.. #b22%-22221    *#@@@@@1111b*+11a1@2-...+....++...  %11%.  ..  322
# *b222c%c222222aa2222@% .%@1111a-....#32 =22222    #@@@@@@1111b%b111@@1-   +     ++...      ..... 122
# ##c222112222221122212-  #%1111a----.... :c2221    111@@11111111111@@#%.   +     .++....  ....... #22
# b+%c222222222222222a%   -21111a=@1@@-....1333#   *%11111111111111@@%@-   +      ...++. ....+++.. *12
# 2%+%c2222cc222222211.   .@@111b+1***1%-.....  .. @1111111@11@@@@@@%1#    +           ++++++..+.. +%2
# 2c@*#c221b@@c22222a=    .%%111b+11***1%%@@:--....31111111@@a@@@@%2@-    ++                .. +..  22
# 222b*%222c1%%122223:.    -2111b*+2**2++****1@:..@@111111@@2:@111%-.    ++                    +    @2
# 2222@*b2222c1a12222:--.  .@@1113+*2*++*******1:-3111111@@a:......      +                      +   #1
# 2222c##c22222112211::--.  :2111a+*2*+2*******2+111111@@@@1.            +                      +   +@
# 22222b+@222222222c+::%##. .@a1111+2**2****222*+b11111@@@3#       +     +                      +   +#
# 222222#*c22222222a=:%::%#-.:1@11a=******22***=a1@111@@@%@.     *%+@*    ++++++++             +     1
# 222222c**bc22222c2=:%:::%%--:21113=*2222***+@a11111@@@%1-     .@%1%@            ++          ++     -
# 2222222c#+#b222@2=::%::::%::-%3b11#==+**++=1a1111@@@@%1#      ##2223-             ++       ++      :
# 222222222b#*11%3::::%::::%:--+:#111a1==@@13b111@@@@@%1%.      %@222b:              ++    ++       @c
# 2222222222a=3123-:::%:::%%:-113:*b111@%%@@111@@@@@%%1%.       %@222b=               +  ++       *322
# 22222222221.@@b#:::%:::%%::#@11a=+3b111111@@@@@@%%2@:.        @1222b=      .#%%#     +++       %b222
# 222222222c: *+%-::%%:::%::-%@1113::+3bbb@@@@@aaa31:-.         @1222b=.   .%1###*@*           *322222
# 222222222b-  --%%%%:::%:::-21111+=3+==+#33333*+=::-.          @122c#+11::1312221#%          @b222222
# 222222222a-.--%:::::::%::-21111b=#1c#:+=:::====+:--#**       -2222c%b11a3b22ccc21@        %a22222222
# 222222222b---:%::::::%::-%b1111a:a1c*=b@%aaa@@%3:-%::-#**..  @@22222222222cb%%%%#@      %32222222222
# 2222222221@.-:::::%%%%::-211111a:a1c=*@11111@%%2-:::::::-##--212222222222@%%@bb@%1.   %3222222222222
# 2222222222c1-.-:::::::::##@1111a:*1@:3@11111@#2@-%::::::::::=a2222222222c1cc222223: %a22222222222222
# 222222222222a@#..---:::--2@@1@@@+:aa:3@11111@%%-:%:::::::%::112222c22222222222222a+a2222222222222222
# 22222222222222@21%###**..=%%@@%%2-:+:#@11111@@1-:%::::::%:::21221b@bcc222cc@bcccc*#22222222222222222
# 2222222222222222211@%##3=-2%%%31----##@@1111@@1-:%::::::%:::21221c1@%1c22b%%###%*+b22222222222222222
# 222222222222222222222222b:-%1@:--=@:-1%@111@@@1-:%::::::%:::@1222222c@1222222ca+*b222222222222222222
# 222222222222222222222222c:-----%==@=-%%@@@@@@%@-:%::::::%::::a2222222222222222c*%2222222222222222222
# 222222222222222222222222b-:%%%@===%:--2%%@@%%3:-%:::::::%::::11222222222222222c*b2222222222222222222
# 222222222222222222222222a-=@====@%:::-#2%%%%a+---%:::::::%::-a222222222ccccccc#*c2222222222222222222
# 2222222222222222222222223-=%==@=:=:-:---1232=-:@--%::::::%%:%1@a3bcccca#*****+*b22222222222222222222
# 2222222222222222222222221-:%==%:@@3-:#%------:@=%--:%:::::%::*1==+*##*+#abb%%bc222222222222222222222
# 22222222222222222222222c=-:%=:::1@a-:#:%%:::%@===%---%%%::%:--..1ba##ac22222222222222222222222222222
# 22222222222222222222222c:::%:%::%3@-:#:::======:::%---::%%%-   .a22222222222222222222222222222222222
# 22222222222222222222222c:::%:%:::--::#::::::::::::%-@1*-:::-  .%122222222222222222222222222222222222
# 22222222222222222222222b-::%:::%%:#%:-::::::::::::%:#@%%--:-. .3222222222222222222222222222222222222
# 22222222222222222222222a-::%::::::::-#::::::::::::%:-+212%-...11222222222222222222222222222222222222
# 222222222222222222222223-::%:::::::#-#::::::::::::%::#a221a1@2c2222222222222222222222222222222222222
# 222222222222222222222222-::%:::::%#--#::::::::::::%::.1222222222222222222222222222222222222222222222
# 2222222222222222222222c+-:::%%%%------####%%%%%###----3222222222222222222222222222222222222222222222
# 22222222222222222222222@.-::------%%#---------------.#1222222222222222222222222222222222222222222222
# 22222222222222222222222a%------#%==-:=%#---------##::.3222222222222222222222222222222222222222222222
# 2222222222222222222222221b--%@=====%.#=============@=-@222222222222222222222222222222222222222222222
# 2222222222222222222222222c=-@=======%.-%============@:-b22222222222222222222222222222222222222222222
# 222222222222222222222222222-@@=======%..%@==========@=.122222222222222222222222222222222222222222222
# 22222222222222222222222222b-=@=======%---:@==========@:#12222222222222222222222222222222222222222222
# 22222222222222222222222222c::=@======%-@3-:=@========@:.22222222222222222222222222222222222222222222
# 2222222222222222222222222222-=@=====%:-%2a-:=@========@-#1222222222222222222222222222222222222222222
# 222222222222222222222222222b-=@=====%:-%223.:=@=======@:.3222222222222222222222222222222222222222222
# 22222222222222222c2222222222%:@====%%:-%2222.:@@======@=-@222222222222222222222222222222222222222222
# 22222222222222ca2+23b22222222-@@@@%%:-.%222c@.:%@@====%:-@2222222222cba333bc222222222222222222222222
# 222222222222c3:------@a22222b-------.-%a2222c%-:::%%%%%--3%122222ca2:------:2c2222222222222222222222
# 22222222222a%-:======:-@a222c: .-%%.:b2222222b#-::::--..--.1222b2=--:======:-%a222222222222222222222
# 222222222c3-:==========:-@aca-:--%%.-a22222222a%#-..#=2--:=-33@--:===========:#322222222222222222222
# 22222222c*-:@@==@@@@@====:-=::@@-1#--@2222222221@b1 1@@::@@:--:=====@@@====@@=:-32222222222222222222
# 2222222c*-+#*+==@====@@====:-%==-11.-%2222222222222.-::-%=@@====@@@@===@@==1#+@:-a222222222222222222
# 222222c2-+%#+@=@=======@@@@@===@-----1222222222222b---:%%====@@@========@==@*%*@:#b22222222222222222
# 2222223-=#%+@==@=================%::.a2222222222222@-::%:===============@===@#%*=:@c2222222222222222
# 22222a-=+3+@==@@=================%::.222222222222222-::%:================@===@#*==-22222222222222222
# 2222b#:======@@==================%::-@2222222222222a-::%::===============@@===@=@=:-b222222222222222
# 222c@-==@==@@==================::%::-%2222222222222b--::%%%%%%=============@@@==@==-@222222222222222
# 2223.::%=================@%%%%%%%%::-@2222222222222c:-::::::::%%%@==============@=::-b22222222222222
# 2223.-::%%%=@=======%%%%%::::::::::-.22222222222222c:.------::::::%%%@@@@@@@===%%:::-222222222222222
# 222c3-.-:::::%%%%%%%:::::::::-------.a22222222222222@.----.-.--:::::::::::::::::::::.222222222222222
# 22222b@.--:::::::::::::::--.#..----.#122222222222222a%---.%b3@#.--:::::::::::::::--.%b22222222222222
# 2222222a@..---:::::----..#%2@3*...#%a22222222222222221a322b222@3@#..-----------..#@2c222222222222222
# 222222222b2@#********#%13@2222b223@2222222222222222222222222222221a21@%#####%@12a1222222222222222222
# 2222222222221@%####%@1222222222222222222222222222222222222222222222222111111122222222222222222222222