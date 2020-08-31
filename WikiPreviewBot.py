import praw
import wikipedia
import os
import time

#################Bot Information#########################
userAgent = 'Wikipedia Preview Bot (by /u/RealIamMellow)'
clientID = ''
clientSC = ''
username = ''
password = ''
#########################################################


reddit = praw.Reddit(user_agent = userAgent,
                     client_id = clientID,
                     client_secret = clientSC,
                     username = username,
                     password = password)

subreddit = reddit.subreddit('todayilearned')

print('---------------------------')

if not os.path.isfile('posts_replied_to.txt'):
    posts_replied_to = []
else:
    with open('posts_replied_to.txt', 'r') as file:
        posts_replied_to = file.read()
        posts_replied_to = posts_replied_to.split('\n')
        posts_replied_to = list(filter(None, posts_replied_to))

while True:
    for post in subreddit.new(limit=5):
        if post.id not in posts_replied_to:
            if (post.selftext == '' and 'wikipedia' in post.url):
                url = post.url
                print('Bot replying to: ', post.title)
            elif 'wikipedia' in post.selftext.lower():
                text = post.selftext
                print('Bot replying to: ', post.title)
                url = text[2: text.index(']')]
            else:
                continue
            split_info = url.split('/')
            print('Formatted URL: ', url)

            subject = split_info[-1]
            print('Subject: ', subject)

            try:
                summary = wikipedia.summary(subject, sentences=3)
                reply_text = 'Here is the wikipedia summary of ' + subject + ':' + '\n' \
                             + '>' + summary + '\n' + '\n' \
                             + '^beep ^beep ^boop, ^I ^am ^a ^bot, ^please ^message' \
                               ' ^me ^with ^any ^concerns ^and ^I ^will ^try ^to ^fix ^them!'
                post.reply(reply_text)
                print('Replying with summary!')
                posts_replied_to.append(post.id)
            except Exception as e:
                print(e.message)
            print('---------------------------')

    num_replied_to = 0
    with open('posts_replied_to.txt', 'w') as file:
        for post_id in posts_replied_to:
            file.write(post_id + '\n')
            num_replied_to += 1

    print('I have replied to ', num_replied_to, ' posts!')
    print('---------------------------')

    time.sleep(600)