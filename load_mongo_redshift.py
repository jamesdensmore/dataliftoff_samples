# Sample code for the "How to Load Data from MongoDB into Amazon Redshift" on the Data Liftoff Blog
# http://www.dataliftoff.com/2019/06/20/how-to-load-data-from-mongodb-into-amazon-redshift/

from pymongo import MongoClient
import csv
import boto3
import datetime
from datetime import timedelta

# Extracting Data from MongoDB
def extract_mongo_data():
	
	# create a MongoClient instance and connect to your MongoDB host
	# NOTE: store your credentials in a secure config file!
	mongo_client = MongoClient("my_host",
		 username='my_username',
		 password='my_password',
		 authSource='my_auth_db')

	# now connect to the database where your collection resides
	mongo_db = mongo_client['my_database']

	# finally, choose the collection we want to query documents from
	mongo_collection = mongo_db['my_collection']

	start_date = datetime.date.today() + timedelta(days = -1)
	end_date = start_date + timedelta(days =1 )
	mongo_query = { "$and":[{"date" : { "$gte": start_date }}, {"date" : { "$lt": end_date }}] }

	# get a cursor with the result set. Bring back 3000 documents at a time
	result_docs = mongo_collection.find(mongo_query, batch_size=3000)

	# create a blank list to store our results
	all_events = []

	# iterate through the cursor
	for doc in event_docs:
		# Include default values
		event_id = str(doc.get("event_id", -1))
		event_timestamp = doc.get("date", None)
		event_name = doc.get("event_name", None)

		# add all the event properties into a list
		current_event = []
		current_event.append(event_id)
		current_event.append(event_timestamp)
		current_event.append(event_name)

		# add the event to our final list of events   
		all_events.append(current_event)

		# write all the events to a local csv file
		with open('export_file.csv', 'w') as fp:
			csvw = csv.writer(fp, delimiter='|')
			csvw.writerows(all_events)

		fp.close()

	# NOTE: Store all your credentials in a secure config file!
	access_key = "my_access_key"
	secret_key = "my_secret_key"
	export_file = "export_file.csv"
	s3_bucket_name = "s3_bucket_name"
	s3_file = "event_export.csv"

	s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)

	# upload the local CSV file to your S3 bucket
	s3.upload_file(export_file, s3_bucket_name, s3_file)

	# clean up
	mongo_client.close()



