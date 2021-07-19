import json
import opendota

api = opendota.API()
api.get_heroes()
api.generate_hero_ids_dict()
matches, mids = api.get_more_matches(matches_requested=50000, min_mmr=0)
parsed_matches = api.parse_matches_for_ml(matches, file_outputs=["matches.json", "results.json"], append=False)
print(mids)
