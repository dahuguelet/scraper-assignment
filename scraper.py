# Sources:
# http://www.pythonforbeginners.com/cheatsheet/python-mechanize-cheat-sheet
# http://wwwsearch.sourceforge.net/mechanize/faq.html

import urllib2, csv
import mechanize
from bs4 import BeautifulSoup

output = open('data.csv', 'w')
writer = csv.writer(output)
# Open the Secretary of State's election results archives
br = mechanize.Browser()
br.open('http://enrarchives.sos.mo.gov/enrnet/')

# Here's the stuff I did to find the silly forms and controls. 
# Thanks Jason Kander. 

# Finding all forms
# for form in br.forms():
#    print "Form name:", form.name
#    print form

# Finding all controls
# br.select_form(nr=0)
# for control in br.form.controls:
#     print control
#     print "name=%s" % (control.name)

# Identifying the form (it's hidden, but there's only
# one, so I picked it by identifier)
br.select_form(nr=0)

# Telling mechanize to find the control that 
# corresponds to the second dropdown and setting its value to 
# the one corresponding to the auditor's race
control = br.form.find_control('ctl00$MainContent$cboRaces')
control.value = ['460006719']

# There are two buttons on the page to click,
# 'Choose election' and 'Submit'
br.submit('ctl00$MainContent$btnCountyChange')

# Reading updated page with table
html = br.response().read()

# Bringing in BeautifulSoup from class example
soup = BeautifulSoup(html, "html.parser")

###### 
# Time to get the tables and their headers
######

# Picking out the first table w/ overall election results 
# by candidate
first_table = soup.find('table', 
	{'id': 'MainContent_dgrdRaceResults'}
)

# Encoding the cell text as UTF-8 to keep Python from freaking out on me
# about ASCII
for row in first_table.find_all('tr'):
	headers = [cell.text.encode('utf-8') for cell in row.find_all('th')]
	candidates = [cell.text.encode('utf-8') for cell in row.find_all('td')]
	writer.writerow(headers)
	writer.writerow(candidates)

# Picking out the second table w/ county-by-county results
second_table = soup.find('table',
    {'id': 'MainContent_dgrdCountyRaceResults'}
)


for row in second_table.find_all('tr'):
    headers = [cell.text.encode('utf-8') for cell in row.find_all('th')]
    counties = [cell.text.encode('utf-8') for cell in row.find_all('td')]
    writer.writerow(headers)
    writer.writerow(counties)