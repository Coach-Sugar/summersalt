import requests
import json
import ast
import pandas

university_completions = "https://datausa.io/api/data?measures=Completions&drilldowns=PUMA,University"
engineering_completions = "https://datausa.io/api/data?CIP=14&drilldowns=PUMA&measure=Completions"

university_completions_json = requests.get(university_completions).json()
engineering_completions_json = requests.get(engineering_completions).json()

table = {}

for i in range(len(university_completions_json['data'])):
	state = university_completions_json['data'][i]['PUMA'].split(", ")[-1]
	graduates = university_completions_json['data'][i]['Completions']
	if state in table.keys():
		table[state]['Graduates by State'] += graduates
	else:
		table[state] = {}
		table[state]['Graduates by State'] = graduates

for i in range(len(engineering_completions_json['data'])):
	state = engineering_completions_json['data'][i]['PUMA'].split(", ")[-1]
	graduates = engineering_completions_json['data'][i]['Completions']
	if state in table.keys():
		if 'Engineers by state' in table[state].keys():
			table[state]['Engineers by state'] += graduates
		else:
			table[state]['Engineers by state'] = graduates
	else:
		table[state] = {}
		table[state]['Engineers by state'] = graduates

print(table['AL']['Engineers by state'])

for i in table.keys():
	if 'Engineers by state' in table[i].keys():
		table[i]['Percent Engineers'] = (table[i]['Engineers by state'] / table[i]['Graduates by State']) * 100

df = pandas.DataFrame.from_dict(table)
	
print(df)


