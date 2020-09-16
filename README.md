# Instagram-Giveaways-Winner

![GitHub top language](https://img.shields.io/github/languages/top/fytex/Instagram-Giveaways-Winner?style=for-the-badge)
![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/fytex/Instagram-Giveaways-Winner?style=for-the-badge)
![GitHub last commit](https://img.shields.io/github/last-commit/fytex/Instagram-Giveaways-Winner?style=for-the-badge)


##### Instagram Bot which when given a post code will spam mentions to increase the chances of winning


## How does this bot work?
It works as a browser simulator using selenium.

Original from Fytex:
1. Log in
2. Find user from post
3. Find followers/followings
4. Start spamming mentions in the post

My modification:
1. Log in
2. Find user from post
3. read a json file (A) which is a list of all users who are playing the giveaway and also the friends they have tagged
4. read a json file (B) which is a list of all users who are following you
5. reformat these two json files
    5.1. form a list (C) which only keeps the users who are following you in list A
    5.2. form a list (D) take away the users in list C from list A and shuffle these users
    5.3. concatenate list C and D to be the final connection list
6. Start spamming mentions in the post
    6.1. delay 2-10 seconds for each comment write
    6.2. like other comments for each 4 comment writes in a row
    6.3. wait 30 seconds when it meets "Couldn't post comment" alert
    6.4. increase the waiting time if the alert still exist
    6.5. stop and complete when the comment write hits the limit


### Why do I modify?
1. Fytex's bot only allows a very limited comment writes like 5
2. Fytex's bot fetchs all the followers/followings, which take a very long waiting time
3. fetching followers/followings from target user doesn't make sense since most of the giveaway requires tagging friends
4. my bot does like comments for avoiding a single robotic action detected.
5. for the point 3 and 4 of my modification. I will explain it later for fetching two json lists from another bot I made with PHP
6. i have to thank for Fytex's great contribution. If I have seen further, it is by standing upon the shoulders of giants.


### Pre-Setup Warning

Before installing you need to be aware that this folder contains binary files (.exe, .etc) inside `drivers`' folder from an old ChromeDriver's release for a wider compatibility.

But don't worry... if you feel unsafe you can install these files by yourself (just put there because there are people who can't do these by themselves).

1. Go to chrome://settings/help and find out which is your Chrome's version
2. Go to https://chromedriver.chromium.org/downloads and find the latest version which supports your Chrome's version.
3. Download the one for your O.S.
4. Pick the executable and put in `drivers`' folder.
5. Replace and rename the executable with one that was already inside `driver`'s folder depending on your O.S. (You can get rid of the ones that were already inside the folder)


### Setup

1. Install Google Chrome (Don't change the instalation's path) -> if you guys start complaining about this specific step I'll make some updates to have wider options 
2. Install Python 3.6+ (Don't forget to add in system variable `PATH`)
3. Open terminal, change directory to Instagram-Giveaways-Winner's folder and type: `pip install -r requirements.txt`
4. Edit config.ini (See next category)
5. In the same terminal type: `py script.py`

Warning: Avoid resizing or touching the Browser oppened. You can minimize if you want or if you want to get rid of it just change `Window` to `False` in `config.ini`

These commands can change depending on your configuration. Such as python/py/python3... or pip/pip3...

If you need help add me on discord or join the server and ask me (links in my profile's bio) :)

