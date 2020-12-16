# -*- coding: utf-8 -*-
# 기본 템플릿
import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask import jsonify

from flask_socketio import SocketIO

app = Flask(__name__)
# 세션처리
app.secret_key = 'sakccsdcocjk2sdjkdskcj'
# [2] 시크릿키 지정 (환경변수)
app.config['SECRET_KEY'] = '12341234' #  비밀번호
# [3] SocketIO 생성시 Flask 객체를 래핑
socketio = SocketIO( app, cors_allowed_origins="*", async_mode='threading' )


@app.route('/')
def home():    
    # 렌더링시 데이터를 전달하고 싶으면 키=값 형태로 파라미터를 추가
    # **kargs
    return render_template('index3.html', name='사용자명')


@app.route('/top_buy', methods=['POST','GET'])
def top_buy():
    top_name = request.form.get('option1')
    top_size = request.form.get('option2')
    print(top_name,top_size)
    return render_template('top_buy.html')

@app.route('/top')
def top():
    return render_template('top.html')

@app.route('/original')
def original():
    return render_template('original.html')

@app.route('/test', methods=['POST','GET'])
def test():
    return render_template('test.html')

@app.route('/pants' , methods=['POST','GET'])
def pants():
    return render_template('pants.html')

@app.route('/acc')
def acc():
    return render_template('acc.html')







if __name__ == '__main__':
    #app.run(debug=True)
    # [4] 소켓io를 이용하여 서버가동 (래핑해서 가동)
    socketio.run( app,  debug=True)
