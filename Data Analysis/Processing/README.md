# Processing Data

---

In this section we gather data from MongoDB that we then sanitize and format into a Pandas DataFame to be used for training models.

### Aggregating Data From MongoDB

The goal of this portion of the script is to generate a Pandas DataFrame populated for every minute between a specified start and end datetime for all features with either a value or a `None` object.

The process for gathering data from MongoDB is straightforward enough with PyMongo, initially our intentions were to query all features at once but this led to extremely long running times. Currently we call `find({'user': user})` on each feature's collection to gather all data relevant to that user in that collection. From there we populate a list of tuples of the form `(datetime, value)` which is then sent off to a helper function that populates all missing minutes from a specified start datetime to end datetime with `None`.

Then all of the feature lists are combined together to form a Pandas DataFrame for that specific user.
```py
return pd.DataFrame({
    'DATE': date_df, 
    'USER': user_df,
    'SLEEP': sleep_df,
    'HEART': heart_df,
    'STEP': step_df,
    'WEIGHT': weight_df,
    'HEIGHT': height_df
    })
```


### Handling Missing Data

The next step is to handle when we come across missing data (`None` objects) in our DataFrame. We handle missing data according to feature as described below:

##### Heartrate
* Detect chunks of missing data
* Measure the size of each chunk
* Handle according to size:
	- Less than 30 minutes, fill all values with average bpm of immediate surrounding measurements.
	- Greater than 30 minutes, discard all measurements.

##### Sleep
* Detect chunks of missing data
* Measure size
* Handle accordingly:
	- If chunk is between 21:00-9:00 and is less 30 mins, fill in with 'awake'<sup>[*](#footnote1)</sup>.
	- If chunk is greater 30 minutes, discard all measurements.

##### Steps
* Fill all missing values in with 0.

##### Body
* Any missing data can easily be filled with surrounding data, body measurements are relatively static.


### Extracting New Features

This last step follows as it's own script, `feature_extraction.py`, which we use to create new columns of data that our models can use to improve upon their accuracy.

##### Nighttime
This additional metric is a binary indicator of whether the current datetime falls between 21:00-9:00. The motivation behind this is to indicate to the model that typical sleep behaviour occurs during the nighttime.

---

<a name="footnote1"><sup><sub>*</sub></sup></a> <sup><sub>The logic behind this is as follows:
1\. If sleep data is *not* present ⇒ either the user is not wearing the device or the user is awake.
2\. If heartrate data is present ⇒ the user is wearing the device.
3\. If the user is weraing the device ⇒ the device will detect and record sleep accordingly.
4\. If heartrate data is present ⇒ the device will detect and record sleep.
∴ If heartrate data is present **and** sleep data is *not* present ⇒ the user is awake.
</sub></sup>