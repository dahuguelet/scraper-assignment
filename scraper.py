# Sources:
# http://www.pythonforbeginners.com/cheatsheet/python-mechanize-cheat-sheet
# http://wwwsearch.sourceforge.net/mechanize/faq.html

import urllib2, csv
import mechanize
from bs4 import BeautifulSoup

# output = open('electionresults.csv', 'w')
# writer = csv.writer(output)
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

print br.response().read()

# br.select_form['MainContent_cboRaces')

