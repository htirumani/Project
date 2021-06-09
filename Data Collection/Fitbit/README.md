# Fitbit

Utilizes [Fitbit unofficial API](https://github.com/orcasgit/python-fitbit) to fetch user data and format JSON docs for every minute, adapted from an [article](https://towardsdatascience.com/using-the-fitbit-web-api-with-python-f29f119621ea) by Michael Galarnyk. Then it pushes these docs to the relevant collections in the MongoDB Atlas database. The script currently calls and pushes minute data for sleep and heart rate data.

## Using Script

---

Calling the script requires two command line arguments with an optional third argument. The first argument is the date of the data to be collected, this is in YYYY-MM-DD format. The second argument is the userID which is written in all docs pushed to the MongoDB database. The last (optional) argument chooses whether or not the API calls are saved in an external 'output' folder.

### Example Calls
* `python3 script.py 2021-06-01 1`
* `python3 script.py 2021-06-01 1 y`

## Example JSON Doc Formating

---

Some quick notes

* `"user"` field correlates to an integer.
* `"device"` field correlates to an integer, for this project a `0` represents the Fitbit device and a `1` represents the Samsung device.
* `"date"` is in YYYY-MM-DD format.
* For the Sleep docs `"stage"` can be either `1`,`2`, or `3` which directly correlate to "asleep", "awake", and "really awake".

### Sleep
```json
{
	"user" : 1,
 	"device" : 0,
 	"date" : "2021-06-01",
 	"time" : "00:00",
 	"stage" : 1
}
```

### Heartrate
```json
{
	"user" : 1,
 	"device" : 0,
 	"date" : "2021-06-01",
 	"time" : "00:00",
 	"value" : 60
}
```

## MongoDB

---

Connects to the MongoDB database specified in the `ATLAS` field, then the `push_docs(docs, base, feature)` method inserts `docs` to the collection `feature` in the database `base`.