#!/usr/bin/env python
"""Scraper for City of Chesapeake's CrimeMapping app"""

import sys
import requests
from bs4 import BeautifulSoup
import csv
from datetime import date, timedelta


def scraper(data):
    """We are getting the crime results data from the
       Crimemappers site using BeautifulSoup."""

    url = get_url()
    try:
        html = requests.get(url)
        soup = BeautifulSoup(html.text, "html.parser")

        t = soup.findAll('table')[0]
        rows = t.findAll('tr')[2:]
        for row in rows:
            crime_type = row.findAll('td')[0].contents[0]
            description = row.findAll('td')[1].findAll('span')[0].contents[0]
            case_number = row.findAll('td')[2].findAll('span')[0].contents[0]
            location = row.findAll('td')[3].findAll('span')[0].contents[0]
            agency = row.findAll('td')[4].findAll('span')[0].contents[0]
            date_reported = row.findAll('td')[5].findAll('span')[0].contents[0]
            record = {"crime_type": crime_type, "description": description,
                      "case_number": case_number, "location": location,
                      "agency": agency, "date_reported": date_reported}
            data.append(record)
    except:
        print("Invalid URL")


def export_to_csv(data, csvfile):
    f = open("data/" + csvfile, 'wt')
    try:
        fieldnames = ('crime_type', 'description', 'case_number', 'location',
                      'agency', 'date_reported')
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='|')
        for r in data:
            writer.writerow({'crime_type': r['crime_type'],
                             'description': r['description'],
                             'case_number': r['case_number'],
                             'location': r['location'],
                             'agency': r['agency'],
                             'date_reported': r['date_reported']})
    finally:
        f.close()


def get_url():
    root_url = 'http://www.crimemapping.com/DetailedReport.aspx'
    today = date.today()
    start_date = today - timedelta(180)
    start_date_string = str(start_date.month) + '/' + str(start_date.day) + \
        '/' + str(start_date.year) + '+00:00:00'
    current_date_string = str(today.month) + '/' + str(today.day) + '/' + \
        str(today.year) + '+23:59:00'
    ccs = 'AR,AS,BU,DP,DR,DU,FR,HO,VT,RO,SX,TH,VA,VB,WE'
    xmin = '-8514173.687877595'
    ymin = '4386877.010215002'
    xmax = '-8461585.012417465'
    ymax = '4420356.428603864'
    faid = '0b80bce5-5d21-468b-ae81-3d6e2ecf532e'
    url = str(root_url + '?db=' + start_date_string +
              '&de=' + current_date_string + '&ccs=' + ccs + '&xmin=' +
              xmin + '&ymin=' + ymin + '&xmax=' + xmax + '&ymax=' + ymax +
              '&faid=' + faid)
    return url


def main():
    csvfile = sys.argv[1]
    data = []
    scraper(data)
    export_to_csv(data, csvfile)

    if len(data) > 0:
        print("There are %d crimes listed." % len(data))

if __name__ == '__main__':
    main()
