import requests 
from bs4 import BeautifulSoup 
import gspread
import datetime
from time import sleep
  
gc = gspread.oauth()
sh = gc.open("stocks")

def scrap(newUrl, sector, work_sheet):
    url = newUrl
      
    #open with GET method 
    resp = requests.get(url) 
      
    #http_respone 200 means OK status 
    if resp.status_code==200: 
        
        print(sector, "Sector:") 
      
        # we need a parser,Python built-in HTML parser is enough . 
        soup = BeautifulSoup(resp.text,'html.parser')     

        l = soup.find("table",{"class":"W(100%)"}) 
        rows = l.findChildren('tr')
        total = 0
        peTotal = 0
        avgVolume = 0
        for i,row in enumerate(rows):
                cells = row.findChildren('td')
                for idx,cell in enumerate(cells):
                    value = cell.string
                    # Ticker 
                    if idx == 0:
                        # prints to the google sheets, timer is added to not hit the write limit 
                        col = "A"+str(i+1)
                        start_time = datetime.datetime.now()
                        work_sheet.update(col, value)
                        end_time = datetime.datetime.now()
                        if (end_time - start_time).total_seconds() < 1:
                            sleep(1.01)
                    # Price
                    if idx == 2:
                        col = "B"+str(i+1)
                        start_time = datetime.datetime.now()
                        work_sheet.update(col, value)
                        end_time = datetime.datetime.now()
                        if (end_time - start_time).total_seconds() < 1:
                            sleep(1.01)
                    # Percent change daily
                    if idx == 4:
                        col = "C"+str(i+1)
                        start_time = datetime.datetime.now()
                        work_sheet.update(col, value)
                        end_time = datetime.datetime.now()
                        if (end_time - start_time).total_seconds() < 1:
                            sleep(1.01)
                        s = value.split('%')[0]
                        if "+" in s:
                            s1 = s.split('+')[1]
                            total += float(s1)
                        elif "-" in s:
                            s1 = s.split('-')[1]
                            total -= float(s1)
                    # avg volume
                    if idx == 6:
                        col = "D"+str(i+1)
                        s = str(cell)
                        s1 = s.split('-->')[1]
                        s2 = s1.split('<!--')[0]

                        start_time = datetime.datetime.now()
                        work_sheet.update(col, s2)
                        end_time = datetime.datetime.now()
                        if (end_time - start_time).total_seconds() < 1:
                            sleep(1.01)

                        s3 = s2.replace(",","")
                        if "M" in s3:
                            s4 = s3.split('M')[0]
                            avgVolume += float(s4)*1000000
                        else:
                            avgVolume += float(s3)
                    # PE ratio
                    if idx == 8:
                        col = "E"+str(i+1)
                        
                        if value != 'N/A':
                            s = str(cell)
                            s1 = s.split('-->')[1]
                            s2 = s1.split('<!--')[0]

                            start_time = datetime.datetime.now()
                            work_sheet.update(col, s2)
                            end_time = datetime.datetime.now()
                            if (end_time - start_time).total_seconds() < 1:
                                sleep(1.01)

                            s3 = s2.replace(",","")
                            peTotal += float(s3)
                            # print(s3, end =" ")
                        else:
                            start_time = datetime.datetime.now()
                            work_sheet.update(col, value)
                            end_time = datetime.datetime.now()
                            if (end_time - start_time).total_seconds() < 1:
                                sleep(1.01)
                        
                #print()      
        print("Average % Change: "+"{:.4f}".format(total/i))
        print("Average PE Ratio: "+"{:.4f}".format(peTotal/i))
        print("Average Volume (3 mo): "+"{:,.2f}".format(avgVolume/i))
        print()
    else: 
        print("Error") 

def tech():
    url = 'https://finance.yahoo.com/sector/ms_technology' 
    sector = 'Technology'
    work_sheet = sh.worksheet("Technology")
    scrap(url, sector, work_sheet)

def financial():
    url='https://finance.yahoo.com/sector/ms_financial_services'
    sector = 'Financial'
    work_sheet = sh.worksheet("Financial")
    scrap(url, sector, work_sheet)

def basicMaterial():
    url='https://finance.yahoo.com/sector/ms_basic_materials'
    sector = 'Basic Material'
    work_sheet = sh.worksheet("Basic Material")
    scrap(url, sector, work_sheet)

def CommunicationService():
    url='https://finance.yahoo.com/sector/ms_communication_services'
    sector = 'Communication Service'
    work_sheet = sh.worksheet("Communication Service")
    scrap(url, sector, work_sheet)

def ConsumerCyclical():
    url='https://finance.yahoo.com/sector/ms_consumer_cyclical'
    sector = 'Consumer Cyclical'
    work_sheet = sh.worksheet("Consumer Cyclical")
    scrap(url, sector, work_sheet)

def ConsumerDefensive():
    url='https://finance.yahoo.com/sector/ms_consumer_defensive'
    sector = 'Consumer Defensive'
    work_sheet = sh.worksheet("Consumer Defensive")
    scrap(url, sector, work_sheet)

def HealthCare():
    url='https://finance.yahoo.com/sector/ms_healthcare'
    sector = 'Health Care'
    work_sheet = sh.worksheet("Health Care")
    scrap(url, sector, work_sheet)

def Industrial():
    url='https://finance.yahoo.com/sector/ms_industrials'
    sector = 'Industrial'
    work_sheet = sh.worksheet("Industrial")
    scrap(url, sector, work_sheet)

def RealEstate():
    url='https://finance.yahoo.com/sector/ms_real_estate'
    sector = 'Real Estate'
    work_sheet = sh.worksheet("Real Estate")
    scrap(url, sector, work_sheet)

def Utilities():
    url='https://finance.yahoo.com/sector/ms_utilities'
    sector = 'Utilities'
    work_sheet = sh.worksheet("Utilities")
    scrap(url, sector, work_sheet)

def Energy():
    url='https://finance.yahoo.com/sector/ms_energy'
    sector = 'Energy'
    work_sheet = sh.worksheet("Energy")
    scrap(url, sector, work_sheet)

#tech()
#financial()
basicMaterial()
CommunicationService()
ConsumerCyclical()
ConsumerDefensive()
HealthCare()
Industrial()
RealEstate()
Utilities()
Energy()