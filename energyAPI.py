from fastapi import FastAPI
from typing import Optional
import os
import subprocess

app = FastAPI()

def tail(f, n):
    proc = subprocess.Popen(['tail', '-n', f'{n}', f], stdout=subprocess.PIPE)
    lines = proc.stdout.readlines()
    return lines

@app.get("/")
def root():
    return {"msg": "test"}

@app.get("/latest/")
def return_latest():

    lines = tail(f=f'{os.path.abspath(os.path.dirname(__file__))}/P1_log.csv', n=10)
    print(lines)
    return {"msg": lines[0]}

# print(f'{os.path.abspath(os.path.dirname(__file__))}/P1_log.csv')
tail(f=f'{os.path.abspath(os.path.dirname(__file__))}/P1_log.csv', n=10)