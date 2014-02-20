from binascii import a2b_base64
from datetime import datetime
from mimetypes import guess_extension, guess_type
from multiprocessing import Process, Queue
from queue import Empty

from meetups.models import Meetup
from meetups.forms import MeetupForm

import os
import requests
import sys
import time

class MeetupManager(object):
    """Queueies meetup for the most recent list of Boulder Django meetups."""
    def __init__(self, api_key):
        """Initializes instance variables, fills the database with past
        meetups, and checks that the api key works
        """
        # Set variables
        self.api_key = api_key
        self.meetup_url = 'https://api.meetup.com/2/events?' \
            '&sign=true'                                     \
            '&group_urlname=boulder-django'                  \
            '&page=20'                                       \
            '&key=%s' % (self.api_key, )
        
        # Make sure that the api key works
        req = requests.get(self.meetup_url)
        if req.status_code == 401:
            raise Exception('Your instance of MeetupManager failed. %s' % (
                json.dumps(req.json())
            ))

        # Check for new meetups
        if len(Meetup.objects.all()) == 0:
            url = 'https://api.meetup.com/2/events?' \
                '&sign=true'                         \
                '&status=past'                       \
                '&group_urlname=boulder-django'      \
                '&page=20'                           \
                '&key=%s' % (self.api_key, )
            req = requests.get(url)
            self.parse_meetups(req.json().get("results"))

    def check_meetups(self):
        """Checks the database to see if it needs to load previous meetups
        into the database"""
        req = requests.get(self.meetup_url)
        req_json = req.json()
        meetups = req_json.get('results', [])
        if len(meetups) > 0:
            self.parse_meetups(meetups)

    def get_time(self, unix_time=None):
        if unix_time == None:
            return
        return datetime.fromtimestamp(unix_time/1000.0)

    def parse_meetups(self, data):
        """Parses a request from meetup and saves it into the database"""
        for meetup in data:
            return_meetup = {
                "title": meetup.get('name'),
                "description": meetup.get('description'),
                "date": self.get_time(meetup.get('time')),
                "event_url": meetup.get('event_url'),
                "meetup_id": meetup.get('id')
            }
            venue = meetup.get('venue')
            if venue is not None:
                return_meetup['location_name'] = venue.get('name')
                return_meetup['address'] = venue.get('address_1')
                return_meetup['city'] = venue.get('city')
            self.create_or_update_meetup(return_meetup)

    def create_or_update_meetup(self, data):
        """Pass a dictionary of data to create or save a new meetup."""
        try:
            meetup = Meetup.objects.get(meetup_id=data.get('meetup_id'))
        except:
            meetup = None
        meetup_form = MeetupForm(data, instance=meetup)
        if meetup_form.is_valid():
            meetup_form.save()

    def run(self):
        """Checks for new meetups every hour"""
        while True:
            self.check_meetups()
            time.sleep(60*60)
