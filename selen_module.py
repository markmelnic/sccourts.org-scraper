
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import selenium.webdriver.common.action_chains as AC
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.chrome.options
import random
import time


# driver boot procedure
def boot():
    # manage notifications
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs",prefs)

    # driver itself
    dv = webdriver.Chrome(chrome_options = chrome_options, executable_path = r"./chromedriver81.exe")
    return dv

# kill the driver
def killb(dv):
    dv.quit()
    
# open startup page
def startup_link(dv):
    dv.get("http://sccourts.org/")
   
# start the worker 
def worker(dv):
    WebDriverWait(dv, 20).until(EC.visibility_of_all_elements_located)
    
    ind = 1
    while True:
        ind += 1
        try:
            row = dv.find_element_by_xpath("/html/body/form/div[3]/div/div[2]/div[5]/div/table/tbody/tr["+str(ind)+"]/td[3]/a")
            #try:
            row.click()
            get_addresses(dv)
            '''
            except Exception as e:
                print(e)
                dv.back()
                dv.back()
                WebDriverWait(dv, 20).until(EC.visibility_of_all_elements_located)
                time.sleep(3)
                try:
                    row.click()
                    get_addresses(dv)
                except:
                    dv.back()
                    #dv.back()
                    WebDriverWait(dv, 20).until(EC.visibility_of_all_elements_located)
                    time.sleep(3)
                    row.click()
                    get_addresses(dv)
            '''
                    
        except:
            break
       
# get address on case page 
def get_addresses(dv):
    WebDriverWait(dv, 20).until(EC.visibility_of_all_elements_located)
    time.sleep(3)
    
    i = 1
    addresses = []
    while True:
        i += 1
        try:
            address = dv.find_element_by_xpath("/html/body/form/div[3]/div/div[2]/div[5]/div/div/div[2]/div[1]/span/table/tbody/tr["+str(i)+"]/td[2]")
            addresses.append(address.text)
        except:
            break
        
    print(addresses)
    '''
    back = AC.ActionChains(dv)
    back.key_down(Keys.LEFT_ALT).send_keys(Keys.ARROW_LEFT).key_up(Keys.LEFT_ALT).perform()
    AC.ActionChains(dv).send_keys(Keys.LEFT_ALT, Keys.ARROW_LEFT).perform()
    m = dv.find_element_by_xpath("/html")
    m.send_keys(Keys.LEFT_ALT, Keys.ARROW_LEFT)
    '''
    dv.refresh()
    time.sleep(5)
    
    dv.back()
    dv.back()
    
    WebDriverWait(dv, 20).until(EC.visibility_of_all_elements_located)
    time.sleep(3)
