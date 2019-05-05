#!/usr/bin/python
# -*- coding: UTF-8 -*- 
# filename: flask.py

import json
from flask import Flask,render_template


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/hyatt/<string:date>', methods=['GET'])
def get_page(date):
    print(date)
    path = 'data/%s.json' % date
    with open(path, 'r', encoding='utf-8') as f:
        j = f.read()
        #print(j)
        #return j
        hotels = json.loads(j)
    return render_template('template.html', date=date, hotels=hotels)


if __name__ == '__main__':
    app.run(port=2779, debug=False)

    
#path = 'data/2019-05-08.json'
#with open(path, 'r', encoding='utf-8') as f:
#    j = f.read()
#
#data = json.loads(j)
