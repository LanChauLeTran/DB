import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash


app = Flask('Hi')

@app.route('/')
def Hello_World():
    return render_template('hello.html')
    
@app.route('/op')
def op():
    return render_template('op.html')
