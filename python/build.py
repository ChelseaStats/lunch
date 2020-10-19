 # importing modules
import os
import pathlib
import tweepy
import urllib
import json
import helper
import random

# authentication
auth = tweepy.OAuthHandler(os.getenv('c_key'), os.getenv('c_secret'))
auth.set_access_token(os.getenv('a_token'), os.getenv('a_secret'))
api = tweepy.API(auth)

# processing
root = pathlib.Path(__file__).parent.parent.resolve()
with open( root / "data.json", 'r') as filehandle:
    random_item = random.choice(json.load(filehandle))
    name  = random_item.get('Name')
    twitter_handle = random_item.get('Twitter') or None
    facebook = helper.get_social_list(random_item, 'Facebook')
    url = helper.get_social_list(random_item, 'Url')
    twitter = helper.get_social_list(random_item, 'Twitter')
    instagram = helper.get_social_list(random_item, 'Instagram')
    url_safe_text    = urllib.parse.quote(name)
    output_markdown  = f"## {name}\n\n"
    output_markdown += f"Contact details:\n\n"
    output_markdown += f"- [Location](https://www.google.com/maps/place/{url_safe_text}+Cheltenham/)\n"
    output_markdown += f"{url} {facebook} {twitter} {instagram}"

if __name__ == "__main__":
    readme = root / "README.md"
    readme_contents = readme.open().read()
    my_markdown = helper.replace_chunk(readme_contents, "lunch_item", output_markdown)
    readme.open("w").write(my_markdown)
    if(twitter):
        tweet = f"Venue of the day in #Cheltenham is {name}, see lunch.thechels.uk for more info {twitter_handle} #LunchBot #VofD"
    else:
        tweet = f"Venue of the day in #Cheltenham is {name}, see lunch.thechels.uk for more info #LunchBot #VofD"
    print(tweet)
    api.update_status(status = tweet)
