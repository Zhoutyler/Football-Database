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

def getPlayerInfo(playerName, playerID=''):
    try:
        if playerName:
            pinfo = g.conn.execute('SELECT * FROM Player WHERE full_name=%s', playerName)
        else:
            pinfo = g.conn.execute('SELECT * FROM Player WHERE playerID=%s', playerID)
        return pinfo.fetchall()[0]
    except Exception as e:
        print e
        return ()

def getTransfer(playerID):
    try:
        tinfo = g.conn.execute('SELECT * FROM Transfers WHERE playerID=%s',playerID)
        return tinfo.fetchall()
    except Exception as e:
        print "exception:", e
        return []


@app.before_first_request
def before_first_request():
    if session:
        session.clear()

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
        g.conn.close()
    except Exception as e:
        print "Exception when tear down:", e
        pass


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/playerInfo', methods=['POST'])
def showPlayer():
    playerName = request.form['player']
    pinfo = getPlayerInfo(playerName)
    if pinfo:
        tinfo = getTransfer(str(pinfo[0]))
        return render_template("playerInfo.html", n=pinfo, t=tinfo)
    return render_template("index.html")


@app.route('/register')
def getRegis():
    return render_template("register.html")


@app.route('/login')
def getLogin():
    return render_template("login.html")

@app.route('/register', methods=['POST'])
def register():
    thisname = request.form['username']
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
            playerIDs = [p[1] for p in s.fetchall()]
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
        playerIDs = [p[1] for p in s.fetchall()]
        return render_template("profile.html", u=[(session['uid'], session['username'])], f=getPlayerName(playerIDs))
    except Exception as e:
        error = str(e)
        print(error)
    return render_template('login.html')


@app.route('/leagueMatch', methods=['POST'])
def showMatch():
    leagueName = request.form['league']
    try:
        matchInfo = g.conn.execute('SELECT * FROM Match WHERE compName=%s', leagueName)
        return render_template("leagueMatch.html", r=matchInfo)
    except Exception as e:
        error = str(e)
        print(error)
    return render_template("index.html")


@app.route('/clubInfo', methods=['POST'])
def showClub():
    clubName = request.form['club']
    try:
        cinfo = [list(r) for r in g.conn.execute('SELECT * FROM Club WHERE clubName=%s', clubName).fetchall()]
        cname = g.conn.execute('SELECT * FROM Coach WHERE coachID=%s', str(cinfo[0][3])).fetchall()[0][1]
        cinfo[0][3] = cname
        finfo = g.conn.execute('SELECT * FROM Competition WHERE recent_champion=%s', clubName).fetchall()
        return render_template('clubInfo.html', b=cinfo, t=finfo)
    except Exception as e:
        error = str(e)
        print(error)
        return render_template('index.html')


@app.route('/playerFilter', methods=['POST'])
def playerFilter():
    try:
        flt = request.form['filter']
        val = request.form['val']
        players = g.conn.execute('SELECT * FROM Player WHERE %s > %s', flt, val).fetchall()
        return render_template("playersFilter.html", f=flt, v=str(val), p=players, t=[])
    except Exception as e:
      print "exception:", e
    return render_template("index.html")

@app.route('/compare', methods=['POST'])
def cmp():
    name1 = request.form['name1']
    name2 = request.form['name2']
    p1 = getPlayerInfo(name1)
    p2 = getPlayerInfo(name2)
    return render_template("compare.html", p=[p1, p2])

@app.route('/addFavorite', methods=['POST'])
def addFavorite():
    if 'uid' not in session:
        return render_template("login.html")
    playerID = request.form['playerID']
    pinfo = getPlayerInfo('', playerID)
    tinfo = getTransfer(playerID)
    addedBefore = g.conn.execute('SELECT * FROM Favorites WHERE userID=%s AND playerID=%s', session['uid'], playerID)
    res = addedBefore.fetchall()
    print res
    if res:
        return render_template("playerInfo.html", n=pinfo, t=tinfo, msg='Already in Favorites')
    g.conn.execute('''INSERT INTO Favorites (userID, playerID) VALUES (%s, %s)''', (session['uid'], playerID))
    return render_template("playerInfo.html", n=pinfo, t=tinfo, msg='Added to Favorites')












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



