from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def main_page():
  return render_template('main.html')

@app.route('/connectiontest')
def test():
  return 'CONNECTION TEST PAGE - Connection Success!'

if __name__=='__main__':
  app.run()
