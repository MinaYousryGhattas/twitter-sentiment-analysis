import sys
from Twitter import TwitterClient
import matplotlib.pyplot as plt
def main():
	api = TwitterClient()
	api.get_address_ratio('barcelona')

# calling function to get tweets
# tweets = api.get_tweets(query = 'bbi', count = 200)

# # picking positive tweets from tweets
# ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
# ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
# labels = ['POSITIVE', 'NEGATIVE', 'NEUTRAL']
# values = [len(ptweets), len(ntweets), len(tweets)-len(ptweets)-len(ntweets)]
# colors = ['green', 'red', 'orange']
#
# fig1, ax1 = plt.subplots()
#
# ax1.pie(values, labels=labels, colors=colors, autopct='%1.1f%%',
# 		shadow=True, startangle=90)
# ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
# plt.show()




if __name__ == '__main__':
	main()