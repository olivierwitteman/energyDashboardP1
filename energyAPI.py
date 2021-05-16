from fastapi import FastAPI
from typing import Optional
import os
import subprocess

app = FastAPI()

def tail(f, n):
    proc = subprocess.Popen(['tail', '-n', f'{n}', f], stdout=subprocess.PIPE)
    lines = proc.stdout.readlines()
    return lines

@app.get("/latest/")
def return_metrics(metric: Optional[str] = '', n: Optional[int] = 1):
    data = {'data': [],
            'date': []}
    lines = tail(f=f'{os.path.abspath(os.path.dirname(__file__))}/P1_log.csv', n=int(21*n))

    dates = list(set([d.split(b',')[1] for d in lines]))
    dates.sort()

    trimmedlines = []
    if metric != '':
        for line in lines:
            if any(cond in line for cond in [str.encode(metric), b'TIMESTAMP']):
                trimmedlines.append(line)
    else:
        trimmedlines = lines

    for date in dates:
        keeplines = []
        for line in trimmedlines:
            if date in line:
                keeplines.append({"metric": f"{line.split(b',')[2]} [{line.split(b',')[4]}]",
                                  "value": line.split(b',')[3]})
        data['date'].append(date)
        data['data'].append(keeplines)

    return data
