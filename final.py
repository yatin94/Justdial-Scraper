from number import Functions
from selenium import webdriver
from bs4 import BeautifulSoup 
import requests
import time
import lxml
import csv
import traceback

#csv open
f = open('Data\\Output.csv','w',encoding='UTF-8')
print('Excel File Created\n')

#Text open
txt = open('Data\\Input.txt','r')
print('Text File Reading.....\n')
urltxt = txt.read()
urltxt = urltxt.replace("\n","")
print('URL File Read...........\n')
txt.close()
#Header in csv-------------------------------->
header = 'Name,Address,Website,Contact,JDVerified'
f.write(header)
print('Header printed\n')

#initializing variables-------------------------------->
print('Initializing variables and changing useragent\n')
sr_no=1
page_no = 1


#changing useragent---------------------------------->
profile = webdriver.FirefoxProfile()
profile.set_preference("general.useragent.override","Morzilla:4.0")

#initializing Selenium webdriver----------------------->
print('Initializing Selenium driver\n')
driver = webdriver.Firefox()
driver.minimize_window()

#main code---------------------->
print('Running Main Code \n')

#total page is 50 for every search----------------->
try:
    while (page_no < 51):
        url = urltxt+str(page_no)
        driver.get(url)
        try:
            try:  
                  driver.find_element_by_xpath("/html/body/section[15]/section/span[@class='jcl']").click()
            except:
                  pass
            links = driver.find_element_by_xpath("//span[@class='jcn']")
            links.click()
        except:
          break  
        while True:
           #html content from selenium to beautiful soup-------------------->
            content = driver.page_source.encode('utf-8').strip()
            soup = BeautifulSoup(content,"html.parser")
            #finding  name, address, verification  --------------------->
            name = soup.find("span",{"class":"fn"})
            address = (soup.find("span",{"class":"adrstxtr"})).text[:-6].strip()
            address = '"'+address+'"'
            verification = soup.findAll("span",{"class","wrtrvtxt"})[-1]
            #verification execution ---------------------------->
            if(verification.text=='Jd Verified'):
              verification = 'Verified'
            elif(verification.text=='Manage Campaign'):
              verification = 'Not Verified'
            else:
              verification = 'Error'
             #calling phone function -------------------------->
            phone_num = Functions(soup)
              #find website link of the data--------------------------->
            try:  
              website = ((soup.findAll("span",{"class":"mreinfp comp-text"})[-1]).find("a"))
              if(website.get('title')==None):
                website= 'None'
              else:
                website=website.get('title')
            except:
              website="None"
            #print data in excel--------------------->
            f.write('\n'+name.text+","+address+","+website+","+phone_num+","+verification)
            print("line No " + str(sr_no) +" Printed of page "+str(page_no))
            sr_no = sr_no+1
            time.sleep(12)
            try:
              #for Next Button---------------------------------->
              try:  
                  driver.find_element_by_xpath("/html/body/section[15]/section/span[@class='jcl']").click()
              except:
                  pass
              driver.find_element_by_xpath("//a[@class='dtlpg_sprt cntl_right']").click()
            except:  
              page_no = page_no+1
              break
    print("All Data have been printed Successfully without any error")
    f.close()
    driver.quit()
    print('All drivers closed successfully. Press Enter to exit')
    input()
except Exception as e:
    print('Error detected : '+str(e)+'\n')
    print('eror pon line'+traceback.format_exc())
    driver.quit()
    f.close()
    print("All drivers closed. Please press enter to exit")
    input()
