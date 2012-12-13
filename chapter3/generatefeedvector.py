import re
import feedparser

def getwordcounts(url):
    """Returns title and dictionary of wordcounts for an RSS feed"""
    feed = getfeed(url)
    wc = {}
    for entry in feed.entries:
        if entry.has_key('summary'):
            article = entry.summary
        else:
            article = entry.description
        body = entry.title + ' ' + article
        for word in re.split('[^\w]', strip_html(body)):
            normalized_word = word.strip().lower()
            if normalized_word == '':
                continue
            wc.setdefault(normalized_word, 0)
            wc[normalized_word] += 1
    return feed.feed.title, wc

def strip_html(html):
    return re.sub('<.+?>', '', html)

def getfeed(url):
    return feedparser.parse(url)

def main():
    pass

if __name__ == '__main__':
    main()


