import re
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from textblob import TextBlob
import matplotlib.pyplot as plt
import CountryFinder as cf
import Plot





class TwitterClient(object):
	'''
	Generic Twitter Class for sentiment analysis.
	'''

	def __init__(self):
		'''
		Class constructor or initialization method.
		'''
		# keys and tokens from the Twitter Dev Console
		consumer_key = 'XXXXXXX'
		consumer_secret = 'XXXXXXX'
		access_token = 'XXXXXXXXXXXXXX'
		access_token_secret = 'XXXXXXX'

		# attempt authentication
		try:
			# create OAuthHandler object
			self.auth = OAuthHandler(consumer_key, consumer_secret)
			# set access token and secret
			self.auth.set_access_token(access_token, access_token_secret)
			# create tweepy API object to fetch tweets
			self.api = tweepy.API(self.auth)
		except:
			print("Error: Authentication Failed")

	def clean_tweet(self, tweet):
		'''
		Utility function to clean tweet text by removing links, special characters
		using simple regex statements.
		'''
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

	def get_tweet_sentiment(self, tweet):
		'''
		Utility function to classify sentiment of passed tweet
		using textblob's sentiment method
		'''
		# create TextBlob object of passed tweet text
		analysis = TextBlob(self.clean_tweet(tweet))
		# set sentiment
		if analysis.sentiment.polarity > 0:
			return 'positive'
		elif analysis.sentiment.polarity == 0:
			return 'neutral'
		else:
			return 'negative'

	def get_tweets(self, query, count=10):
		'''
		Main function to fetch tweets and parse them.
		'''
		# empty list to store parsed tweets
		tweets = []
		try:
			# call twitter api to fetch tweets
			fetched_tweets = self.api.search(q=query, count=count)

			# parsing tweets one by one
			for tweet in fetched_tweets:
				# empty dictionary to store required params of a tweet
				parsed_tweet = {}

				# saving text of tweet
				parsed_tweet['text'] = tweet.text
				# saving sentiment of tweet
				parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

				parsed_tweet['user'] = tweet.user.followers_count

				# appending parsed tweet to tweets list
				if tweet.retweet_count > 0:
					# if tweet has retweets, ensure that it is appended only once
					if parsed_tweet not in tweets:
						tweets.append(parsed_tweet)
				else:
					tweets.append(parsed_tweet)

			# return parsed tweets
			return tweets

		except tweepy.TweepError as e:
			# print error (if any)
			print("Error : " + str(e))

	def get_categories_ratio(self, category_size=3):
		fetched_tweets = self.api.search(q='the',count=2000)
		tweets = []
		for tweet in fetched_tweets:
			# empty dictionary to store required params of a tweet
			parsed_tweet = {}

			# saving text of tweet
			parsed_tweet['text'] = tweet.text
			# saving sentiment of tweet
			parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

			parsed_tweet['user'] = tweet.user.followers_count

			# appending parsed tweet to tweets list
			if tweet.retweet_count > 0:
				# if tweet has retweets, ensure that it is appended only once
				if parsed_tweet not in tweets:
					tweets.append(parsed_tweet)
			else:
				tweets.append(parsed_tweet)

		lowest_follower = min([x['user'] for x in tweets])
		highest_follower = max([x['user'] for x in tweets])

		step = (highest_follower - lowest_follower) / float(category_size)
		categories = [[] for i in range(category_size)]

		categories_analysis = [[0,0,0] for i in range(category_size)]

		upper_bounds = [lowest_follower + (i + 1) * step for i in range(category_size)]

		for tweet in tweets:
			for i in range(category_size):
				if (tweet['user'] <= upper_bounds[i]):
					categories[i].append(tweet.copy())
					if tweet['sentiment'] == 'positive':
						categories_analysis[i][0]+=1
					elif tweet['sentiment'] == 'negative':
						categories_analysis[i][1] += 1
					else:
						categories_analysis[i][2] += 1
					break
		self.plot_percent(categories, categories_analysis)


	def plot_percent(selfs, categories, categories_analysis):
		total = 0
		for i in range(len(categories)):
			total+=len(categories[i])

		category_percent = [(len(categories[i])/total)*100 for i in range(len(categories))]

		categories_inside_ratio = [[ca[0],ca[1],ca[2]] for ca in categories_analysis]

		labels = ['POSITIVE', 'NEGATIVE', 'NEUTRAL']
		colors = ['green', 'red', 'orange']

		fig, (ax, ax1, ax2, ax3) = plt.subplots(4,sharey=True)

		ax.pie(category_percent , autopct='%1.1f%%',
				shadow=True, startangle=90)
		ax.legend(['Categorey{}'.format(i) for i in range(len(category_percent))], loc="best")
		ax1.pie(categories_inside_ratio[0], colors=colors, autopct='%1.1f%%',pctdistance=2,
				shadow=True, startangle=90)

		ax2.pie(categories_inside_ratio[1], colors=colors, autopct='%1.1f%%',pctdistance=2,
				shadow=True, startangle=90)

		ax3.pie(categories_inside_ratio[2], colors=colors, autopct='%1.1f%%',pctdistance=2,
				shadow=True, startangle=90)

		plt.legend(labels, loc="best")

		ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
		ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
		ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
		ax3.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

		plt.show()


	def get_address_ratio(self,q):
		tweets = []
		try:
			# call twitter api to fetch tweets with keyword q
			fetched_tweets = self.api.search(q=q, count=200)

			# parsing tweets one by one
			for tweet in fetched_tweets:
				# empty dictionary to store required params of a tweet
				parsed_tweet = {}

				# saving text of tweet
				parsed_tweet['text'] = tweet.text
				# saving sentiment of tweet
				parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

				# add address string with keyword map 'user'
				parsed_tweet['user'] = (tweet.user.location, tweet.geo)

				# appending parsed tweet to tweets list
				if tweet.retweet_count > 0:
					# if tweet has retweets, ensure that it is appended only once
					if parsed_tweet not in tweets:
						tweets.append(parsed_tweet)
				else:
					tweets.append(parsed_tweet)
		except tweepy.TweepError as e:
			# print error (if any)
			print("Error : " + str(e))

		categorey_analysis = {}
		i = 1
		for tweet in tweets:
			address = cf.get_Address(tweet['user'][0])
			# print(tweet['user'][0]," : ", address)
			print("\rProcessing tweet: {}/{}".format(i,len(tweets)),end="")
			i+=1
			if (address not in categorey_analysis.keys()):
				categorey_analysis[address] = [0,0,0]
			if (tweet['sentiment']=='positive'):
				categorey_analysis[address][0] += 1
			elif(tweet['sentiment']=='negative'):
				categorey_analysis[address][1] += 1
			else:
				categorey_analysis[address][2] += 1

		Plot.plot_address_ratio(q, categorey_analysis)




