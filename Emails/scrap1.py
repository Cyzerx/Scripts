# -*- coding: utf-8 -*-
"""
Python script to bulk scrape websites for email addresses
"""

import urllib.request, urllib.error
import re
import csv
import pandas as pd
import os
import ssl

# 1: Get input file path from user '.../Documents/upw/websites.csv'
user_input = input("Enter the path of your file: ")

# If input file doesn't exist
if not os.path.exists(user_input):

    print("File not found, verify the location - ", str(user_input))

try:
    # 2. read file
    df = pd.read_csv(user_input)

    # 3. create the output csv file
    with open('EmailID.csv', mode='w', newline='') as file:
        csv_writer = csv.writer(file, delimiter=',')
        csv_writer.writerow(['Website', 'Email'])

    # 4. Get websites
    for site in list(df['Website']):
        #print(site)
        gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        req = urllib.request.Request("http://"+site, headers={'User-Agent': "Magic Browser",
                                                                  #'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                                                                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                                                                   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                                                                   'Accept-Encoding': 'none',
                                                                   'Accept-Language': 'en-US,en;q=0.8',
                                                                   'Connection': 'keep-alive'
                                                                  })

            # 5. Scrape email id
        with urllib.request.urlopen(req, context=gcontext) as url:
            s = url.read().decode('utf-8', 'ignore')
            email = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}", s)
            print(email)

                # 6. Write the output
            with open('Emails.csv', mode='a', newline='') as file:
                csv_writer = csv.writer(file, delimiter=',')
                [csv_writer.writerow([site, item]) for item in email]

# If error occur
except urllib.error.URLError as e:
    print("Failed to open URL {0} Reason: {1}".format(site, e.reason))
