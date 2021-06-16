# MongoDB Data Format Templates

All "datetime" fields should be populated in the user's local time in Unix timestamp format (milliseconds since Jan 1, 1970). Scripts populating the database can simply pass datetime objects in the python dictionaries passed to insert() commands, pymongo will infer the proper format.