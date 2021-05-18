from fastapi import FastAPI
from typing import Optional
import os
import subprocess
import uvicorn
import pandas as pd

app = FastAPI()


def tail(f, n):
    proc = subprocess.Popen(['tail', '-n', f'{n}', f], stdout=subprocess.PIPE)
    lines = proc.stdout.readlines()
    return lines


@app.get("/latest/")
def return_metrics(metric: Optional[str] = '', n: Optional[int] = 1):
    data = {'data': []}
    lines = tail(f=f'{os.path.abspath(os.path.dirname(__file__))}/P1_log.csv', n=int(21*n))

    dates = list(set([d.split(b',')[1] for d in lines]))
    dates.sort()

    trimmedlines = []
    if metric != '':
        for line in lines:
            if any(cond in line for cond in [str.encode(metric)]):
                trimmedlines.append(line)
    else:
        trimmedlines = lines

    for date in dates:
        keeplines = []
        for line in trimmedlines:
            if date in line:
                keeplines.append({"metric": str(line.split(b',')[2], 'utf-8'),
                                  "value": str(line.split(b',')[3], 'utf-8'),
                                  "unit": line.split(b',')[4],
                                  "date": date})

        data['data'].append({"sample": keeplines})

    return data


@app.get("/state/")
def return_state():
    with open(f'{os.path.abspath(os.path.dirname(__file__))}/P1.state', 'r') as register:
        state = register.readline().split(',')
        return {"L1_positive": state[0],
                "L1_negative": state[1],
                "currentUsage": state[2],
                "currentDelivery": state[3],
                "usedTarrif1": state[4],
                "usedTarrif2": state[5],
                "deliveredTarrif1": state[6],
                "deliveredTarrif2": state[7]}


if __name__ == '__main__':
    uvicorn.run("energyAPI:app", host="192.168.178.42", port=8000)
