import re
from robobrowser import RoboBrowser
import random
import time

# Browse to Poshmark
browser = RoboBrowser(history=True)
browser.open('https://poshmark.com/login')

# Get username and pw from text file
# First line of text file must be in the following form:
# 'username password'
# the info array will have two entire, the username and pw
# at indices 0 and 1
userInfo = open('userInfo.txt','r')
info = userInfo.read().split(' ')
	
# fill out the form with necessary inputs
form = browser.get_form(id = 'email-login-form')
form                # <RoboForm q=>
form['login_form[username_email]'].value = info[0]
form['login_form[password]'].value = info[1]
browser.submit_form(form)

#Actually do the search
searchList = raw_input('What would you like to search for? Separate your search queries with spaces: ')
sum = 0;

# Initialize the link-holder array and the query array
linksToVisit = []
searchQuery = searchList.split(' ')

# Iterate through all the search values
for searchVal in searchQuery:
	browser.open('https://poshmark.com/search?query=' + searchVal + '&type=people')

	# Compile list of users to go to
	print 'Here are all users you are going to visit from search ' + searchVal + ':'
	
	for link in browser.find_all('a'):
		if (str(link.get('href'))[:6] == '/user/' and str(link.get('href'))[-12:] == '/follow_user'):
	   		linksToVisit.append(str(link.get('href')))
	   		print link.get('href')

	# Actually visits them. And sleeps a lot too.
	if (len(linksToVisit) == 0):
		print 'No users were returned'
	else:
		for url in linksToVisit:
			timetosleep = int(random.random() * 10)
			print 'sleeping for ' + str(timetosleep) + ' seconds.'
			time.sleep(timetosleep)
			print 'followed user ' + url
			browser.open('https://poshmark.com' + url)
			time.sleep(int(random.random() * 2))
			browser.back()
	
	# Keep adding to our cummulative amount
	sum = sum + len(linksToVisit)
	print 'Done! ' + info[0] + ' just followed ' + str(len(linksToVisit)) + ' people.'

	# Delete everything in the linksToVisit array
	del linksToVisit[:]

	print 'Note: You may have already followed some of these people...'

print 'Your total amount of follows is ' + str(sum) + '.'

# Bugs:
# 1. How to scroll down.
# 2. How do you know if the person is already followed.
