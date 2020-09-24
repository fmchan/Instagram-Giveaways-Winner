import subprocess
import json

'''
result = subprocess.run(
    ['php', '/Library/WebServer/Documents/php-test.php'],    # program and arguments
    stdout=subprocess.PIPE,  # capture stdout
    check=True               # raise exception if program fails
)
names = json.loads(result.stdout)         # result.stdout contains a byte-string
print(names[0])
'''

comment_json = 'C:\\www\\scraper\\collect-comment.php'
code = 'CFW31dHDwRr'

result = subprocess.run(
    ['php', comment_json, code],    # program and arguments
    stdout=subprocess.PIPE,  # capture stdout
    check=True               # raise exception if program fails
)
'''
#result = subprocess.check_output(['php', comment_json, code], stdout=subprocess.PIPE)
#result.wait()

#start and process things, then wait
#p = subprocess.Popen(['php', comment_json, code])
#p.communicate() #now wait plus that you can send commands to process
'''
#print(list(result.stdout.decode('utf-8')))
try:
    with open(f'records/tags/'+code+'.json', 'r') as file:
    	tags = json.load(file)
    	print(tags[0])
    
except FileNotFoundError:
    pass
#data = json.loads(json.dumps(result.stdout))
#print(data)
'''
tweets = []
for line in open(result.stdout.decode('utf-8'), 'r'):
    tweets.append(json.loads(line))
print(tweets)
print(len(tweets))
print(tweets[0])
'''