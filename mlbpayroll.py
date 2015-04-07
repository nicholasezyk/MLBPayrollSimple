import urllib2
import string
import copy
import datetime
import time
import random
 
#grip: a function that takes a url in quotes (e.g., "http://www.google.com" and returns the source code in a string) 
def grip(url):
        page =urllib2.urlopen(url)
        data=page.read()
        return data
 
#snip: a function that skips past unnecessary data, giving you everything in that string after. 
#For instance, on the string "The quick brown fox jumps over the lazy dog.", 
#calling snip('The quick brown fox jumps over the lazy dog.', 'over ') gives "the lazy dog." as its return value. 
def snip(src, key):
        h = copy.deepcopy(src)
        if key not in h:
                return src
        else:
                num = string.find(src, key)
                num = num + len(key)
                h = h[num:]
                #print(h)
                return h

#clip: a function that retrieves a piece of data, giving you everything until a given string.
#For instance, on the string "She got a big booty, so I call her Big Booty",
#calling clip('She got a big booty, so I call her Big Booty', "big booty") gives "She got a " as its return value.
#Note the space at the end of the return value. 
def clip(src, key):
        h = copy.deepcopy(src)
        if key not in h:
                return src
        else:
                num = string.find(h, key)
                h = h[:num]
                #print(h)
                return h

#grabbing the initial site base, opening the text file and giving it its headers
url = "http://www.baseball-reference.com"
p = open("payroll.txt", 'w')
p.write("TeamName PayrollMillions 2014Wins" + '\n')

#initializing our list of lists and getting the source code for the teams splash page
info = []
master = grip(url + "/teams")

#while we haven't yet collected all 30 teams, we skip forward to the meat of the source code...
while '<td align="right" >247,760</td>' in master:

        #grabbing the franchise name 
        master = snip(master, 'class=" franchise_names">')
        master = snip(master, '<a href="')
        team_url = url + clip(master, '">')

        #setting up the second-level of the array to store each team's data
        team_info = []

        #cutting through to get the team name
        team_name = clip(master, '</a></td>')
        team_name = snip(team_name, '">')
        print(team_name)

        #cutting out the spaces and adding the team name to the list
        team_name = team_name.replace(' ', '')
        team_info.append(team_name)

        #getting the team's page and cutting through to the payroll page
        team_page = grip(team_url)
        team_page = snip(team_page, ' 40-man Roster</a> / <a href="')

        #cutting through the payroll page to the relevant data
        ext = clip(team_page, '">')
        #print(url + ext)
        team_payroll_page = grip(url + ext)
        team_payroll_page = snip(team_payroll_page, 'Est. Total Payroll w/o Options <small>(Guaranteed + Arb + Other)</small></td>')
        team_payroll_page = snip(team_payroll_page, '<td align="right" >$')

        #getting the payroll info and adding the payroll
        team_payroll = clip(team_payroll_page, 'M')
        team_info.append(team_payroll)

        #parsing through to get the wins
        team_page = snip(team_page, '2014</a></td>')
        team_page = snip(team_page, '162</td>')
        team_page = snip(team_page, '<td align="right" >')

        #collecting the wins and recording it
        team_wins = clip(team_page, '</td>')
        team_info.append(team_wins)

        #showing off our completed team info and writing it to the text file
        print(team_info)
        p.write(team_name + ' ' + team_payroll + ' ' + team_wins + '\n')

        #cutting through to get a good starting point for the next team
        master = snip(master, "</tr>")

#the while loop is completed, so we're finished! We close the text file and can load it into R for further analysis
p.close()





