def readfile(filename):
    pass

def pearson(v1, v2):
    pass

class bicluster:
    pass

def hcluster(rows, distance=pearson):
    pass

"""
>>> import clusters
>>> blognames, words, data = clusters.readfile('blogdata.txt')
>>> clust = clusters.hcluster(data)
"""

def printclust(clust, labels=None, n=0):
    pass

"""
>>> reload(clusters)
>>> clusters.printclust(clust, labels=blognames)
"""
