import os, wget, json, io, absolute
from datetime import datetime

def new_page(folder):
    file = os.path.join(folder, 'tweets.html')
    return io.open(file, "w", encoding = 'utf-8')

def get_content(id):
    url ='https://api.twitter.com/1.1/statuses/oembed.json?id=' + id
    wget.download(url, 'content.json')
    with io.open('content.json', encoding = 'utf-8') as j:
        content = json.loads(j.read())
    html = content['html']
    os.remove('content.json')
    return html

def write_content(page, tweet_ids):
    for actor, id_list in tweet_ids.items():
        title = '<h2 style="font-family:Helvetica;color:#000000;">' + actor + '</h2>'
        page.write(title)
        for id in id_list:
            html = get_content(id)
            page.write(html)

def new_folder():
    now = datetime.now()
    date_and_time = now.strftime("%Y-%m-%d_%H-%M-%S")
    path = os.path.join(absolute.path(), 'tweets', date_and_time)
    os.mkdir(path)
    return path

def build(tweet_ids):
    folder = new_folder()
    page = new_page(folder)
    write_content(page, tweet_ids)
    page.close