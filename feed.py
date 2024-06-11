import requests
import rss_parser
import rss_parser.models
import rss_parser.models.rss
import rss_parser.models.rss.channel
import rss_parser.models.rss.item

class Deviation:
    def __init__(self):
        self.name = ""
        self.author = ""
        self.url = ""
        self.nsfw = False
        self.date = ""
        self.description = ""
        self.image_url = ""
        self.thumb_url = ""

class Gallery:
    def __init__(self):
        self.title = ""
        self.description = ""
        self.deviations = [Deviation()]
        self.count = 0


def list_popular():
    base_url = "https://backend.deviantart.com/rss.xml?type=deviation"
    res_dict = Gallery()

    res_raw = requests.get(base_url)
    if (res_raw.status_code != 200):
        return None
    
    res_raw_lines = res_raw.text.splitlines()
    res_rss = rss_parser.RSSParser.parse(res_raw.text)

    res_dict.title = res_rss.channel.title.content
    res_dict.description = res_rss.channel.description.content
    #print("[DEBUG]")
    #print(type(res_rss.channel))
    #print(type(res_rss.channel.content))
    #print(type(res_rss.channel.content.items))

    for i in res_rss.channel.items:
        for a in res_raw_lines:
            if i.content.guid.content in a:
                res_raw_author = res_raw_lines[res_raw_lines.index(a) + 7]
                break
        
        res_dict.deviations.append(Deviation())
        res_dict.deviations[res_dict.count].name = i.content.title.content
        res_dict.deviations[res_dict.count].author = res_raw_author[53:-15]
        res_dict.deviations[res_dict.count].date = i.content.pub_date.content
        res_dict.deviations[res_dict.count].url = i.content.guid.content

        res_dict.count += 1
    
    return