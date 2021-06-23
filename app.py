#!/usr/bin/python3
#-*- coding: utf-8 -*-

from flask import Flask, render_template, request
from mod_pkg.Webinit import search
from mod_pkg.Webinit import searchall
app = Flask(__name__)

@app.route('/')
def main_page():
    return render_template('main.html', rest=searchall())
    #return render_template('main.html', rest={'site': ['t1', 't2', 't3', 't4', 't5'], 'title': ['t1', 't2', 't3', 't4', 't5'], 'host': ['testhost', 'h2', 'h3', 'h4', 'h5'], 'ddaying': ['진행', '진행', 'jj', 'jj', 'jj'], 'Dday': ['0', '1', '2', '3', '4']})

#추후 elasticsearch 결과코드로 대체될 예정
@app.route('/connectiontest')
def test():
  return 'CONNECTION TEST PAGE - Connection Success!'
@app.route('/search_action', methods=['GET','POST'])
def searchaction():
  rch = request.form['search']
  setpr = request.form['setp']
  print(rch)
  print(setpr)
  res = search(rch, setpr)

  return res


if __name__=='__main__':
  ipaddr="127.0.0.1"
  print("Starting the service with ip_addr="+ipaddr)
  app.run(debug=False, host=ipaddr, port=5000)
