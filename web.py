import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash


app = Flask('DataBase')

@app.route('/')
def home():
    return render_template('home.html')
    
@app.route('/student')
def student():
    return render_template('student.html')
