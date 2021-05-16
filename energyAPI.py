from fastapi import FastAPI
from typing import Optional
import os
import subprocess

app = FastAPI()

def tail(f, n):
    proc = subprocess.Popen(['tail', '-n', n, f], stdout=subprocess.PIPE)
    lines = proc.stdout.readlines()
    return lines

@app.get("/")
def root():
    return {"msg": "test"}

@app.get("/latest/")
def return_latest():

    test = tail(f=f'{os.path.abspath(os.path.dirname(__file__))}/P1_log.csv', n=30)
    return {test}