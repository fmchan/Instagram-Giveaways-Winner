from configparser import ConfigParser
from modules.instagram_bot import Bot

parser = ConfigParser()
parser.read('config.ini', encoding='utf8')

post_code = parser.get('Required', 'Post Code')
post_link = 'https://www.instagram.com/p/' + post_code
expr = parser.get('Required', 'Expression')
username = parser.get('Required', 'UserName')
password = parser.get('Required', 'Password')

db = parser.getboolean('Optional', 'DB', fallback=False)
window = parser.getboolean('Optional', 'Window', fallback=True)
user_connections = parser.get('Optional', 'UserTarget', fallback=None)
user_participants = parser.get('Optional', 'Participants', fallback=False)
from_followers = parser.getboolean('Optional', 'Followers', fallback=True)
limit = parser.getint('Optional', 'Limit', fallback=None)
timeout = parser.getint('Optional', 'Timeout', fallback=30)
count_comments = parser.getint('Optional', 'Comments', fallback=30)
save_only = parser.getboolean('Optional', 'SaveOnly', fallback=False)

bot = Bot(window, timeout)

print('Logging in...')

bot.log_in(username, password)

print('Logged in successfully!')

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
	connections = bot.get_and_reformat_json(post_code, connections)

#print(connections)

if not save_only:
    print('Let\'s win this giveaway together! Spamming...')
    #bot.read_comment()
    bot.comment_post(post_link, expr, connections, count_comments)

print('Program finished with success!')
