from os import environ
import gspread
import tweepy
import secrets
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

consumer_key = environ['consumer_key']
consumer_secret = environ['consumer_secret']
access_token = environ['access_token']
access_token_secret = environ['access_token_secret']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

gc = gspread.service_account(filename='./sheets.json')

sh = gc.open_by_key('1TzIUmBSEVeLQjCkTnZ4cr2Y8oWQPSGgYFEUQrGGcSGY')
worksheet = sh.sheet1

INTERVAL = int(environ['INTERVAL'])
DEBUG = environ['DEBUG'] == '1'

def main():
	while True:
		tweet_records = worksheet.get_all_records()
		current_time = datetime.utcnow() + timedelta(hours=5, minutes=30)
		logger.info(f'{len(tweet_records)} tweets found at {current_time.time()}')

		for idx, tweet in enumerate(tweet_records, start=2):
			msg = tweet['message']
			time_str = tweet['time']
			done = tweet['done']
			date_time_obj = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
			
			if not done:
				now_time_ist = datetime.utcnow() + timedelta(hours=5, minutes=30)
				if date_time_obj < now_time_ist:
					logger.info('this should be tweeted')
					try:
						api.update_status(msg)
						worksheet.update_cell(idx, 3, 1)
					except Exception as e:
						logger.warning(f'error during tweet! {e}')

		time.sleep(INTERVAL)

if __name__ == '__main__':
	main()