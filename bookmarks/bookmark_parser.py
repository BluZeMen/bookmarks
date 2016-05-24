""" Bookmarks parsing module
bookmarks_parse.py
"""
import time
import random
import threading
from queue import Queue
from threading import Thread
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import urlopen, Request

from django.conf import settings
from bs4 import BeautifulSoup


def parse(bookmark):
    """
    Parsing function, which get title, description and favicon of internet page.
    Function specifies title, description and favicon fields of Bookmark object in argument
    :param bookmark:
        Bookmark instance with specified url
    :return:

    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3)' +
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
        with urlopen(Request(bookmark.url, data=None, headers=headers), timeout=3) as link:
            doc = BeautifulSoup(link, 'html.parser')
    except HTTPError as e:
        print('Parsing failed (http error):', e)
        return False
    except URLError as e:
        print('Parsing failed (url error):', e)
        return False

    fails = 0
    head = doc.head
    try:
        bookmark.title = head.title.string
    except:
        print('Parsing warning: can\'t get a title of page')
        fails += 1

    try:
        bookmark.description = head.find(lambda tag: tag.name.lower() == 'meta'
                                                     and tag.has_attr('name')
                                                     and tag['name'].lower() == 'description')['content']
    except:
        print('Parsing warning: can\'t get a description of page')
        fails += 1

    try:
        bookmark.favicon = head.find(lambda tag: tag.name == 'link' and 'icon' in tag['rel'])['href']
        if bookmark.favicon[0] is '/' and bookmark.favicon[1] is not '/':
            u = urlparse(bookmark.url)
            bookmark.favicon = u.scheme + '://' + u.netloc + bookmark.favicon
        elif bookmark.favicon[0] is '.':
            bookmark.favicon = bookmark.url.split('/')[:-1].join('/') + bookmark.favicon
    except:
        print('Parsing warning: can\'t get a favicon of page')
        fails += 1

    if fails is 3:
        print('Parsing error: bad page')
        return False

    return True


def worker():
    """
    Thread worker
    """
    while True:
        item = _tasks_queue.get()
        print('Started task by: ' + str(threading.current_thread()) + 'bookmark: ' + str(item))
        item.save()
        tries = getattr(settings, 'NUMBER_OF_TRIES_TO_PARSE', 3)
        for i in range(tries):
            if parse(item):
                break
            else:
                print('Trying to parse again')
                time.sleep(1)

        time.sleep(random.randint(3, 6))  # for illustrating of multithreading
        item.save()
        print('Finished task by: ' + str(threading.current_thread()) + 'bookmark: ' + str(item))
        _tasks_queue.task_done()


_tasks_queue = Queue()

for i in range(getattr(settings, 'PARSING_THREADS_COUNT', 2)):
    t = Thread(target=worker)
    t.setDaemon(True)
    t.start()


def parse_bookmark(bookmark):
    """
    This function is main interface of bookmark parse module.
    As argument accepts a Bookmark instance with specified url
    """
    _tasks_queue.put(bookmark)
