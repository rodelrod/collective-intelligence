#!/usr/bin/env python
"""Retrieve data from del.icio.us to form recommendations."""
from __future__ import division
import sys
import pydelicious as pydlc

def update_progress(progress):
    """Fancy progress bar"""
    done_bars = progress//10
    sys.stdout.write('\r[{0}{1}] {2}%'.format(
                '*' * done_bars, 
                ' ' * (10 - done_bars), 
                progress))
    sys.stdout.flush()

def initialize_userdict(tag, count=5):
    """Form a dict with a group of users sampled from delicious.
    
    tag -- used as a seed for popular posts from which to get the users
    count -- number of posts used as seed

    """
    user_dict = {}
    # get the top count' popular posts
    for popular in pydlc.get_popular(tag='programming')[0:count]:
        # find all users that posted this
        for post in pydlc.get_urlposts(popular['url']):
            user_dict[post['user']] = {}
    if '' in user_dict.keys():
        del user_dict['']   # this was polluting our results
    return user_dict

def fill_items(user_dict):
    """Classify posts with 1 if the user submited post, 0 otherwise."""
    users = user_dict.copy()  # copy&return instead of changing in place
    all_urls = []
    update_progress(0)
    nb_users = len(users)
    user_count = 1
    for user, urls in users.items():
        try:
            posts = pydlc.get_userposts(user)
        except pydlc.PyDeliciousException:
            del users[user]
            continue
        finally:
            user_count += 1
        for post in posts:
            urls[post['url']] = 1.0
            all_urls.append(post['url'])
        update_progress(int((user_count/nb_users)*100))
    for user, urls in users.items():
        for url in all_urls:
            if not urls.has_key(url):
                urls[url] = 0.0
    return users

            

