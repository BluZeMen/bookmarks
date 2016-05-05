import threading
from queue import Queue
from threading import Thread
from urllib.error import HTTPError
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

import time
import random

# количество потоков обслуживающих очередь
num_worker_threads=3


def parse(bookmark):
    try:
        with urlopen(Request(bookmark.url), timeout=3) as link:
            doc = BeautifulSoup(link, 'html.parser')
    except HTTPError as e:
        print('Parsing failed:', e)
        return

    head = doc.head
    try:
        bookmark.title = head.title.string
    except:
        pass
    try:
        bookmark.description = head.find(lambda tag: tag.name.lower() == 'meta'
                                                     and tag.has_attr('name')
                                                     and tag['name'].lower() == 'description')['content']
    except:
        pass

    try:
        bookmark.favicon = head.find(lambda tag: tag.name == 'link' and 'icon' in tag['rel'])['href']
        if bookmark.favicon[0] is '/' and bookmark.favicon[1] is not '/':
            o = urlparse(bookmark.url)
            bookmark.favicon = o.scheme + '://' + o.netloc + bookmark.favicon
        elif bookmark.favicon[0] is '.':
            bookmark.favicon = bookmark.url.split('/')[:-1].join('/') + bookmark.favicon
    except:
        pass


def worker():
    while True:
        item = tasks_queue.get()
        print('Started task by: '+str(threading.current_thread()) + 'bookmark: ' + str(item))
        item.save()
        parse(item)
        time.sleep(random.randint(4, 8))  # Для наглядности многопоточного выполнения
        item.save()
        print('Finished task by: ' + str(threading.current_thread()) + 'bookmark: ' + str(item))
        tasks_queue.task_done()


tasks_queue = Queue()


for i in range(num_worker_threads):
    t = Thread(target=worker)
    t.setDaemon(True)
    t.start()


def parse_bookmark(bookmark):
    tasks_queue.put(bookmark)

