import json
import requests
import time
from datetime import date, datetime
import warnings
warnings.filterwarnings("ignore")

# loads variables from json files
variaveis = json.load(open('variables.json', 'r'))
chaves = json.load(open('keys.json', 'r'))
dep = variaveis['arg']

# creates time and date objects
hoje = date.today()
t = time.localtime()
hora = time.strftime("%H:%M", t)

# prepare cookies
cookies = {
    '_npx_session': chaves['npx_session']
}

# prepare params
params = (
    ('queue', dep),
    ('queue_type', ''),
)

# json from API response
res = {}


# makes request
try:
    deptos = chaves['groups'][dep]
    res = {
        'duration_answered': '00:00:00',
        'wait': '00:00:00',
        'answered': 0,
        'not_answered': 0
    }
    for depto in deptos:
        params = (
            ('queue', depto),
            ('queue_type', ''),
        )
        response = requests.get('{}/rates/totals_filter_by_queues.json'.format(
            chaves['npx_url']), params=params, cookies=cookies, verify=False)
        res['duration_answered'] = str((datetime.strptime(res['duration_answered'], '%H:%M:%S') - datetime.strptime(
            '00:00:00', '%H:%M:%S') + datetime.strptime(response.json()['duration_answered'], '%H:%M:%S')).time())
        res['wait'] = str((datetime.strptime(res['wait'], '%H:%M:%S') - datetime.strptime(
            '00:00:00', '%H:%M:%S') + datetime.strptime(response.json()['wait'], '%H:%M:%S')).time())
        res['answered'] += response.json()['answered']
        res['not_answered'] += response.json()['not_answered']
    res['duration_answered'] = time.strftime('%H:%M:%S',time.localtime((((time.mktime(time.strptime("00:00:00","%H:%M:%S"))*(len(deptos)-1))+time.mktime(time.strptime(res['duration_answered'],"%H:%M:%S")))/len(deptos))))
    res['wait'] = time.strftime('%H:%M:%S',time.localtime((((time.mktime(time.strptime("00:00:00","%H:%M:%S"))*(len(deptos)-1))+time.mktime(time.strptime(res['wait'],"%H:%M:%S")))/len(deptos))))
except:
    response = requests.get('{}/rates/totals_filter_by_queues.json'.format(
        chaves['npx_url']), params=params, cookies=cookies, verify=False)
    res = response.json()

# creates the message string
mensagem = open('model.txt', 'r', encoding='utf8').read()
mensagem = mensagem.replace('{dep_name}', dep.capitalize())
mensagem = mensagem.replace('{time}', str(hora))
mensagem = mensagem.replace('{avg_duration}', res['duration_answered'])
mensagem = mensagem.replace('{avg_waiting}', res['wait'])
mensagem = mensagem.replace('{ans_calls}', str(res['answered']))
mensagem = mensagem.replace('{total_calls}', str(
    res['answered'] + res['not_answered']))
mensagem = mensagem.replace('{day}', str(hoje.day).zfill(2))
mensagem = mensagem.replace('{month}', str(hoje.month).zfill(2))
mensagem = mensagem.replace('{perc_ans}', str(
    round((res['answered'] / (res['answered'] + res['not_answered'])) * 100, 2)))

# dumps the message into the variables json
variaveis['report'] = mensagem
with open('variables.json', 'w', encoding='utf8') as write_file:
    json.dump(variaveis, write_file)
