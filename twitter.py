#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mechanize
import string
import cookielib
from bs4 import BeautifulSoup
import time

# Twitter Login
def login(username,password):
  try:
    print "Trying to connect to Twitter ..."
    br = mechanize.Browser()

    cookies = cookielib.LWPCookieJar()
    br.set_cookiejar(cookies)

    br.set_handle_equiv(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.set_debug_http(False)
    br.set_debug_responses(False)
    br.set_debug_redirects(False)
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time = 1)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    #br.set_proxies({"http": PROXYNAME})

    br.open('http://twitter.com/')
    br.select_form(nr=1)

    br['session[username_or_email]'] = username
    br['session[password]'] = password
    br.submit()
    return br
  except:
    print "Failed to connect!"

# Beautifulsoup Debugging
def print_forms(br):
  page = br.response().read()
  soup = BeautifulSoup(page, "html.parser");
  forms = soup.find_all("form")
  print forms[0]

# Sending Tweet
def tweet(text,br):
  try:
    print "Sending Tweet ..."
    br.open('https://mobile.twitter.com/compose/tweet')
    br.select_form(nr=0)
    br['tweet[text]'] = text
    br.submit()
  except:
    print "Failed to send Tweet!"

# Unfollowing specified User
def unfollow(user,br):
  try:
    print "Unfollowing "+user
    br.open('https://mobile.twitter.com/'+user+'/unfollow')
    br.select_form(nr=0)
    br.submit()
  except:
    print "Failed to unfollow "+user

# Follow specified User
def follow(user,br):
  try:
    print "Following "+user
    br.open('https://mobile.twitter.com/'+user)
    br.select_form(nr=0)
    br.submit()
  except:
    print "Failed to follow "+user

# Executin Program
br = login("TechFryer", "ZzAg5frD")
tweet("HEYYY WAHTAATATAT", br)
follow("BraunPhilipp", br)
