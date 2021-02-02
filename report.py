import json, requests, time
from datetime import date

#loads variables from json files
variaveis = json.load(open('variables.json', 'r'))
chaves = json.load(open('keys.json', 'r'))
dep = variaveis['arg']

#creates time and date objects
hoje = date.today()
t = time.localtime()
hora = time.strftime("%H:%M", t)

#prepare cookies
cookies = {
    '_npx_session': chaves['npx_session']
}

#prepare params
params = (
    ('queue', dep),
    ('sla', '30'),
    ('queue_type', ''),
)

#makes request
response = requests.get('{}/rates/details_by_queue_by_interval.json'.format(chaves['npx_url']), params=params, cookies=cookies, verify=False)

#json from API response
res = response.json()

#creates the message string
mensagem = open('model.txt', 'r').read()
mensagem = mensagem.replace('{dep_name}', dep.capitalize())
mensagem = mensagem.replace('{time}', str(hora))
mensagem = mensagem.replace('{avg_duration}', res['totals'][0]['duration_avg'])
mensagem = mensagem.replace('{avg_waiting}', res['totals'][0]['wait_avg'])
mensagem = mensagem.replace('{total_time}', res['totals'][0]['total_time'])
mensagem = mensagem.replace('{ans_calls}', str(res['totals'][0]['total_answered']))
mensagem = mensagem.replace('{total_calls}', str(res['totals'][0]['total_calls']))
mensagem = mensagem.replace('{day}', str(hoje.day).zfill(2))
mensagem = mensagem.replace('{month}', str(hoje.month).zfill(2))
mensagem = mensagem.replace('{perc_ans}', res['totals'][0]['perc_answered'])

#dumps the message into the variables json
variaveis['report'] = mensagem
with open('variables.json', 'w') as write_file:
    json.dump(variaveis, write_file)