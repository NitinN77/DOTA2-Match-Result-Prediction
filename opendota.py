import requests
import pandas as pd
from time import sleep
import json


class API:

	OPENDOTA_URL = "https://api.opendota.com/api/"
	REQUEST_TIMEOUT = 0.3

	def __init__(self, apikey=None):
		if not apikey:
			self.wait = 2
		else: 
			self.wait = 0.2

	def get_public_matches(self, less_than_match_id=None):
		url = self.OPENDOTA_URL + 'publicMatches'
		if less_than_match_id:
			url += '?less_than_match_id=' + str(less_than_match_id)
		r = requests.get(url)
		return json.loads(r.text)

	def get_more_matches(self, less_than_match_id=None, min_mmr=3000, matches_requested=100, columns=['match_id', 'radiant_win', 'avg_mmr', 'radiant_team', 'dire_team']):
		matches = pd.DataFrame()
		mids = []
		current_match_id = less_than_match_id
		matches_found = 0

		url = self.OPENDOTA_URL + 'publicMatches?lessthanmatchid='
		while matches_found < matches_requested:
			try:
				jsons = self.get_public_matches(less_than_match_id=current_match_id)
				current_match_id = jsons[-1]['match_id']
				current_dataframe = pd.io.json.json_normalize(jsons)
				mids.append(current_dataframe['match_id'])
				current_dataframe = current_dataframe[columns]  
				current_dataframe = current_dataframe.loc[current_dataframe["avg_mmr"] > min_mmr]
				matches_found += len(current_dataframe)
				print(matches_found)
				matches = matches.append(current_dataframe, ignore_index=True)
				sleep(self.wait)
			except:
				print("Error")
				continue
		matches = matches.iloc[0:matches_requested]

		return matches, mids

	def get_heroes(self):
		url = self.OPENDOTA_URL + 'heroes'
		#if self.apikey:
		#	payload = {"api_key": self.apikey}
		r = requests.get(url)
		jsons = json.loads(r.text)
		self.heroes = jsons

		return jsons

	def generate_hero_ids_dict(self):
		'''Generate a dictionary mapping hero ids to 0-based index values'''
		if not self.heroes:
			raise NameError(
			    "Run get_heroes() to generate a json of the heroes first, then run generate_hero_ids_dict()")
		heroes = self.heroes
		hero_ids_dict = {}
		n = 0
		for hero in heroes:
			hero_ids_dict[hero["id"]] = n
			n += 1
		self.hero_ids_dict = hero_ids_dict
		return hero_ids_dict

	def generate_hero_dict(self):
		'''Generate a dictionary mapping hero names to hero ids'''
		if not self.heroes:
			raise NameError(
			    "Run get_heroes() to generate a json of the heroes first, then run generate_hero_dict()")
		heroes = self.heroes
		heroes_dict = {}
		for hero in heroes:
			heroes_dict[hero["localized_name"]] = hero["id"]
		self.heroes_dict = heroes_dict
		return heroes_dict

	def parse_matches_for_ml(self, matches=None, file_input=None, file_outputs=None, append=False):
		if file_input:
			matches_json = json.load(file_input)
			matches = pd.io.json.json_normalize(matches_json)
		elif type(matches) != pd.core.frame.DataFrame:
			raise TypeError("Matches should be pandas DataFrame")

		matches_output = []
		results_output = []

		for index, row in matches.iterrows():
			ids = [0]*(len(self.heroes)*2)

			radiant_team = row.loc["radiant_team"].split(',')
			dire_team = row.loc["dire_team"].split(',')
			for hero in radiant_team:
				hero_index = self.hero_ids_dict[int(hero)]
				ids[hero_index] = 1
			for hero in dire_team:
				hero_index = self.hero_ids_dict[int(hero)] + len(self.heroes)
				ids[hero_index] = 1
			matches_output.append(ids)
			if row.loc["radiant_win"] == True:
				results_output.append(1)
			else: results_output.append(0)
		
		if file_outputs:
			if append:
				matches_outputf = open(file_outputs[0], 'r+')
				results_outputf = open(file_outputs[1], 'r+')
				old_matches = json.load(matches_outputf)
				matches_output = matches_output + old_matches
				old_results = json.load(results_outputf)
				results_output = results_output + old_results
				matches_outputf.close()
				results_outputf.close()
				
			matches_outputf = open(file_outputs[0], 'w+')
			results_outputf = open(file_outputs[1], 'w+')
			json.dump(matches_output, matches_outputf)
			json.dump(results_output, results_outputf)
			matches_outputf.close()
			results_outputf.close()

		
		return matches_output, results_output
