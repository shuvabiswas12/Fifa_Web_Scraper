
import sys, os
from fifa_script.extract import Extract
from fifa_script.fifa import Crawl, GetData

if not os.path.exists("F:\\Python Projects\\Fifa Web Scraper\\html_page\\fifa.txt"):
    crawlObject = Crawl()
    crawlObject.getHtmlPage_request()
else:
    print("True")

while True:

    print("\nDo you want to generate a report right now ? (Y/N) \n")
    generate = input('Answer: ')
    if generate.upper() == 'Y':
        report = Extract()
        report.createWorkSheet()
        print("Report is Generated named 'Report.xlsx' \n")
        break
    else:
        print('\n\n')
        getDataObject = GetData()
        getDataObject.getData()

        print("\nDo you want to terminate the program now ? (Y/N)\n")
        terminate = input("Answer: ")
        
        # terminating the running program/script
        if terminate.upper() == 'Y':
            sys.exit()
        else:
            continue
    
