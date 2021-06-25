# Project

## MongoDB Data Formats
Specifications for document formats for wearabledb. Data should be reported minute by minute. All "datetime" fields should be populated in the user's local time. Scripts populating the database can simply pass datetime objects in the python dictionaries passed to insert() commands, pymongo will infer the proper format.

SLEEP
```
{"user": 0, "device": 0, "datetime": 2021-05-31T12:00:00.000+00:00, "stage" : 1}
```

HEART
```
{"user": 1, "device": 0, "datetime": 2021-05-31T12:00:00.000+00:00, "heart_rate": 60}
```

STEP
```
{"user": 1, "device": 0, "datetime": 2021-05-31T12:00:00.000+00:00, "steps": 20}
```
Steps field is populated with number of steps taken in the minute alone.

BODY
```
{"user": 1, "device": 0, "datetime": 2021-05-31T12:00:00.000+00:00, "height" : 72, "weight" : 180}
```

## Data Encodings
device
```
{
    "0": "fitbit",
    "1": "samsung"
}
```

sleep
```
{
	"0": "awake",
	"1": "asleep"
}
```

user
```
{
    "0": "Neelam",
    "1": "Bronson",
    "2": "Max",
    "3": "Harshitha"
}
```

samsung sleep stage
```
{
    "awake": 40001,
    "light": 40002,
    "deep": 40003,
    "rem": 40004
}
```