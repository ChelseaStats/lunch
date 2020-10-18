 # importing modules
"""
 Build and Tweet
"""
import os
import re
import csv
import random
import pathlib
import tweepy
import urllib

# setup
root = pathlib.Path(__file__).parent.parent.resolve()

# authentication
auth = tweepy.OAuthHandler(os.getenv('c_key'), os.getenv('c_secret'))
auth.set_access_token(os.getenv('a_token'), os.getenv('a_secret'))
api = tweepy.API(auth)

# functions
def replace_chunk(content, marker, chunk):
    replacer = re.compile(
        r"<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->".format(marker, marker),
        re.DOTALL,
    )
    chunk = "<!-- {} starts -->\n{}\n<!-- {} ends -->".format(marker, chunk, marker)
    return replacer.sub(chunk, content)

# processing
with open('data.csv') as csvfile:
    reader          = csv.DictReader(csvfile)
    random_row      = random.choice(list(reader))
    data_item_text  = random_row['text']
    url_safe_text   = urllib.parse.quote(data_item_text)
    output_markdown = f"# [{data_item_text}](https://www.google.com/maps/place/{url_safe_text}+Cheltenham/)"

if __name__ == "__main__":
    readme = root / "README.md"
    readme_contents = readme.open().read()
    my_markdown = replace_chunk(readme_contents, "lunch_item", output_markdown)
    readme.open("w").write(my_markdown)
    print (data_item_text)
    api.update_status(status = f"#Cheltenham #LunchBot Today's lunchtime venue is {data_item_text}, see lunch.thechels.uk for more info")
