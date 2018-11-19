#!/usr/bin/env python2.7

import re
import datetime
import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, abort, url_for, render_template, g, redirect, Response, session
import json
import datetime

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
DATABASEURI = "postgresql://nc2734:4291@35.196.158.126/proj1part2"
engine = create_engine(DATABASEURI)
app.secret_key = 'w4111proj1'




def getPlayerName(playerIDs):
    ans = []
    for playerid in playerIDs:
        try:
            pname = g.conn.execute('SELECT full_name FROM Player WHERE playerID=%s', playerid)
            ans.append(pname.fetchall()[0][0])
        except Exception as e:
            print e
    return ans

def getPlayerInfo(playerName):
    try:
        pinfo = g.conn.execute('SELECT * FROM Player WHERE full_name=%s', playerName)
        return pinfo.fetchall()
    except Exception as e:
        print e
        return []


@app.before_request
def before_request():
    try:
        g.conn = engine.connect()
    except:
        print("uh oh, problem connecting to database")
        import traceback;
        traceback.print_exc()
        g.conn = None


@app.teardown_request
def teardown_request(exception):
    try:
        if session:
          session.clear()
        g.conn.close()
    except Exception as e:
        print "Exception when tear down:", e
        pass


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/register')
def getRegis():
    return render_template("register.html")


@app.route('/login')
def getLogin():
    return render_template("login.html")

@app.route('/register', methods=['POST'])
def register():
    thisname = request.form['usrname']
    password = request.form['password']
    try:
        usernames = g.conn.execute('''SELECT A.username FROM Account A ''')
        for unm in usernames:
            if unm == thisname:
                usernames.close()
                return render_template('register.html', msg='Username exists!')
        g.conn.execute('''INSERT INTO  Account (username, pswd) VALUES (%s, %s)''', (thisname, password))
        usernames.close()
        return render_template('register.html', msg='User:%s registered!'%usernames)
    except Exception as e:
        error = str(e)
        print(error)
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.form['username']
        session['username'] = username
        password = request.form['password']
        session['password'] = password
        uids = g.conn.execute('''SELECT userID FROM Account WHERE username = %s AND pswd = %s''', (username, password))
        uid = uids.fetchone()
        if uid:
            session['uid'] = uid[0]
            s = g.conn.execute('SELECT * FROM Favorites WHERE userID=%s', uid[0])
            uids.close()
            playerIDs = [p[0] for p in s.fetchall()]
            return render_template("profile.html", u=[(uid[0], username)], f=getPlayerName(playerIDs))
    except Exception as e:
        error = str(e)
        print(error)
    return render_template('login.html')

@app.route('/profile')
def profile():
    if 'uid' not in session:
        return render_template('login.html')
    try:
        s = g.conn.execute('SELECT * FROM Favorites WHERE userID=%s', session['uid'])
        playerIDs = [p[0] for p in s.fetchall()]
        return render_template("profile.html", u=[(session['uid'], session['username'])], f=getPlayerName(playerIDs))
    except Exception as e:
        error = str(e)
        print(error)
    return render_template('login.html')




@app.route('/playerName', methods=['POST'])
def showPlayer():
    playerName = request.form['player']
    pinfo = getPlayerInfo(playerName)
    if pinfo:
        return render_template("playerInfo.html", p=pinfo)
    return render_template("index.html")

@app.route('/leagueMatch', methods=['POST'])
def showMatch():
    leagueName = request.form['leagueName']
    try:
        matchInfo = g.conn.execute('SELECT * FROM Match WHERE compName=%s', leagueName)
        return render_template("leagueMatch.html", m=matchInfo)
    except Exception as e:
        error = str(e)
        print(error)
    return render_template("index.html")

@app.route('/favourites')
def addFav():
    if "uid" not in session:
        return render_template('login.html')
    try:
        players = g.conn.execute('SELECT * FROM Player')
        s = g.conn.execute('SELECT playerID FROM Favorites WHERE userID=%s', session['uid'])
        favoured = set([i[0] for i in s])
        cands = []
        for player in players:
            if player[0] not in favoured:
                cands.append(player)
        return render_template('favourites.html', cands)

    except Exception as e:
        error = str(e)
        print(error)
        return render_template('index.html')

if __name__ == "__main__":
    import click


    @click.command()
    @click.option('--debug', is_flag=True)
    @click.option('--threaded', is_flag=True)
    @click.argument('HOST', default='0.0.0.0')
    @click.argument('PORT', default=8111, type=int)
    def run(debug, threaded, host, port):
        HOST, PORT = host, port
        print("running on %s:%d" % (HOST, PORT))
        app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


    run()



