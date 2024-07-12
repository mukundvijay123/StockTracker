import json
import os 


def get_profile():
    env=os.environ.get("STOCKS")
    profile_fp=open(os.path.join(env,r"json/profile.json"),"r+")
    profile_dict=json.load(profile_fp)
    return profile_dict


    

