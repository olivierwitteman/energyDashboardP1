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
def return_metrics(metric: Optional[str] = None, n: Optional[int] = 1):
    data = {}
    lines = tail(f=f'{os.path.abspath(os.path.dirname(__file__))}/P1_log.csv', n=21*n).reverse()
    last_sample = lines[0].split(",")[1]

    dates = list(set([lambda d: d.split(',')[1] for d in lines]))

    print(dates)

    for line in lines:
        pass

        # if last_sample in line:

    return {"msg": lines}
