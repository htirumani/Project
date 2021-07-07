"""
Aggregates data from MongoDB into Pandas Dataframes filled in with every
minute between START_DATE and the date of running the script.
"""
import datetime
import numpy as np
import pandas as pd
import pymongo
import os
from dotenv import load_dotenv
from os.path import abspath, dirname, join

# load in env variable
project_root = dirname(dirname(dirname(__file__)))
load_dotenv(project_root)

# define global variables
START_DATE = datetime.datetime(2021, 5, 31, 0, 0)
y,m,d = str(datetime.date.today()).split("-")
END_DATE = datetime.datetime(int(y), int(m), int(d), 0, 0)
DELTA = datetime.timedelta(minutes = 1)
ATLAS = os.environ.get("ATLAS")
USERS = [0, 1, 2, 3]


"""
Various methods to grab data from MongoDB, each a list of tuples 
formatted as (datetime, value) and fill in data for each minute.
"""
def grab_sleep(db, user):
	data = []
	docs = db.sleep.find({'user': user})
	for doc in docs:
		data.append((doc['datetime'], doc['stage']))

	return add_null(data, START_DATE, END_DATE)

def grab_hr(db, user):
	data = []
	docs = db.heart.find({'user': user})
	for doc in docs:
		data.append((doc['datetime'], doc['heart_rate']))

	return add_null(data, START_DATE, END_DATE)

def grab_steps(db, user):
	data = []
	docs = db.step.find({'user': user})
	for doc in docs:
		data.append((doc['datetime'], doc['steps']))

	return add_null(data, START_DATE, END_DATE)

def grab_body(db, user):
	height = []
	weight = []
	docs = db.body.find({'user': user})
	for doc in docs:
		height.append((doc['datetime'], doc['height']))
		weight.append((doc['datetime'], doc['weight']))

	return add_null(height, START_DATE, END_DATE), add_null(weight, START_DATE, END_DATE)

'''
Data is a list of tuples of the form (date, value)
'''
def add_null(data, sdate, edate):
	valid_dates = [i[0] for i in data]
	curr_date = sdate
	col = []
	while curr_date != edate:
		if curr_date in valid_dates:
			col.append([i[1] for i in data if i[0] == curr_date][0])
		else:
			col.append(None)
		curr_date += DELTA
	
	return col


"""
Various methods to then clean up the initial dataframe and
fill in each respective feature's mising data.
"""
def process_heart(df):
	dates = get_dates(df, 'HEART')
	for d in dates:
		stime, etime = d
		delta = etime - stime
		m = delta.seconds / 60
		if m < 30:
			v = mean_surr_vals(df, 'HEART', d)
			fill_values(df, 'HEART', d, v)
	
	df.dropna(subset=['HEART'], inplace=True)

def process_sleep(df):
	# dates = get_dates(df, 'SLEEP')
	# for d in dates:
	# 	stime, etime = d
	# 	delta = etime - stime
	# 	m = delta.seconds//60%60
	# 	if m < 30 and not ((stime.time().hour>9) and (etime.time().hour<21)):
	# 		fill_values(df, 'SLEEP', d, 0)
	df['SLEEP'] = df['SLEEP'].fillna(0)

def process_steps(df):
	df['STEP'] = df['STEP'].fillna(0)

# get list of tuples (stime, etime) of None data in specified feature
def get_dates(df, feature):
	ixs = df[df[feature].isnull()].index.tolist()
	tups = []
	s = ixs[0]
	p = ixs[0]
	ixs.pop(0)

	for i in ixs:
		if i != p+1:
			tups.append((s, p))
			s = i
			p = i
		else:
			p = i
	tups.append((s, p))

	date_tups = [(df.at[s, 'DATE'], df.at[e, 'DATE']) for s, e in tups]
	return date_tups

# fill all values in specified date range in feature
def fill_values(df, feature, dates, value):
	sdate, edate = dates
	cindex = pd.Index(df['DATE']).get_loc(str(sdate))
	eindex = pd.Index(df['DATE']).get_loc(str(edate))
	while cindex != eindex:
		df.at[cindex, feature] = value
		cindex += 1

# calculate mean of surrounding values
def mean_surr_vals(df, feature, dates):
	sdate, edate = dates
	sindex = pd.Index(df['DATE']).get_loc(str(sdate))
	eindex = pd.Index(df['DATE']).get_loc(str(edate))

	if sindex == 0:
		return df.at[eindex + 1, feature]
	if eindex == df.shape[0] - 1:
		return df.at[sindex - 1, feature]
	
	return int(np.mean([df.at[sindex-1,feature], df.at[eindex+1,feature]]).item())

"""
Then finally, construct the clean dataframe for each user
with option to save the 'raw' dataframe.
"""
def main():
	# connect to db & grab collections
	client = pymongo.MongoClient(ATLAS, ssl=True, ssl_cert_reqs='CERT_NONE')
	db = client.wearabledb

	cdate = START_DATE
	date_df = []
	while cdate != END_DATE:
		date_df.append(cdate)
		cdate += DELTA

	DF_ALL = pd.DataFrame(columns=['DATE', 'USER', 'SLEEP', 'HEART', 'STEP', 'WEIGHT', 'HEIGHT'])
	file_dir = dirname(dirname(abspath(__file__)))
	fp = join(file_dir, 'Dataset/')

	# create dataframes for all users
	for user in USERS:
		print("Fetching data for user: ", user)
		sleep_df = grab_sleep(db, user)
		heart_df = grab_hr(db, user)
		steps_df = grab_steps(db, user)
		height_df, weight_df = grab_body(db, user)

		# create initial dataframe with missing data
		rdf_user = pd.DataFrame({'DATE':date_df,
								'USER':user,
								'SLEEP':sleep_df,
								'HEART':heart_df,
								'STEP':steps_df,
								'WEIGHT':weight_df,
								'HEIGHT':height_df,})
		
		# clean up missing data to a 'clean' df
		print("Cleaning data for user: ", user)
		cdf_user = rdf_user.copy()
		process_heart(cdf_user)
		process_sleep(cdf_user)
		process_steps(cdf_user)
		cdf_user.dropna(inplace=True)
		cdf_user['USER'] = cdf_user['USER'].astype(int)
		cdf_user['SLEEP'] = cdf_user['SLEEP'].astype(int)
		cdf_user['HEART'] = cdf_user['HEART'].astype(int)
		cdf_user['STEP'] = cdf_user['STEP'].astype(int)
		cdf_user['WEIGHT'] = cdf_user['WEIGHT'].astype(int)
		cdf_user['HEIGHT'] = cdf_user['HEIGHT'].astype(int)

		# write csv files
		rdf_user.to_csv(join(fp, 'raw/user{}_raw.csv'.format(user)), index = False)
		cdf_user.to_csv(join(fp, 'clean/user{}_clean.csv'.format(user)), index = False)
		
		# append to the ALL dataframe
		DF_ALL = pd.concat([DF_ALL, cdf_user], ignore_index=True)

	# write DF_ALL out to clean
	ixs = np.array(list(range(DF_ALL.shape[0])))
	DF_ALL.set_index(ixs, inplace = True)
	DF_ALL.to_csv(join(fp, 'clean/all.csv'))

if __name__ == '__main__':
	main()