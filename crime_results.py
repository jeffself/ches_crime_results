import sys, os
import urllib, urllib2
from bs4 import BeautifulSoup
import csv

def scraper(data):
    """We are getting the crime results data from the
       Crimemappers site using BeautifulSoup."""

    url = get_url()
    try:
        html = urllib.urlopen(url).read()
        soup = BeautifulSoup(html)

        t = soup.findAll('table')[0]
        rows = t.findAll('tr')[2:]
        for row in rows:
            crime_type = row.findAll('td')[0].contents[0]
            description = row.findAll('td')[1].findAll('span')[0].contents[0]
            case_number = row.findAll('td')[2].findAll('span')[0].contents[0]
            location = row.findAll('td')[3].findAll('span')[0].contents[0]
            agency = row.findAll('td')[4].findAll('span')[0].contents[0]
            date_reported = row.findAll('td')[5].findAll('span')[0].contents[0]
            record = {"crime_type": crime_type, "description": description, "case_number": case_number, "location": location,
                      "agency": agency, "date_reported": date_reported}
            data.append(record)
    except:
        print "Invalid URL"

def export_to_csv(data, ofile):
    f = open(ofile, 'wt')
    try:
        fieldnames = ('crime_type', 'description', 'case_number', 'location', 'agency', 'date_reported')
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='|')
        headers = {}
        for r in data:
            writer.writerow({'crime_type':r['crime_type'], 'description':r['description'], 'case_number':r['case_number'], \
                             'location':r['location'], 'agency':r['agency'], 'date_reported':r['date_reported']})
    finally:
        f.close()

def get_url():
    return 'http://www.crimemapping.com/DetailedReport.aspx?db=1/01/2012+00:00:00&de=3/09/2012+23:59:00&ccs=AR,AS,BU,DP,DR,DU,FR,HO,VT,RO,SX,TH,VA,VB,WE&xmin=-8498704.744278405&ymin=4397645.076574663&xmax=-8477053.956016656&ymax=4404581.736891533'

def main():
    ofile = sys.argv[1]
    data = []
    scraper(data)
    export_to_csv(data, ofile)

    if len(data) > 0:
        print "There are %d crimes listed." % len(data)

if __name__ == '__main__':
    main()
