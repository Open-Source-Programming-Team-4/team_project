from flask import Flask, render_template, request
from mod_pkg.Webinit import search
app = Flask(__name__)

@app.route('/')
def main_page():
  return render_template('main.html')

@app.route('/connectiontest')
def test():
  return 'CONNECTION TEST PAGE - Connection Success!'
@app.route('/search_action', methods=['GET','POST'])
def searchaction():
  rch = request.form['search']
  res = search(rch)

  return res


if __name__=='__main__':
  app.run()
