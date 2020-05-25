from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

#get stock
symbol = input("Enter stock symbol: ")

#chrome setup
my_path ="C:\\Users\\joshu\\Documents\\Uni Work\\YCS\\chromedriver.exe"  #where chromedriver.exe is located
browser = webdriver.Chrome(executable_path=my_path)

#url setup
url_form = "https://www.nasdaq.com/market-activity/stocks/{}/earnings"
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

#get elements and add to a list
def get_elements(xpath):
    elements = browser.find_elements_by_xpath(xpath) # find the elements
    text = []
    for e in elements:
        text.append(e.text)
    return text

#get earnings per share
earningspershare = get_elements("//html/body/div[2]/div/main/div/div[5]/div[2]/div/div[1]/div/div[4]/div[1]/div/div/table/tbody/tr[1]/td[1]")
earningspershare=float(earningspershare[0])

#get price per earnings
pe_button_xpath = "//html/body/div[2]/div/main/div/div[4]/div/section/div/div[3]/ul/li[6]/a/span"
pe_button = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, pe_button_xpath))).click()
time.sleep(10)
pe = get_elements("//main/div/div[5]/div[2]/div/div[1]/div/div[1]/div[2]/div[2]/div[2]/table/tbody/tr[2]/td")
pe=float(pe[0])

#get peg ratio
pegratio = get_elements("//main/div/div[5]/div[2]/div/div[1]/div/div[1]/div[4]/div[2]/div[2]/table/tbody/tr/td")
pegratio=float(pegratio[0])

#get pe industry average
peindurl = "https://www.gurufocus.com/term/pettm/{}/PE-Ratiottm"
url = peindurl.format(symbol)
browser.get(url)
peind = get_elements("//html/body/div[2]/div[2]/div/div/div/div/div/div/div/div")
peind = peind[1]
m = re.search('Industry Median: (.+?) vs', peind)
if m:
    found = m.group(1)
peind = found
peind = float(peind)

#print results
value = earningspershare*pe
value = "{:.2f}".format(value)
print("Forecast intrinsic Value: $" + str(value))
#over or under
if (price>float(value)):
    print("(Over valued)")
if (price<float(value)):
    print("(Under valued)")
if (price==float(value)):
    print("(Hold)")

#peg ratio comparison
print("PEG Ratio = " + str(pegratio))
if (pegratio<1):
    print("(Under Valued)")
if (pegratio>1):
    print("(Over Valued)")
if (pegratio==0.0):
    print("(Hold)")

#pe comparison
print("PE Ratio: "+str(pe))
print("Industry Average PE Ratio: " + str(peind))
if (pe>peind):
    print("(Over Valued)")
if (pe<peind):
    print("(Under Vauled)")
if (pe==peind):
    print("(Hold)")

browser.quit()
