'''/
Author: @king
Date: 5/30/2014
Description: Gaiaonine gbot [ daily chance, slots, dumpster-dive, multi-account]
Website: www.glitch.sx
Version: 4.1.100
Keywords: gaiaonline, avatar, forum, login, forms, python, hack, cheat, bot, script, tool, mechanize, automated
cheat, gold, gen, generator, tektek, golden, engine, how, to, bot, chaos, working, daily chance, slots, dumpster-dive, multi,
mule, farm, engine, botters,
'''
from gbot import gbot
import hel

def main():
	#- Helpy makes sure you have mechanize, avoids ugly break if you dont.
	helpy = hel.helpy()
	helpy.require("mechanize")
	account_list = helpy.list_builder("accounts.txt") #also handles file readng into list
	for line in account_list: #Iterate through accounts
		u,p = line.split(',') #split username and password data up
		gbot(u,p).start() #start gbot for user

main()
