# -*- coding: utf-8 -*-
""" Simple rss to html converter """
import StringIO
from feedparser import parse as parsefeed
from bs4 import BeautifulSoup as bs
from unicodedata import normalize


def flatten_unicode_keys(dic):
    '''pass unicode keywords to **kwargs '''
    for key in dic.keys():
        if isinstance(key, unicode):
            value = dic[key]
            del dic[key]
            dic[normalize('NFKD',key).encode('ascii','ignore')] = value


def entry2html(**kwargs):
    """ Format feedparser entry """
    flatten_unicode_keys(kwargs)
    title = kwargs['title']
    link = kwargs['link']
    description = kwargs['description']
    template = u"""
    <h2 class='title'>{title}</h2>
    <a class='link' href='{link}'>{title}</a>
    <span class='description'>{description}</span>
    """
    return template.format(title=title, link=link, description=description).encode('utf-8')


def convert_feed(**kwargs):
    """ Main loop """
    flatten_unicode_keys(kwargs)
    out = StringIO.StringIO("")
    for entry in parsefeed(kwargs['url']).entries:
        title = entry['title']
        link = entry['link']
        description = entry['description']
        print >> out, entry2html(title=title, link=link, description=description)
    return bs(out.getvalue(), 'lxml').prettify()


def save_file(url, fname):
    ''' Save data to disc'''
    print fname
    with open(fname, 'w') as file_object:
        file_object.write(convert_feed(url=url).encode('utf-8'))

save_file('http://stackoverflow.com/feeds', 'index.html')
