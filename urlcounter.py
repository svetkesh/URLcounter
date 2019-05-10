#!/usr/bin/python3
# import section
import os
import random
import time
from flask import Flask, request, render_template, session, flash, redirect, \
    url_for, jsonify
from celery import Celery
from urllib.request import Request, urlopen
from urllib.error import URLError
import ssl
from bs4 import BeautifulSoup
import collections
from datetime import datetime
from pymongo import MongoClient
import datetime

# settings and config
app = Flask(__name__)

app.config['SECRET_KEY'] = 'p8jIyjKbnjdhbej4k4jojar9eitmngkapr9gu'

# Celery configuration
# app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'  # local
# app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

app.config['CELERY_BROKER_URL'] = 'redis://:password@redis-12785.c135.eu-central-1-1.ec2.cloud.redislabs.com:12785/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://:password@redis-12785.c135.eu-central-1-1.ec2.cloud.redislabs.com:12785/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

uri = "mongodb+srv://make_it_eazy:109hkjh6bh23ioeqwrHiTqbi@cluster0-amwcq.mongodb.net/test?retryWrites=true"
client = MongoClient(uri)

def insert_one_doc(doc):
    """ Insert document into MongoDB remote base."""
    em = client['em']
    queries = em.queries
    doc_id = queries.insert_one(doc).inserted_id
    return doc_id

# Default route
@app.route('/')
def index():
    return render_template('index.html')

# route for dealing with AJAX request
@app.route('/process', methods= ['POST'])
def process():
    address = request.form['address']
    if address:
        task = parse_tags.apply_async(args=[address])
        return jsonify({'202' : {'Location': url_for('taskstatus',
                                                     task_id=task.id)}})
    return jsonify({'output' : 'Missing data!'})

# address retriever and parser, and DB writer
@celery.task(bind=True)
def parse_tags(self, *args):
    start_parse_task = datetime.datetime.utcnow()
    address = args[0]

    # generate some test data for javascript
    # for i in range(10):
    #     # as list
    #
    #     # result = []
    #     # # result = random.random()
    #     # div = ['div',random.randint(1, 100)]
    #     # a = ['a',random.randint(1, 100)]
    #     # p = ['p',random.randint(1, 100)]
    #     # tags = [div, a, p]
    #     # for tag in tags:
    #     #     result.append(tag)
    #     # print(result)
    #
    #     # # result as dictionary OK
    #     # result = {}
    #     # # result = random.random()
    #     # result['div'] = random.randint(1, 100)
    #     # result['a'] = random.randint(1, 100)
    #     # result['p'] = random.randint(1, 100)
    #     # print(result)
    #     #
    #     #
    #     # result.add(r)
    #     # result = result.add(['a',random.randint(1, 100)])
    #     # print(result)
    #     # time.sleep(0.2)
    #     # self.update_state(state='PROGRESS',
    #     #               meta={'address': args,
    #     #                     'status': 'PROGRESS',
    #     #                     'result': result})

    # parser for fake / real page
    # req = Request('https://www.rabota.ua/',
    #                 headers={'User-Agent': 'Mozilla/5.0'}) # gives 697 tags
    try:
        req = Request(address, headers={'User-Agent': 'Mozilla/5.0'})
        html_page = urlopen(req).read()
    except URLError as e:
        print(f"URLError error reason: {e.reason}")
        if "certificate" in str(e.reason):
            # workaround outdated SSL sertificates
            context = ssl._create_unverified_context()
            req = Request(address, headers={'User-Agent': 'Mozilla/5.0'})
            html_page = urlopen(req, context=context).read()
        else:
            print(f"Exception while fetching page: {type(e)} , {e}")
            html_page = '<html> </html>'

    except Exception as e:
        # permissive execution - user can fetch next address
        print(f"Exception while fetching page: {type(e)} , {e}")
        html_page = '<html> </html>'

    soup = BeautifulSoup(html_page, 'html.parser')  # works fine
    all_tags = [tag.name for tag in soup.find_all()]
    c = collections.Counter()
    c.update(all_tags)

    c.most_common()  # https://docs.python.org/3/library/collections.html
    counted_tags = dict(c)
    # could count only most common tags
    # counted_tags_most_common = dict(c.most_common(5))
    self.update_state(state='PROGRESS',
                  meta={'address': args,
                        'status': 'PROGRESS',
                        'result': counted_tags})

    end_parse_task = datetime.datetime.utcnow()
    doc_to_store_in_db = {"address": address,
                          "starttime": start_parse_task,
                          "endtime": end_parse_task}

    try:
        insert_result = insert_one_doc(doc_to_store_in_db)
        # print(f"insert_result: {insert_result}")
    except Exception as e:
        print(f"Exception while writing to db: {type(e)} , {e}")

    return {'address': address,
            'status': 'SUCCESS',
            'result': counted_tags,
            'starttime': start_parse_task,
            'endtime': end_parse_task}

# Query queue and return data for result display
@app.route('/status/<task_id>')
def taskstatus(task_id):
    task = parse_tags.AsyncResult(task_id)

    response = {
        'state': task.state,
        'status': task.status,
        'result': task.result,
        }

    return jsonify(response)

# start main
if __name__ == '__main__':
    # app.run(debug=True)
    app.run()
