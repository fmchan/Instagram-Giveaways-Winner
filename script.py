from configparser import ConfigParser
from modules.instagram_bot import Bot
import yaml
import time

parser = ConfigParser()
parser.read('config.ini', encoding='utf8')

#post_code = parser.get('Required', 'Post Code')
#post_link = 'https://www.instagram.com/p/' + post_code
#expr = parser.get('Required', 'Expression')
username = parser.get('Required', 'UserName')
password = parser.get('Required', 'Password')

comment_json = parser.get('Optional', 'Collect Comment File Path', fallback=None)
can_create_comment_json = parser.getboolean('Optional', 'Create Comment Json', fallback=False)
includeTagged = parser.getboolean('Optional', 'Include Tagged', fallback=True)
db = parser.getboolean('Optional', 'DB', fallback=False)
window = parser.getboolean('Optional', 'Window', fallback=True)
user_connections = parser.get('Optional', 'UserTarget', fallback=None)
user_participants = parser.get('Optional', 'Participants', fallback=False)
from_followers = parser.getboolean('Optional', 'Followers', fallback=True)
limit = parser.getint('Optional', 'Limit', fallback=None)
timeout = parser.getint('Optional', 'Timeout', fallback=30)
#count_comments = parser.getint('Optional', 'Comments', fallback=30)
save_only = parser.getboolean('Optional', 'SaveOnly', fallback=False)

with open('post_detail.yaml', encoding="utf8") as f:
    posts = yaml.safe_load(f)

bot = Bot(window, timeout)

if can_create_comment_json:
  print('Create Comment Json by PHP...')
  bot.create_comment_json_by_php(','.join([ c['code'] for c in posts ]), comment_json)
  # getting all codes as an array then reformat it as a string with comma among them

print('Logging in...')

bot.log_in(username, password)

print('Logged in successfully!')

for post in posts:
    if 'code' not in post or 'exp' not in post:
        continue
    post_link = 'https://www.instagram.com/p/' + post["code"]
    count_comments = mcm = post['mcm'] if 'mcm' in post else 20

    if not user_connections:
        print('Searching for post\'s owner')
        
        user_connections = bot.get_user_from_post(post_link)
        
        print('Post\'s owner found!')

    print(f'Searching and saving {"followers" if from_followers else "followings"}...')

    if db:
    	connections = bot.get_user_json(username)
    else:
    	connections = bot.get_user_connections(user_connections,
    									   username=username,
                                           limit=limit,
                                           followers=from_followers)

    	print(('followers' if from_followers else 'followings') + '\' database complete!')

    if user_participants:
    	connections = bot.get_and_reformat_json(post['code'], connections, includeTagged)

    #print(connections)
    start_time = time.time()

    if not save_only:
        print('Let\'s win this giveaway together! Spamming...')
        #bot.read_comment()
        bot.comment_post(post_link, post["exp"], connections, count_comments)

    print('Program finished with success!')
    print("--- %s seconds ---" % (time.time() - start_time))
