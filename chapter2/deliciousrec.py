#!/usr/bin/env python
import pydelicious as pydlc

def initialize_userdict(tag, count=5):
    user_dict = {}
    # get the top count' popular posts
    for popular in pydlc.get_popular(tag='programming')[0:count]:
        # find all users that posted this
        for post in pydlc.get_urlposts(popular['url']):
            user_dict[post['user']] = {}
    return user_dict
