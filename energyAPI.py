from fastapi import FastAPI
from typing import Optional
import os
import subprocess
import uvicorn
# import pandas as pd

app = FastAPI()


def tail(f, n):
    proc = subprocess.Popen(['tail', '-n', f'{n}', f], stdout=subprocess.PIPE)
    lines = proc.stdout.readlines()
    return lines


@app.get("/usage/power/")
def return_deltas(n: int):
    dict = {}
    dict_1 = return_minutes(metric='USED_TARIFF_1', n=n)
    dict_2 = return_minutes(metric='USED_TARIFF_2', n=n)
    dict['values'] = [int(60. * (float(dict_1['values'][i+1]) - float(dict_1['values'][i]) + float(dict_2['values'][i+1]) - float(dict_2['values'][i]))) for i in range(len(dict_1['values'])-1)]
    dict['dates'] = dict_1['dates'][1:]
    dict['unit'] = 'kW'

    return dict


@app.get("/usage/electricity/")
def return_deltas(n: int):
    dict = {}
    dict_1 = return_minutes(metric='USED_TARIFF_1', n=n)
    dict_2 = return_minutes(metric='USED_TARIFF_2', n=n)
    dict['values'] = [(float(dict_1['values'][i+1]) - float(dict_1['values'][i]) + float(dict_2['values'][i+1]) - float(dict_2['values'][i])) for i in range(len(dict_1['values'])-1)]
    dict['dates'] = dict_1['dates'][1:]
    dict['unit'] = 'kWh'

    return dict


@app.get("/usage/gas/")
def return_deltas(n: int):
    dict = return_minutes(metric='HOURLY_GAS', n=n)
    dict['values'] = [(float(dict['values'][i+1]) - float(dict['values'][i])) for i in range(len(dict['values'])-1)]
    dict['dates'] = dict['dates'][1:]
    dict['unit'] = 'm3'

    return dict


@app.get("/minute/")
def return_minutes(metric: str, n: int):
    data = {'dates': [],
            'values': []}

    lines = tail(f=f'{os.path.abspath(os.path.dirname(__file__))}/P1_log.minute', n=int(21 * n))

    dates = list(set([d.split(b',')[1] for d in lines]))
    dates.sort()

    trimmedlines = []

    for line in lines:
        if any(cond in line for cond in [str.encode(metric)]):
            trimmedlines.append(line)

    print(trimmedlines)
    for date in dates:
        for line in trimmedlines:
            if date in line:
                data['dates'].append(date)
                data['values'].append(float(line.split(b',')[3]))

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
                "deliveredTarrif2": state[7],
                "gasMeter": state[8]}


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
                                  "value": float(line.split(b',')[3]),
                                  "unit": line.split(b',')[4],
                                  "date": date})

        data['data'].append({"sample": keeplines})

    return data


if __name__ == '__main__':
    uvicorn.run("energyAPI:app", host="192.168.178.42", port=8000)
