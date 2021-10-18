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
    ('queue_type', ''),
)

#makes request
response = requests.get('{}/rates/totals_filter_by_queues.json'.format(chaves['npx_url']), params=params, cookies=cookies, verify=False)

#json from API response
res = response.json()

#creates the message string
mensagem = open('model.txt', 'r', encoding='utf8').read()
mensagem = mensagem.replace('{dep_name}', dep.capitalize())
mensagem = mensagem.replace('{time}', str(hora))
mensagem = mensagem.replace('{avg_duration}', res['duration_answered'])
mensagem = mensagem.replace('{avg_waiting}', res['wait'])
mensagem = mensagem.replace('{ans_calls}', str(res['answered']))
mensagem = mensagem.replace('{total_calls}', str(res['answered'] + res['not_answered']))
mensagem = mensagem.replace('{day}', str(hoje.day).zfill(2))
mensagem = mensagem.replace('{month}', str(hoje.month).zfill(2))
mensagem = mensagem.replace('{perc_ans}', str(round( (res['answered'] / (res['answered'] + res['not_answered']) ) * 100, 2)) )

#dumps the message into the variables json
variaveis['report'] = mensagem
with open('variables.json', 'w', encoding='utf8') as write_file:
    json.dump(variaveis, write_file)
