import pandas as pd

# IMPORTING RAW DATA:
okt2021 = pd.read_csv('workfiles/202110-divvy-tripdata.csv', index_col=0)
nov2021 = pd.read_csv('workfiles/202111-divvy-tripdata.csv', index_col=0)
dec2021 = pd.read_csv('workfiles/202112-divvy-tripdata.csv', index_col=0)
jan2022 = pd.read_csv('workfiles/202201-divvy-tripdata.csv', index_col=0)
feb2022 = pd.read_csv('workfiles/202202-divvy-tripdata.csv', index_col=0)
mar2022 = pd.read_csv('workfiles/202203-divvy-tripdata.csv', index_col=0)
apr2022 = pd.read_csv('workfiles/202204-divvy-tripdata.csv', index_col=0)
may2022 = pd.read_csv('workfiles/202205-divvy-tripdata.csv', index_col=0)
jun2022 = pd.read_csv('workfiles/202206-divvy-tripdata.csv', index_col=0)
jul2022 = pd.read_csv('workfiles/202207-divvy-tripdata.csv', index_col=0)
aug2022 = pd.read_csv('workfiles/202208-divvy-tripdata.csv', index_col=0)
sep2022 = pd.read_csv('workfiles/202209-divvy-tripdata.csv', index_col=0)

# DATA CLEANING:
# Merging all datasets into one:
dataframe = [okt2021, nov2021, dec2021, jan2022, feb2022,
             mar2022, apr2022, may2022, jun2022, jul2022, aug2022, sep2022]
df_complete = pd.concat(dataframe)

# Checking number and columns and its names in datasets:
for _ in dataframe:
    print(_.shape)
    print(_.columns)
# Raw datasets contain 12 same columns. Tables are consistent.
df_complete.shape
df_complete.columns
# Merged raw dataset has 5828235 rows and 12 columns.

# Pushing "ride_id" index as first column
# df_complete['ride_id'] = df_complete.index
df_complete = df_complete.reset_index(level=0)

# Checking data types:
df_complete.dtypes
# Columns "started_at" and "ended_at" should be in datetype format:
df_complete['started_at'] = pd.to_datetime(df_complete['started_at'])
# Checking first cell:
df_complete['started_at'][0]

df_complete['ended_at'] = pd.to_datetime(df_complete['ended_at'])
# Checking first cell:
df_complete['ended_at'][0]


# Checking for "typos" or "misspellings" in the whole dataset:
df_complete.rideable_type.unique()
# There are 3 types of bikes: "electric bike", "docked bike" and "classic bike". No errors.
df_complete.member_casual.unique()
# There are 2 types of users: "casual", "member". No errors.
df_complete.start_station_id.value_counts()
df_complete.start_station_name.value_counts()
df_complete.end_station_id.value_counts()
df_complete.end_station_name.value_counts()
# There are many names and id's that occur just once. 
# They could be error inputs or new/deleted stations. To further investigation


# Checking length of the id's
df_complete['ride_id'].map(len).unique()
# All id's have 16 characters

# Checking for duplicate inputs based on ride id:
df_complete.duplicated(subset=['ride_id']).value_counts()
# There are no duplicates of ride ids


# Checking for empty cells, null values:
for column in df_complete.columns:
    print(df_complete[column].isnull().value_counts())

# 895032 rows with empty cells or null values in start station description columns
# start_station_id inconsistent length and format

# 958227 rows with empty cells or null values in start station description columns
# end_station_id inconsistent length and format

# 821264 rows where both start and end station is not given

# 5844 rows with empty cells or null values in end coordinates columns


# Deleting rows with missing data:
no_nan_data = df_complete.dropna()
no_nan_data.shape
# The dataset without NAN values contains 4474141 rows with data.
# In relation to the whole dataset over 76% of data is complete.

# Searching for the unwanted data - test data.
# Context: TEST found in one of the start stations id's "Hubbard Bike-checking (LBS-WH-TEST)"
no_nan_data['start_station_id'].str.contains('TEST').value_counts()
# 1207 test rides found in start station id's. All should not be considered.

no_nan_data['start_station_name'].str.contains('TEST').value_counts()
# No test rides found in start station names.
# Deleting test rides:
no_test_start_data = no_nan_data[no_nan_data['start_station_id'].str.contains(
    'TEST') != True]


no_test_start_data['end_station_id'].str.contains('TEST').value_counts()
# 254 test rides found in rest end station id's. All should not be considered.

no_test_start_data['end_station_name'].str.contains('TEST').value_counts()
# No test rides found in end station names.

# Deleting test rides:
no_nan_no_test_data = no_test_start_data[no_test_start_data['end_station_id'].str.contains(
    'TEST') != True]
# 4472680 rows left

# Dataframe with no test rides and no NaN values:
no_nan_no_test_data.head(5)

# Creating copy of the dataframe to add new column:
df_ridetime = no_nan_no_test_data.copy(deep=True)

# Adding new column with ride time:
df_ridetime.insert(
    loc=4, column='ride_time[s]', value=df_ridetime['ended_at'] - df_ridetime['started_at'])
# Changing ride time to seconds:
df_ridetime['ride_time[s]'] = df_ridetime['ride_time[s]'].astype(
    'timedelta64[s]')
df_ridetime.head(5)


# Sorting data by ride time:
df_rt_sorted = df_ridetime.sort_values(by='ride_time[s]')
df_rt_sorted.head(5)


# Checking for negative ride time values:
df_rt_sorted[df_rt_sorted['ride_time[s]'] < 0]
df_rt_sorted[df_rt_sorted['started_at'] > df_rt_sorted['ended_at']]

# 71 wrong inputs with negative ride times. Deleting:
df_rt_no_neg = df_rt_sorted[df_rt_sorted['ride_time[s]'] > 0]
df_rt_no_neg.head(5)


# Checking for the low ride time values, assuming these are incorrect or irrelevant records (below 60s):
df_rt_no_neg[df_rt_no_neg['ride_time[s]'] < 60]
# There are 73439 inputs with ride time below 60s. Deleting:
df_rt_cleaned = df_rt_sorted[df_rt_sorted['ride_time[s]'] >= 60]
df_rt_cleaned.head(5)


# Data sorted by date:
df_sort_date = df_rt_cleaned.sort_values(by="started_at")
df_sort_date.head(5)


columns_to_be_dropped = ['ride_id', 'start_station_id',
                         'end_station_id', 'start_lat', 'start_lng', 'end_lat', 'end_lng']
df_drop_columns = df_sort_date.drop(columns=columns_to_be_dropped)
df_drop_columns.head(5)


## Adding columns with the day of the week that each ride started
# 0 - Monday, 6 - Sunday:
df_drop_columns.insert(loc=4, column='weekday', value=df_ridetime['started_at'].dt.weekday)

all_rides = df_drop_columns.copy(deep=True)
all_rides.head(5)

# weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# for _ in range(7):
#     all_rides.loc[all_rides.weekday == _, 'weekday'] = weekdays[_]

new_columns = {'rideable_type': 'BikeType',
               'started_at': 'RideStart',
               'ended_at': 'RideEnd',
               'ride_time[s]': 'RideTime[s]',
               'weekday': 'Weekday',
               'start_station_name': 'StartStation',
               'end_station_name': 'EndStation',
               'member_casual': 'UserType'
              }

all_rides = all_rides.rename(columns=new_columns)

# EXPORTING CLEAN DATA:
all_rides.to_csv('cleaned_data/cyclistic_202110-202209_cleaned.csv', index=False)


all_rides_100 = all_rides[:100].copy()
all_rides_100.to_csv('cleaned_data/cyclistic_202110-202209_cleaned.csv', index=False)