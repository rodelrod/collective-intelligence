#!/usr/bin/env python
"""Playing with recommendation systems

Code supporting Chapter 2 of "Programming Collective Intelligence",
First Edition

"""
from __future__ import division
from math import sqrt
from collections import defaultdict

class ArgumentError(Exception):
    pass

# A dictionary of movie critics and their ratings of a small
# set of movies
critics = {
    'Lisa Rose': {
        'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5, 
        'Just My Luck': 3.0, 'Superman Returns': 3.5, 
        'You, Me and Dupree': 2.5, 'The Night Listener': 3.0},
    'Gene Seymour': {
        'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 
        'Just My Luck': 1.5, 'Superman Returns': 5.0, 
        'The Night Listener': 3.0, 'You, Me and Dupree': 3.5},
    'Michael Phillips': {
        'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0, 
        'Superman Returns': 3.5, 'The Night Listener': 4.0}, 
    'Claudia Puig': {
        'Snakes on a Plane': 3.5, 'Just My Luck': 3.0, 
        'The Night Listener': 4.5, 'Superman Returns': 4.0, 
        'You, Me and Dupree': 2.5},
    'Mick LaSalle': {
        'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
        'Just My Luck': 2.0, 'Superman Returns': 3.0, 
        'The Night Listener': 3.0, 'You, Me and Dupree': 2.0},
    'Jack Matthews': {
        'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 
        'The Night Listener': 3.0, 'Superman Returns': 5.0, 
        'You, Me and Dupree': 3.5},
    'Toby': {
        'Snakes on a Plane':4.5, 'You, Me and Dupree':1.0,
        'Superman Returns':4.0}
}


def sim_distance(prefs, person1, person2):
    shared_movies = get_shared_movies(prefs, person1, person2)
    if len(shared_movies) == 0:
        return 0
    else:
        sum_squares = sum([ pow(prefs[person1][film]-prefs[person2][film], 2) 
                            for film in prefs[person1].keys() 
                            if film in prefs[person2].keys() 
                          ])
        return 1./(1. + sqrt(sum_squares))

def get_shared_movies(prefs, person1, person2):
    return [m for m in prefs[person1].keys() if m in prefs[person2].keys()] 

def get_rating_across_movie_list(prefs, person, movie_list):
    return [prefs[person][m] for m in movie_list] 

def average(seq):
    return sum(seq)/len(seq)

def stdev(seq):
    N = len(seq)
    avg = average(seq)
    return sqrt(sum([(s-avg)**2 for s in seq])/N)

def stdev2(seq):
    N = len(seq)
    return sqrt(sum([s**2 for s in seq])/N - (sum(seq)/N)**2)

def cov(seq1, seq2):
    if len(seq1) != len(seq2):
        raise ArgumentError("Both argument sequences must have the same length.")
    N = len(seq1)
    eXY = sum([seq1[i]*seq2[i] for i in range(0,N)])/N
    eX = sum([s for s in seq1])/N
    eY = sum([s for s in seq2])/N
    return eXY - (eX * eY)

def pearson_corr(seq1, seq2):
    return cov(seq1, seq2)/(stdev2(seq1)*stdev2(seq2))

def sim_pearson(prefs, person1, person2):
    shared_movies = get_shared_movies(prefs, person1, person2)
    if len(shared_movies) == 0:
        return 0
    else:
        ratings = [get_rating_across_movie_list(prefs, person, shared_movies)
                   for person in [person1, person2]]
        return pearson_corr(ratings[0], ratings[1])

# Returns the best matches for person from the prefs dictionary.
# Number of results and similarity function are optional params.
def topMatches(prefs, person, n=5, similarity=sim_pearson):
    all_matches = [(similarity(prefs, person, other), other) 
                   for other in prefs.keys()
                   if person != other]
    all_matches.sort()
    all_matches.reverse()
    return all_matches[0:n]

def getRecommendations(prefs,person,similarity=sim_pearson):
    """Gets recommendations for a person by using a weighted average
    of every other user's rankings
    
    """
    weighted_similarities = dict((
            (other, similarity(prefs, person, other)) 
            for other in prefs.keys() if other != person))
    # Eliminate critics with negative correlation (I'm not sure why
    # this is a good idea)
    for critic, sim in weighted_similarities.items():
        if sim <= 0:
            del weighted_similarities[critic]
    sum_ratings = defaultdict(int)      # int() initializes to 0
    sum_weights = defaultdict(int)
    for other, weight in weighted_similarities.items():
        for movie, rating in prefs[other].items():
            sum_ratings[movie] += rating * weight
            sum_weights[movie] += weight
    recommendations = [(sum_ratings[movie]/sum_weights[movie], movie)
                       for movie in sum_ratings.keys()
                       if movie not in prefs[person].keys()]
    recommendations.sort()
    recommendations.reverse()
    return recommendations

def transformPrefs(prefs):
    new_prefs = defaultdict(dict)
    for person, movies in prefs.items():
        for movie, rating in movies.items():
            new_prefs[movie][person] = rating
    return new_prefs





