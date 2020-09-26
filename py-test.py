from configparser import ConfigParser
import yaml
with open('post_detail.yaml', encoding="utf8") as f:
    conf = yaml.safe_load(f)

parser = ConfigParser()
parser.read('config.ini', encoding='utf8')

post_code = parser.get('Required', 'Post Code')

#items = parser.items('section')

posts = {
  "fsjiffsfs" : {
    "expression" : "@ @ @",
    "comments" : 20
  },
  "faFRWR34" : {
    "expression" : "@ @",
    "comments" : 10
  },
  "FSD434sfd" : {
    "expression" : "@",
    "comments" : 30
  }
}
list_of_keys = list(posts.keys())
#print(list_of_keys[0])
#print(posts.get("fsjiffsfs").get("expression"))

print(conf[0]['code'])
codes = ','.join([ exp['code'] for exp in conf ])
print(codes)
for post in conf:
	mcm = post['mcm'] if 'mcm' in post else 0
	if 'mcm' not in post or 'exp' not in post:
		print(mcm)