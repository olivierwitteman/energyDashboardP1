from fastapi import FastAPI
from typing import Optional
import os
import subprocess

app = FastAPI()

def tail(f, n):
    print(f'tail -n {n} {f}')
    proc = subprocess.Popen(['tail', '-n', f'{n}', f], stdout=subprocess.PIPE)
    lines = proc.stdout.readlines()
    return lines

@app.get("/")
def root():
    return {"msg": "test"}

@app.get("/latest/")
def return_metrics(metric: Optional[str] = None, n: Optional[int] = 1):
    data = {}
    lines = tail(f=f'{os.path.abspath(os.path.dirname(__file__))}/P1_log.csv', n=int(21*n))
    lines.reverse()

    dates = list(set([d.split(b',')[1] for d in lines]))[:n]
    #
    print(dates)


    for date in dates:
        keeplines = []
        for line in lines:
            if all(cond in line for cond in date+bytes(metric)):
                keeplines.append(line)
        data['date'] = date
        data['data'] = keeplines


    return {"msg": data}

return_metrics(n=2)