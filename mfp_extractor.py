"""
# Script to log in to myfitnesspal website and extract data
# run as: python mfp_extractor.py USERNAME PASSWORD
#
# sources of code include:
# 
# http://stackoverflow.com/questions/2954381/python-form-post-using-urllib2-also-question-on-saving-using-cookies
# http://stackoverflow.com/questions/301924/python-urllib-urllib2-httplib-confusion
# http://www.voidspace.org.uk/python/articles/cookielib.shtml
#
# mashed together by Martin Chorley
# 
# Licensed under a Creative Commons Attribution ShareAlike 3.0 Unported License.
# http://creativecommons.org/licenses/by-sa/3.0/
"""

import urllib, urllib2
import cookielib
import time
import sys
import os
from datetime import datetime, timedelta
from BeautifulSoup import BeautifulSoup


class MfpExtractor(object):

    def __init__(self, username, password):
        
        # url for website
        self.base_url = 'http://www.myfitnesspal.com'
        # login action we want to post data to
        self.login_action = '/account/login'
        # file for storing cookies
        self.cookie_file = 'mfp.cookies'

        # user provided username and password
        self.username = username
        self.password = password

        # only want to access a page once every 2 seconds 
        #so we don't thrash the mfp server too much
        self.earliest_query_time = time.time()
        self.query_interval = 2 

        # set up a cookie jar to store cookies
        self.cj = cookielib.MozillaCookieJar(self.cookie_file)

        # set up opener to handle cookies, redirects etc
        self.opener = urllib2.build_opener(
            urllib2.HTTPRedirectHandler(),
            urllib2.HTTPHandler(debuglevel=0),
            urllib2.HTTPSHandler(debuglevel=0),
            urllib2.HTTPCookieProcessor(self.cj)
        )

        # pretend we're a web browser and not a python script
        self.opener.addheaders = [('User-agent', 
            ('Mozilla/4.0 (compatible; MSIE 6.0; '
            'Windows NT 5.2; .NET CLR 1.1.4322)'))
        ]

    def access_page(self, path, username, params):

        # go to sleep for as long as necessary to avoid making more than 
        # one call to the website every 2 seconds
        while time.time() < self.earliest_query_time:
            sleep_dur = self.earliest_query_time - time.time()
            time.sleep(sleep_dur)

        # strip the path
        path = path.lstrip('/')
        path = path.rstrip('/')

        # construct the url
        url = self.base_url + '/' + path + '/' + username + '?' + urllib.urlencode(params)
        print url

        # retrieve the web page
        try:
            response = self.opener.open(url)
        except urllib2.HTTPError as e:
            raise e
        except urllib2.URLError as e:
            raise e

        # return the data from the page
        return response.read()

    # method to do login
    def login(self):

        # open the front page of the website to set and save initial cookies
        response = self.opener.open(self.base_url)
        soup = BeautifulSoup(response)
        token = ''
        for attr, value in soup.find('input', attrs={'name': 'authenticity_token'}).attrs:
            if attr == 'value':
                token = value
                print value
        # parameters for login action
        login_data = urllib.urlencode({
            'username' : self.username,
            'password' : self.password,
            'remember_me' : True,
            'authenticity_token' : token
        })

        # construct the url
        login_url = 'https://www.myfitnesspal.com' + self.login_action
        print login_url
        # then open it
        try:
            response = self.opener.open(login_url, login_data)
        except urllib2.URLError as e:
            raise e
        # save the cookies and return the response
        self.cj.save()

        return response

    def get_daily_food_data_from_mfp(self, username, date):

        diary_path = '/food/diary/'
        params = {'date' : date}

        return self.access_page(diary_path, username, params)

    def get_daily_exercise_data_from_mfp(self, username, date):

        diary_path = '/exercise/diary'
        params = {'date' : date}

        return self.access_page(diary_path, username, params)


if __name__ == "__main__":

    args = sys.argv

    # check for username and password and optional number of days to get
    if len(args) not in [3,4]:
        print "Incorrect number of arguments"
        print "Argument pattern: username password [days]"
        exit(1)

    username = args[1]
    password = args[2]

    # check how many days to retrieve
    if len(args) == 4:
        # we've been specified a number of days
        num_days = timedelta(days=float(args[3]))
    else:
        # we haven't, go back 4 weeks
        num_days = timedelta(days=28.0)
    
    print 'Retrieving food and exercise data for %s days' % num_days.days

    # the date we want to go back to in the history
    start_date = datetime.now() - num_days

    # create list of days to get
    dates_to_check = []
    date_to_check = datetime.now()
    one_day = timedelta(days=1)
    while date_to_check - one_day > start_date:
        date_to_check = date_to_check - one_day
        dates_to_check.append(date_to_check)

    # initialise an MfpExtractor to login to the website
    mfp = MfpExtractor(username, password)
    response = mfp.login()

    print response.read()


    # want to store downloaded html files for later processing. Check to see 
    # if the directories already exist, if not then make them.
    cwd = os.getcwd()
    exercise_dirname = os.path.join(username, 'exercise')
    food_dirname = os.path.join(username, 'food')

    exercise_dir = os.path.join(cwd, exercise_dirname)
    food_dir = os.path.join(cwd, food_dirname)

    if not os.path.isdir(exercise_dir):
        os.mkdir(exercise_dir)
    if not os.path.isdir(food_dir):
        os.mkdir(food_dir)

    for date_to_check in dates_to_check:
        fmt_date = date_to_check.strftime('%Y-%m-%d')
        exer_file = os.path.join(exercise_dir, 'exercise_diary_%s.html' % fmt_date)
        if not os.path.isfile(exer_file):
            print 'Exercise file for %s not found, fetching from mfp' % fmt_date
            html = mfp.get_daily_exercise_data_from_mfp(username, fmt_date)
            print 'Exercise file for %s retrieved' % fmt_date
            soup = BeautifulSoup(html)
            out_file = open(exer_file, 'w')
            out_file.write(soup.prettify())
        else:
            print 'Exercise file for %s already downloaded' % fmt_date
        food_file = os.path.join(food_dir, 'food_diary_%s.html' % fmt_date)
        if not os.path.isfile(food_file):
            print 'Food file for %s not found, fetching from mfp' % fmt_date
            html = mfp.get_daily_food_data_from_mfp(username, fmt_date)
            print 'Food file for %s retrieved' % fmt_date
            soup = BeautifulSoup(html)
            out_file = open(food_file, 'w')
            out_file.write(soup.prettify())
        else:
            print 'Food file for %s already downloaded' % fmt_date
