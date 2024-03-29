
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
    #prefs = {"profile.default_content_setting_values.notifications" : 2}
    #chrome_options.add_experimental_option("prefs",prefs)
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-blink-features")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    #chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    #chrome_options.add_experimental_option('useAutomationExtension', False)
    
    #chrome_options.add_argument("user-agent=[Mozilla/5.0 (Linux; Android 10; SM-A205U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Mobile Safari/537.36]")

    # driver itself
    dv = webdriver.Chrome(chrome_options = chrome_options, executable_path = r"./chromedriver81.exe")
    dv.maximize_window()
    script = '''
    Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
    })
    '''
    dv.execute_script(script)
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
            try:
                with open("processed_cases.txt", "r", newline='')as pc:
                    processed_cases = pc.read().splitlines()
            except:
                with open("processed_cases.txt", "w", newline='')as pc:
                    pc.close()
                    processed_cases = []

            case_number = dv.find_element_by_xpath("/html/body/form/div[3]/div/div[2]/div[5]/div/table/tbody/tr["+str(ind)+"]/td[3]/a").text
            
            if case_number in processed_cases:
                continue
            else:
                processed_cases.append(case_number)
                with open("processed_cases.txt", "w", newline='')as pc:
                    for case in processed_cases:
                        pc.write(case + "\n")
                        
            temp = dv.find_element_by_xpath("/html/body/form/div[3]/div/div[2]/div[5]/div/table/tbody/tr["+str(ind)+"]/td[3]/a")
            mouse.click(10, 10, 2)
            time.sleep(0.1)
            mouse.click(20, 110, 1)
            time.sleep(0.2)

            script = '''
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
            '''
            dv.execute_script(script)
    
            dv.switch_to.window(dv.window_handles[0])
            time.sleep(0.3)
            row = dv.find_element_by_xpath("/html/body/form/div[3]/div/div[2]/div[5]/div/table/tbody/tr["+str(ind)+"]/td[3]/a")
            row.click()
            #location = row.location
            #mouse.click(location['x'] + 5, location['y'] + 75, 1)
            get_addresses(dv)
            dv.close()
            time.sleep(0.3)
            dv.switch_to.window(dv.window_handles[0])
            time.sleep(0.3)
            
        except Exception as e:
            #print(e)
            print("Something went wrong, or all cases have been processed.\nType STOP if you would like to stop the execution.\nType RESTART to try again, but make sure you are on the cases page.\nPress ENTER to process in manual mode, but make sure to open a case page.")
            p = input()
            if p.lower() == "stop":
                break
            elif p.lower() == "restart":
                ind = 1
                dv.switch_to.window(dv.window_handles[0])
                time.sleep(5)
                continue
            else:
                dv.switch_to.window(dv.window_handles[0])
                get_addresses(dv)                
        
    dv.close()

# get address on case page 
def get_addresses(dv):
    while True:
        WebDriverWait(dv, 20).until(EC.visibility_of_all_elements_located)
        time.sleep(3)

        case_number = dv.find_element_by_xpath("/html/body/form/div[3]/div/div[2]/div[3]/table/tbody/tr[3]/td[2]").text  
        case_type = dv.find_element_by_xpath("/html/body/form/div[3]/div/div[2]/div[3]/table/tbody/tr[4]/td[4]").text
        case_status = dv.find_element_by_xpath("/html/body/form/div[3]/div/div[2]/div[3]/table/tbody/tr[5]/td[2]").text
        disposition_date = dv.find_element_by_xpath("/html/body/form/div[3]/div/div[2]/div[3]/table/tbody/tr[6]/td[4]").text
        filed_date = dv.find_element_by_xpath("/html/body/form/div[3]/div/div[2]/div[3]/table/tbody/tr[3]/td[6]").text
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
                

                if full_address == '':
                    full_address = '+'
                    zip_code = '+'
                    state = '+'
                    city = '+'
                else:
                    split_address = full_address.split(' ')
                    zip_code = split_address[-1]
                    try:
                        if len(zip_code) > 5:
                                zip_code = zip_code[ 0 : 5 ]
                        if len(zip_code) != 5:
                            try: 
                                zip_code = int(zip_code)
                            except:
                                zip_code = '+'
                        else:
                            zip_code = split_address[-1]
                        print(zip_code)
                    except Exception as e:
                        #print(e)
                        None
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
                data['FiledDate'] = filed_date
                data['County'] = county
                data['CourtAgency'] = court_agency
                
                data['Defendants'] = []
                for i in range(len(defendants)):
                    def_name = {}
                    def_name['Name'] = defendants[i][0]
                    def_name['FullAddress'] = defendants[i][1]
                    def_name['State'] = defendants[i][2]
                    def_name['City'] = defendants[i][3]
                    def_name['ZipCode'] = defendants[i][4]
                    data['Defendants'].append(def_name)

                data['Plaintiffs'] = []
                for i in range(len(plaintiffs)):
                    plf_name = {}
                    plf_name['Name'] = plaintiffs[i][0]
                    plf_name['FullAddress'] = plaintiffs[i][1]
                    plf_name['State'] = plaintiffs[i][2]
                    plf_name['City'] = plaintiffs[i][3]
                    plf_name['ZipCode'] = plaintiffs[i][4]
                    data['Plaintiffs'].append(plf_name)
                
                filename = case_number + ".json"
                with open(filename, 'w') as outfile:
                    json.dump(data, outfile)
                break
        
        url = 'http://admin.rentaware.net/system/evictions/index.cfm'
        payload = data
        headers = {'content-type': 'application/json'}

        response = requests.post(url, data=json.dumps(payload), headers=headers)
        print(response.status_code)
        
        print("Case", case_number, "processed successfully")
        
        break