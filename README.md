# Project

## Guide to Handling Missing Data

To be clear, we'll be aggregating all features into a single dataset. When we "discard measurements", we'll need to remove all feature data in that corresponding user-date-minute combo. Any models we intend to employ won't be able to tolerate any missing features.

#### Heartrate
1. Detect chunks of missing data
2. Measure the size of each chunk
3. Handle according to size:
- $\geq$ 30 minutes: fill all values with average bpm of immediately surrounding measurements
- >30 minutes: discard all measurements

#### Sleep
1. Detect chunks of missing data
2. Measure size
3. Handle accordingly:
- If chunk is between 9am-9pm (9:00-21:00), fill in with 'awake'
- else if chunk is <30 mins, fill in with surrounding measurement
- if surrounding measurements conflict i.e. immediately before chunk is 'awake' and immediately after is 'asleep', discard all measurements (that's the consequential time period we're trying to predict, don't want to be making things up in that period)
- if chunk is >30 minutes, discard all measurements

#### Steps
1. ^
2. ^
3. Handle:
- if chunk is >30mins, discard all measurements
- if chunk is <30mins, fill with average of surrounding measurements

#### Body
Any missing data can easily be filled with surrounding data, body measurements are relatively static.

##### Clarifying 'fill with average of surrounding measurements'
Data looks like this: 62 NA NA NA NA NA NA NA 70.
Fill in all NAs with average of 62 and 70.