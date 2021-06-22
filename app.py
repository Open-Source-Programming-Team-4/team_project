from flask import Flask, render_template, request
from mod_pkg.Webinit import search
app = Flask(__name__)

@app.route('/')
def main_page():
    return render_template('main.html', rest={'site': ['t1', 't2'], 'title': ['t1'], 'host': ['testhost'], 'ddaying': ['진행'], 'Dday': ['0']})
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
  app.run()
