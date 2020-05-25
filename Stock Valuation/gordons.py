from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

#get stock
symbol = input("Enter stock symbol: ")

#chrome setup
my_path ="C:\\Users\\joshu\\Documents\\Uni Work\\YCS\\chromedriver.exe" #where chromedriver.exe is
browser = webdriver.Chrome(executable_path=my_path)

#url setup
url_form = "https://www.nasdaq.com/market-activity/stocks/{}/dividend-history"
url = url_form.format(symbol)
browser.get(url)

#get compnay name
company_xpath = "//h1[contains(text(), {})]".format(symbol.upper())
company = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, company_xpath))).text
print(company)

#get price
price_xpath = "//html/body/div[2]/div/main/div/div[3]/section/div[2]/div/div/div[1]/div[1]/div/div[1]/div[2]/span/span[2]"
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

#get current div value
currentdiv = get_elements("//html/body/div[2]/div/main/div/div[4]/div[1]/div/div[2]/ul/li[3]/span[2]/span")
currentdiv = float(currentdiv[0].replace("$",""))

#wacc
waccurl = "https://www.gurufocus.com/term/wacc/{}/WACC/"
url = waccurl.format(symbol)
browser.get(url)
wacc = get_elements("//html/body/div[2]/div[2]/div/div/div/div[2]/font[1]")
wacc = wacc[0].replace(":","")
wacc = (float(wacc.replace("% As of Today","")))/100

#get div growth rate
divgrowthurl = "https://www.gurufocus.com/term/dividend_growth_3y/{}/3-Year-Dividend-Growth-Rate/"
url = divgrowthurl.format(symbol)
browser.get(url)
divgrowth = get_elements("//html/body/div[2]/div[2]/div/div/div/div[2]/font[1]")
m = re.search(': (.+?)%', divgrowth[0])
if m:
    found = m.group(1)
divgrowth = found
divgrowth = float(divgrowth)/100

#calculation
intrinsicprice=((currentdiv*(1+divgrowth))/(wacc - divgrowth))


#print results
intrinsicprice="{:.2f}".format(intrinsicprice)
print("Gordons Intrinsic Value: $" + str(intrinsicprice))

#over or under
if (price>float(intrinsicprice)):
    print ("(Over valued)")
else:
    print ("(Under valued)")
print("If negative then div growth>wacc")

browser.quit()
