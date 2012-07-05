#!/usr/bin/env python
"""Creates a mock of the delicious data store and stores it in a file

Should be executed only once. The unittest will use the resulting file and
the tests will fail if it changes.

"""
import random
from pprint import pprint
users = ['fulano', 'sicrano', 'beltrano', 'goedel', 'escher', 'bach', 'brahms', 'bartok']
tags = {'programming': [
            ('news.ycombinator.com','hacker news'),
            ('joelonsoftware.com','joel'),
            ('codecomplete.com','codecomplete'),
            ('python.org', 'python'),
            ('django.org', 'django'),
            ('ror.org', 'ruby on rails'),
            ],
        'news': [
            ('nyt.com', 'ny times'),
            ('publico.pt', 'publico'),
            ('dn.pt', 'dn'),
            ('newyorker.com', 'the new yorker'), 
            ('theguardian.co.uk','the guardian'),
            ],
        'photography': [
            ('theonlinephotographer.com', 'online photographer'),
            ('nikonrumors.com', 'nikon rumors'),
            ]
       }
user_posts = {}
for user in users:
    user_tags = user_posts.setdefault(user, {})
    for tag, sites in tags.items():
        user_posts_per_tag = user_tags.setdefault(tag, set())
        for site in sites[0:random.randrange(0, len(sites))]:
            user_posts_per_tag.add(site)
posts = []
for user, tags in user_posts.items():
    for tag, sites in tags.items():
        for site in sites:
            posts.append({
                    'description': site[1],
                    'tags': tag,
                    'url': site[0],
                    'user': user
                    })
with open('mock_delicious.py', 'w') as outfile:
    outfile.write('POSTS = \\\n')
    pprint(posts, outfile)



