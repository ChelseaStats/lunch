import urllib

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