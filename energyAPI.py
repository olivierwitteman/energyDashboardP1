from fastapi import FastAPI
from typing import Optional
import os
import subprocess

app = FastAPI()

def tail(f, n):
    # print(f'tail -n {n} {f}')
    proc = subprocess.Popen(['tail', '-n', f'{n}', f], stdout=subprocess.PIPE)
    lines = proc.stdout.readlines()
    return lines

@app.get("/")
def root():
    return {"msg": "test"}

@app.get("/latest/")
def return_metrics(metric: Optional[str] = '', n: Optional[int] = 1):
    data = {'data': [],
            'date': []}
    lines = tail(f=f'{os.path.abspath(os.path.dirname(__file__))}/P1_log.csv', n=int(21*n))
    lines.reverse()

    dates = list(set([d.split(b',')[1] for d in lines]))[:n]
    #
    # print(dates)


    for date in dates:
        keeplines = []
        for line in lines:
            if all(cond in line for cond in date+str.encode(metric)):
                keeplines.append({f"{line.split(b',')[2]} [{line.split(b',')[4]}]": line.split(b',')[3]})
        data['date'].append(date)
        data['data'].append(keeplines)


    return {"msg": data}

# print(return_metrics(n=2, metric='POWER_L1'))