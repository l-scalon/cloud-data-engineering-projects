import os, wget, json, io

def new_page(work_dir):
    file = os.path.join(work_dir, 'tweets.html')
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
        for id in id_list[:10]:
            html = get_content(id)
            page.write(html)

def build(tweet_ids, work_dir):
    page = new_page(work_dir)
    write_content(page, tweet_ids)
    page.close