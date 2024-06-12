import requests
import feedparser

class Deviation:
    def __init__(self, name="", author="", url="", date="", image=""):
        self.name = name
        self.author = author
        self.url = url
        self.nsfw = False
        self.date = date
        self.description = ""
        self.image_url = image
        self.thumb_url = ""

class Gallery:
    def __init__(self):
        self.title = ""
        self.description = ""
        self.deviations = []


def list_popular():
    base_url = "https://backend.deviantart.com/rss.xml?type=deviation"
    res_dict = Gallery()

    res_raw = requests.get(base_url)
    if (res_raw.status_code != 200):
        return None
    
    res_raw_lines = res_raw.text.splitlines()
    res_rss = feedparser.parse(base_url)

    res_dict.title = res_rss["feed"]["title"]
    res_dict.description = res_rss["feed"]["description"]
    
    #print("[DEBUG]")
    #print("Title: " + str(res_rss["feed"]["title"]))
    #print("Description: " + str(res_rss["feed"]["description"]))
    #print("\nItems:")

    img_pos = 0
    for i in res_rss["entries"]:
        for a in res_raw_lines:
            if i["link"] in a:
                res_raw_author = res_raw_lines[res_raw_lines.index(a) + 7]
                break
        
        for a in res_raw_lines:
            if "media:content" in a:
                if res_raw_lines.index(a) > img_pos:
                    res_raw_image = res_raw_lines[res_raw_lines.index(a)]
                    img_pos = res_raw_lines.index(a)
                    break

        res_dict.deviations.append(Deviation(i["title"], res_raw_author[53:-15], i["link"], i["published"], str(res_raw_image[res_raw_image.find("media:content") + 19:res_raw_image.find("medium") - 27].strip('"'))))

    #for i in res_dict.deviations:
    #    print("'" + i.name + "' by " + i.author)
    #    print(i.url)
    #    print("Published on " + i.date + "\n")
    #    print("Image stored at: " + i.image_url + "\n")

    return res_dict