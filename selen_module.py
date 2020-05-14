
import json
import time
import requests
from pymouse import PyMouse
from selenium import webdriver
import selenium.webdriver.chrome.options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# driver boot procedure
def boot():
    # manage notifications
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs",prefs)

    # driver itself
    dv = webdriver.Chrome(chrome_options = chrome_options, executable_path = r"./chromedriver81.exe")
    dv.maximize_window()
    return dv

# kill the driver
def killb(dv):
    dv.quit()
    
# open startup page
def startup_link(dv):
    dv.get("http://sccourts.org/")
    #dv.get("https://www2.greenvillecounty.org/SCJD/PublicIndex/")
   
# start the worker 
def worker(dv):
    WebDriverWait(dv, 20).until(EC.visibility_of_all_elements_located)
    
    mouse = PyMouse()
    ind = 1
    while True:
        ind += 1
        try:
            temp = dv.find_element_by_xpath("/html/body/form/div[3]/div/div[2]/div[5]/div/table/tbody/tr["+str(ind)+"]/td[3]/a")
            mouse.click(10, 10, 2)
            time.sleep(0.1)
            mouse.click(20, 110, 1)
            
        except:
            break
    
    dv.close()
    
    ind = 1
    while True:
        ind += 1
        try:
            dv.switch_to.window(dv.window_handles[0])
            time.sleep(0.5)
            row = dv.find_element_by_xpath("/html/body/form/div[3]/div/div[2]/div[5]/div/table/tbody/tr["+str(ind)+"]/td[3]/a")
            #try:
            row.click()
            get_addresses(dv)
            dv.close()
            time.sleep(0.5)
        except:
            break

# get address on case page 
def get_addresses(dv):
    WebDriverWait(dv, 20).until(EC.visibility_of_all_elements_located)
    time.sleep(3)
    
    case_number = dv.find_element_by_xpath("/html/body/form/div[3]/div/div[2]/div[3]/table/tbody/tr[3]/td[2]").text
    case_type = dv.find_element_by_xpath("/html/body/form/div[3]/div/div[2]/div[3]/table/tbody/tr[4]/td[4]").text
    case_status = dv.find_element_by_xpath("/html/body/form/div[3]/div/div[2]/div[3]/table/tbody/tr[5]/td[2]").text
    disposition_date = dv.find_element_by_xpath("/html/body/form/div[3]/div/div[2]/div[3]/table/tbody/tr[3]/td[6]").text
    county = dv.find_element_by_id("LabelHeadingCounty").text
    court_agency = dv.find_element_by_xpath("/html/body/form/div[3]/div/div[2]/div[3]/table/tbody/tr[3]/td[4]").text
    
    i = 1
    defendants = []
    plaintiffs = []
    while True:
        i += 1
        try:
            defendant = []
            plaintiff = []
            name = dv.find_element_by_xpath("/html/body/form/div[3]/div/div[2]/div[5]/div/div/div[2]/div[1]/span/table/tbody/tr["+str(i)+"]/td[1]").text
            full_address = dv.find_element_by_xpath("/html/body/form/div[3]/div/div[2]/div[5]/div/div/div[2]/div[1]/span/table/tbody/tr["+str(i)+"]/td[2]").text
            party_type = dv.find_element_by_xpath("/html/body/form/div[3]/div/div[2]/div[5]/div/div/div[2]/div[1]/span/table/tbody/tr["+str(i)+"]/td[6]").text
            
            split_address = full_address.split(' ')
            zip_code = split_address[-1]
            state = split_address[-2]
            city = split_address[-3]
            
            if "d" in str(party_type.lower()):
                defendant.append(name)
                defendant.append(full_address)
                defendant.append(state)
                defendant.append(city)
                defendant.append(zip_code)
                defendant.append(party_type)
                defendants.append(defendant)
            else:
                plaintiff.append(name)
                plaintiff.append(full_address)
                plaintiff.append(state)
                plaintiff.append(city)
                plaintiff.append(zip_code)
                plaintiff.append(party_type)
                plaintiffs.append(plaintiff)
                
        except:
            data = {}
            data['CaseNumber'] = case_number
            data['CaseType'] = case_type
            data['CaseStatus'] = case_status
            data['DispositionDate'] = disposition_date
            data['County'] = county
            data['CourtAgency'] = court_agency
            
            data['Parties'] = {}
            for i in range(len(defendants)):
                def_name = "Defendant" + str(i+1)
                data['Parties'][def_name] = {}
                data['Parties'][def_name]['Name'] = defendants[i][0]
                data['Parties'][def_name]['FullAddress'] = defendants[i][1]
                data['Parties'][def_name]['State'] = defendants[i][2]
                data['Parties'][def_name]['City'] = defendants[i][3]
                data['Parties'][def_name]['ZipCode'] = defendants[i][4]
            
            for i in range(len(plaintiffs)):
                plf_name = "Plaintiff" + str(i+1)
                data['Parties'][plf_name] = {}
                data['Parties'][plf_name]['Name'] = plaintiffs[i][0]
                data['Parties'][plf_name]['FullAddress'] = plaintiffs[i][1]
                data['Parties'][plf_name]['State'] = plaintiffs[i][2]
                data['Parties'][plf_name]['City'] = plaintiffs[i][3]
                data['Parties'][plf_name]['ZipCode'] = plaintiffs[i][4]
            
            filename = case_number + ".json"
            with open(filename, 'w') as outfile:
                json.dump(data, outfile)
                
            break
    
    url = 'http://admin.rentaware.net/system/evictions/index.cfm'
    payload = data
    headers = {'content-type': 'application/json'}

    response = requests.post(url, data=json.dumps(payload), headers=headers)
    print(response.status_code)