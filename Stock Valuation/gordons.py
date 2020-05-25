from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

#chrome setup
my_path ="C:\\Users\\joshu\\Documents\\Uni Work\\YCS\\chromedriver.exe" #where chromedriver.exe is
browser = webdriver.Chrome(executable_path=my_path)

#url setup
url_form = "https://www.nasdaq.com/market-activity/stocks/{}/dividend-history"
symbol = input("Enter stock symbol: ")
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

#get div growth rate
div1 = get_elements("//html/body/div[2]/div/main/div/div[4]/div[1]/div/div[2]/div[2]/div[2]/table/tbody/tr[3]/td[2]")
div1 = float(div1[0].replace("$",""))
div2 = get_elements("//html/body/div[2]/div/main/div/div[4]/div[1]/div/div[2]/div[2]/div[2]/table/tbody/tr[4]/td[2]")
div2 = float(div2[0].replace("$",""))
div3 = get_elements("//html/body/div[2]/div/main/div/div[4]/div[1]/div/div[2]/div[2]/div[2]/table/tbody/tr[5]/td[2]")
div3 = float(div3[0].replace("$",""))
div4 = get_elements("//html/body/div[2]/div/main/div/div[4]/div[1]/div/div[2]/div[2]/div[2]/table/tbody/tr[6]/td[2]")
div4 = float(div4[0].replace("$",""))

sumdiv = div1 + div2 + div3 + div4
divgrowth = (currentdiv/sumdiv) -1

#wacc
waccul = "https://www.gurufocus.com/term/wacc/{}/WACC/"
url = waccul.format(symbol)
browser.get(url)
wacc = get_elements("//html/body/div[2]/div[2]/div/div/div/div[2]/font[1]")
wacc = wacc[0].replace(":","")
wacc = (float(wacc.replace("% As of Today","")))/100

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

browser.quit()
