from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

#chrome setup
my_path ="C:\\Users\\joshu\\Documents\\Uni Work\\YCS\\chromedriver.exe"  #where chromedriver.exe is located
browser = webdriver.Chrome(executable_path=my_path)

#url setup
url_form = "https://www.nasdaq.com/market-activity/stocks/{}/earnings"
symbol = input("Enter stock symbol: ")
url = url_form.format(symbol)
browser.get(url)

#accept cookies
accept_button_xpath = "//div/button[contains(text(), 'Accept')]"
accept_button = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, accept_button_xpath))).click()

#get compnay name
company_xpath = "//h1[contains(text(), {})]".format(symbol.upper())
company = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, company_xpath))).text
print(company)

#get price
price_xpath = "//html/body/div[2]/div/main/div/div[4]/section/div[2]/div/div/div[1]/div[1]/div/div[1]/div[2]/span/span[2]"
price = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, price_xpath))).text
print("Price: " + str(price))
price = float(price.replace("$",""))

#get elemts and add to a list
def get_elements(xpath):
    elements = browser.find_elements_by_xpath(xpath) # find the elements
    text = []
    for e in elements:
        text.append(e.text)
    return text

#get earnings per share
earningspershare = get_elements("//html/body/div[2]/div/main/div/div[5]/div[2]/div/div[1]/div/div[4]/div[1]/div/div/table/tbody/tr[1]/td[1]")
earningspershare=float(earningspershare[0])

#get price per eaenings
pe_button_xpath = "//html/body/div[2]/div/main/div/div[4]/div/section/div/div[3]/ul/li[6]/a/span"
pe_button = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, pe_button_xpath))).click()
time.sleep(10)
pe = get_elements("//main/div/div[5]/div[2]/div/div[1]/div/div[1]/div[2]/div[2]/div[2]/table/tbody/tr[1]/td")
pe=float(pe[0])

#print results
value = earningspershare*pe
value = "{:.2f}".format(value)
print("Intrinsic Value: $" + str(value))
#over or under
if (price>float(value)):
    print ("(Over valued)")
else:
    print ("(Under valued)")

browser.quit()
