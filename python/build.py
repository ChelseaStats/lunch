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
error = False
list_of_venues = []

class venue:
        def __init__(self, name, hijack, desc, url, facebook, twitter, instagram):
                self.name = name
                self.hijack = hijack
                self.desc = desc or "coming soon!"
                self.url = url or None
                self.facebook = facebook or None
                self.twitter = twitter or None
                self.instagram = instagram or None
                self.location = f"https://www.google.com/maps/place/{urllib.parse.quote(name)}+Cheltenham/"
        def __repr__(self):
            return repr(self.name, self.hijack, self.desc, self.url, self.facebook, self.twitter, self.instagram, self.location)

# processing
root = pathlib.Path(__file__).parent.parent.resolve()
with open( root / "data.json", 'r') as filehandle:
    for a in json.load(filehandle):
        list_of_venues.append(venue(a['Name'],a['Hijack'],a['Desc'],a['Url'] or None, a['Facebook'],a['Twitter'],a['Instagram']))
        count_hijacks = 1 if (a['Hijack'] == 'true') else 0
    print("Total number of hijacks: ", count_hijacks)

    chosen_venue = venue
    if(count_hijacks > 1):
        print("Error: too many hijacks!")
        error = True
    elif(count_hijacks == 1):
        chosen_venue = list(filter(lambda venue: venue.hijack == 'true', list_of_venues))[0]
    else:
        chosen_venue = random.choice(list_of_venues)

if(error is False):
    # construct string
    output_markdown  = f"## Venue of the day is: {chosen_venue.name}\n\n"
    output_markdown += f"### About\n\n"
    output_markdown += f"{chosen_venue.desc}\n\n"
    output_markdown += f"### Contact details\n\n"
    output_markdown += helper.get_social_list(chosen_venue.location,"Map")
    output_markdown += helper.get_social_list(chosen_venue.url,"Url")
    output_markdown += helper.get_social_list(chosen_venue.twitter,"Twitter")
    output_markdown += helper.get_social_list(chosen_venue.facebook,"Facebook")
    output_markdown += helper.get_social_list(chosen_venue.instagram,"Instagram")

    if __name__ == "__main__":
        readme = root / "README.md"
        readme_contents = readme.open().read()
        my_markdown = helper.replace_chunk(readme_contents, "lunch_item", output_markdown)
        readme.open("w").write(my_markdown)
        if(chosen_venue.twitter):
            tweet = f"Venue of the day in #Cheltenham is {chosen_venue.name}, see lunch.thechels.uk for more info {chosen_venue.twitter} #LunchBot #VofD"
        else:
            tweet = f"Venue of the day in #Cheltenham is {chosen_venue.name}, see lunch.thechels.uk for more info #LunchBot #VofD"
        print(tweet)
        #api.update_status(status = tweet)
