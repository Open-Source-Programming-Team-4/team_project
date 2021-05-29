from flask import Flask
app = Flask(__name__)

@app.route('/')
def main_page():
  return '대외활동 및 공모전 모음 - 사용자 맞춤형 대외활동 검색 추천 서비스'

@app.route('/connectiontest')
def test():
  return 'CONNECTION TEST PAGE'
