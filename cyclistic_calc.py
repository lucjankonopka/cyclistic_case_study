import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

cleaned_data = pd.read_csv(
    'cleaned_data/cyclistic_202110-202209_cleaned.csv', index_col=0)

cleaned_data.head()

# Color palette for weekdays plots - from dark to bright:
colors_w = ('#3f94a4', '#3aa7ab', '#45baac',
          '#60cba6', '#84db9c', '#aee991', '#dcf587')
def_color = colors_w[0]

# Fonts:
font1 = {'color': 'black', 'fontweight': 'bold', 'size': 14}
font2 = {'color': 'black', 'fontweight': 'bold', 'size': 10}


# Overall bike type usage:
bike_type_usage_overall = cleaned_data.BikeType.value_counts()
btus_y = np.array([bike_type_usage_overall]).flatten()
btus_labels = ['classic_bike',
               'electric_bike',
               'docked_bike']

plt.pie(btus_y, labels=btus_labels,
        startangle=90, autopct='%.1f%%', colors=(colors_w[0], 
        colors_w[3], colors_w[5]))
plt.title("Bike types usage", fontdict=font1, pad=20)
plt.axis('equal')
plt.tight_layout()


# Bike type used by user type:
bike_usage_by_user = cleaned_data[['BikeType', 'UserType']].copy()
bubu = bike_usage_by_user.value_counts()

fig, ax = plt.subplots()
bubu.unstack().plot.bar(ax=ax, rot=0, color=(colors_w[0], colors_w[5]), zorder=3, edgecolor='w')
plt.title("Bike type used by user type", fontdict=font1, pad=20)
plt.grid(axis='y', zorder=0)
plt.tight_layout()
plt.ylim(0, 2e6)


# Overall usage by user:
overall_usage_by_user = cleaned_data['UserType'].copy()
oubu = overall_usage_by_user.value_counts()

oubu_labels = ['member',
               'casual']
plt.pie(oubu, labels=oubu_labels,
        startangle=90, autopct='%.1f%%', colors=(colors_w[0], colors_w[5]))
plt.title("User types", fontdict=font1, pad=10)
plt.axis('equal')
plt.tight_layout()


# Bike type used in single days:
days = ['Monday', 'Tuesday', 'Wednesday',
        'Thursday', 'Friday', 'Saturday', 'Sunday']

bike_usage_by_weekday = cleaned_data[['BikeType', 'Weekday']].copy()

bubw = bike_usage_by_weekday.value_counts()

fig, ax = plt.subplots()
bubw.unstack().plot.bar(ax=ax, rot=0, width=0.7 ,color=colors_w, zorder=3, edgecolor='w')
ax.grid(axis='y', zorder=0)
plt.title("Bike type used in sigle days", fontdict=font1, pad=20)
plt.xlabel("Bike type", fontdict=font2)
plt.ylim(0, 5e5)
plt.legend(days, loc='upper right', prop={'size': 9}, facecolor='white')
plt.tight_layout()


# Most usage by days
usage_by_weekday = cleaned_data['Weekday'].copy()
ubw = usage_by_weekday.value_counts().sort_index()
plt.bar(days, height=ubw, width=0.5, color=def_color, zorder=3, edgecolor='w')
plt.grid(axis='y', zorder=0)
plt.xlabel("Weekday", fontdict=font2)
plt.title("Usage in single days", fontdict=font1, pad=20)
plt.ylim(0, 8e5)
plt.tight_layout()


# Most usage by days & user type
usage_by_weekday_user = cleaned_data[['Weekday', 'UserType']].copy()
ubwu = usage_by_weekday_user.value_counts().sort_index()

ubwu_plot = ubwu.unstack().plot.bar(
    rot=0, color=(colors_w[0], colors_w[5]), stacked=True, zorder=3, edgecolor='w')
plt.grid(axis='y', zorder=0)
plt.xlabel("Weekday", fontdict=font2)
index = range(len(days))
plt.title("Usage in single days by single user type", fontdict=font1, pad=20)
plt.xticks(index, days)
plt.ylim(0, 8e5)
plt.tight_layout()
plt.legend(loc='upper left', prop={'size': 9}, facecolor='white')


# Most usage in single days by casual users
usage_days_casual = usage_by_weekday_user[usage_by_weekday_user['UserType'] == 'casual']
uc = usage_days_casual.value_counts().sort_index()
plt.bar(days, height=uc, width=0.5, color=def_color, zorder=3, edgecolor='w')
plt.grid(axis='y', zorder=0)
plt.ylim(0, 5e5)
plt.xlabel("Weekday", fontdict=font2)
plt.title("Usage in single days by casual users", fontdict=font1, pad=20)
plt.xticks(index, days)
plt.tight_layout()

# Most usage in single days by members
usage_days_member = usage_by_weekday_user[usage_by_weekday_user['UserType'] == 'member']
um = usage_days_member.value_counts().sort_index()
plt.bar(days, height=um, width=0.5, color=def_color, zorder=3, edgecolor='w')
plt.grid(axis='y', zorder=0)
plt.ylim(0, 5e5)
plt.xlabel("Weekday", fontdict=font2)
plt.title("Usage in single days by members", fontdict=font1, pad=20)
plt.xticks(index, days)
plt.tight_layout()


# Bike type used in single months:
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
colors_m = ('#3f94a4', '#35a1ac', '#27b9b5', '#2cc6b6', '#3bd2b4', '#4fddb0', '#69e3a8',
            '#82e7a0', '#99eb98', '#afef91', '#c6f28b', '#dcf587')


bike_usage_by_month = cleaned_data[['BikeType', 'RideStart']].copy()
bike_usage_by_month['Month'] = pd.DatetimeIndex(bike_usage_by_month['RideStart']).month
bubm = bike_usage_by_month[['BikeType', 'Month']].value_counts().sort_index()

fig, ax = plt.subplots()
bubm.unstack().plot.bar(ax=ax, rot=0, width=0.8, color=colors_m, zorder=3, edgecolor='w')
ax.grid(axis='y', zorder=0)
plt.title("Bike type used in sigle months", fontdict=font1, pad=20)
plt.xlabel("Bike type", fontdict=font2)
plt.ylim(0, 7e5)
plt.legend(months, loc='upper right', prop={'size': 9}, facecolor='white')
plt.tight_layout()


# Most usage by months

usage_by_month = cleaned_data.filter(['RideStart'], axis=1)
usage_by_month['Month'] = pd.DatetimeIndex(usage_by_month['RideStart']).month
ubm = usage_by_month['Month'].value_counts().sort_index()
plt.bar(months, height=ubm, width=0.5, color=def_color, zorder=3, edgecolor='w')
plt.grid(axis='y', zorder=0)
plt.xlabel("Month", fontdict=font2)
plt.title("Usage in single months", fontdict=font1, pad=20)
plt.ylim(0, 7e5)
plt.tight_layout()

# Horizontal
plt.barh(months, width=ubm, height=0.5, color=def_color)
plt.tight_layout()


# Most usage by months & user type
usage_by_month_user = cleaned_data.filter(['RideStart', 'UserType'], axis=1)
usage_by_month_user.insert(loc=1, column='Month', value=pd.DatetimeIndex(
    usage_by_month['RideStart']).month)
usage_by_month_user_clean = usage_by_month_user.copy(deep=True)
usage_by_month_user_clean = usage_by_month_user_clean.drop(columns='RideStart')

ubmuc = usage_by_month_user_clean.value_counts().sort_index()
ubwu_plot = ubmuc.unstack().plot.bar(
    rot=0, color=(colors_w[0], colors_w[5]), stacked=True, zorder=3, edgecolor='w')
plt.grid(axis='y', zorder=0)
plt.ylim(0, 7e5)
plt.xlabel("Month", fontdict=font2)
plt.title("Usage in single months by single user type", fontdict=font1, pad=20)
index = range(len(months))
plt.xticks(index, months)
plt.tight_layout()
plt.legend(loc='upper right', prop={'size': 9}, facecolor='white')


# Most usage in single months by casual users
usage_casual = usage_by_month_user_clean[usage_by_month_user_clean['UserType'] == 'casual']
uc = usage_casual.value_counts().sort_index()
plt.bar(months, height=uc, width=0.5, color=def_color, zorder=3, edgecolor='w')
plt.grid(axis='y', zorder=0)
plt.ylim(0, 3.5e5)
plt.xlabel("Month", fontdict=font2)
plt.title("Usage in single months by casual users", fontdict=font1, pad=20)
plt.xticks(index, months)
plt.tight_layout()


# Most usage in single months by members
usage_member = usage_by_month_user_clean[usage_by_month_user_clean['UserType'] == 'member']
um = usage_member.value_counts().sort_index()
plt.bar(months, height=um, width=0.5, color=def_color, zorder=3, edgecolor='w')
plt.grid(axis='y', zorder=0)
plt.ylim(0, 3.5e5)
plt.xlabel("Month", fontdict=font2)
plt.title("Usage in single months by members", fontdict=font1, pad=20)
plt.xticks(index, months)
plt.tight_layout()


# Ride time
ride_time = cleaned_data['RideTime[s]'].copy()
rt = ride_time.value_counts()
data_rt = {'1min-5min': 0, '5min-15min': 0, '15min-30min': 0, '30min-60min': 0, 'above 1 hour': 0}
ranges = ['1min-5min', '5min-15min', '15min-30min', '30min-60min', 'above 1 hour']
for el in range(len(rt)):
    if rt.index[el] <= 300:
        data_rt['1min-5min'] += rt.values[el]
    elif rt.index[el] > 300 and rt.index[el] <= 900:
        data_rt['5min-15min'] += rt.values[el]
    elif rt.index[el] > 900 and rt.index[el] <= 1800:
        data_rt['15min-30min'] += rt.values[el]
    elif rt.index[el] > 1800 and rt.index[el] <= 3600:
        data_rt['30min-60min'] += rt.values[el]
    else:
        data_rt['above 1 hour'] += rt.values[el]

ridetimes_grouped = pd.Series(data=data_rt, index=ranges)

plt.bar(ranges, height=ridetimes_grouped, width=0.5, color=def_color, zorder=3, edgecolor='w')
plt.grid(axis='y', zorder=0)
plt.xlabel("Ride time ranges", fontdict=font2)
plt.title("Ride times overall", fontdict=font1, pad=20)
plt.ylim(0, 2.25e6)
plt.tight_layout()

ride_time.mean()
ride_time.median()


# Ride time by users
ride_time_by_users = cleaned_data.filter(['RideTime[s]', 'UserType'], axis=1)

# casual users
ride_time_casual = ride_time_by_users[usage_by_month_user_clean['UserType'] == 'casual']
ride_c = ride_time_casual['RideTime[s]'].copy()
rtc = ride_c.value_counts()
data_rtc = {'1min-5min': 0, '5min-15min': 0, '15min-30min': 0, '30min-60min': 0, 'above 1 hour': 0}
for el in range(len(rtc)):
    if rtc.index[el] <= 300:
        data_rtc['1min-5min'] += rtc.values[el]
    elif rtc.index[el] > 300 and rtc.index[el] <= 900:
        data_rtc['5min-15min'] += rtc.values[el]
    elif rtc.index[el] > 900 and rtc.index[el] <= 1800:
        data_rtc['15min-30min'] += rtc.values[el]
    elif rtc.index[el] > 1800 and rtc.index[el] <= 3600:
        data_rtc['30min-60min'] += rtc.values[el]
    else:
        data_rtc['above 1 hour'] += rtc.values[el]
ridetimes_casual_grouped = pd.Series(data=data_rtc, index=ranges)

plt.bar(ranges, height=ridetimes_casual_grouped, width=0.5, color=def_color, zorder=3, edgecolor='w')
plt.grid(axis='y', zorder=0)
plt.xlabel("Ride time ranges", fontdict=font2)
plt.title("Ride times overall by casual users", fontdict=font1, pad=20)
plt.ylim(0, 1.5e6)
plt.tight_layout()


ride_c.mean()
ride_c.median()



# members
ride_time_member = ride_time_by_users[usage_by_month_user_clean['UserType'] == 'member']
ride_m = ride_time_member['RideTime[s]'].copy()
rtm = ride_m.value_counts()
data_rtm = {'1min-5min': 0, '5min-15min': 0, '15min-30min': 0, '30min-60min': 0, 'above 1 hour': 0}
for el in range(len(rtm)):
    if rtm.index[el] <= 300:
        data_rtm['1min-5min'] += rtm.values[el]
    elif rtm.index[el] > 300 and rtm.index[el] <= 900:
        data_rtm['5min-15min'] += rtm.values[el]
    elif rtm.index[el] > 900 and rtm.index[el] <= 1800:
        data_rtm['15min-30min'] += rtm.values[el]
    elif rtm.index[el] > 1800 and rtm.index[el] <= 3600:
        data_rtm['30min-60min'] += rtm.values[el]
    else:
        data_rtm['above 1 hour'] += rtm.values[el]
ridetimes_member_grouped = pd.Series(data=data_rtm, index=ranges)

plt.bar(ranges, height=ridetimes_member_grouped, width=0.5, color=def_color, zorder=3, edgecolor='w')
plt.grid(axis='y', zorder=0)
plt.xlabel("Ride time ranges", fontdict=font2)
plt.title("Ride times overall by members", fontdict=font1, pad=20)
plt.ylim(0, 1.5e6)
plt.tight_layout()


ride_m.mean()
ride_m.median()


# Most popular start stations
most_start_stations = cleaned_data['StartStation'].copy()
mss = most_start_stations.value_counts().head(10)

plt.barh(mss.index, width=mss, height=0.5, color=def_color, zorder=3, edgecolor='w')
plt.grid(axis='x', zorder=0)
plt.yticks(rotation=25, ha='right')
plt.ylabel("Start station names", fontdict=font2)
plt.title("Most used start stations", fontdict=font1, pad=20)
plt.xlim(0, 8e4)



# Heatmap - Most usage in single months and days
color_heatmap = list(colors_m[::-1])

bike_usage_by_month = cleaned_data[['RideStart', 'Weekday']].copy()
bike_usage_by_month['Month'] = pd.DatetimeIndex(bike_usage_by_month['RideStart']).month
bubm = bike_usage_by_month.drop(columns='RideStart')

bubm_count = bike_usage_by_month[['Month', 'Weekday']].value_counts().sort_index()
bubm_count_table = bubm_count.reset_index()
bubm_count_table.columns = ['Month', 'Weekday', 'Count']

temp_df = bubm_count_table[['Month', 'Weekday', 'Count']]

heatmap_pt = pd.pivot_table(temp_df, values='Count', index=['Weekday'], columns='Month')

fig, ax = plt.subplots(figsize=(16,8))
sns.set()
sns.heatmap(heatmap_pt, cmap=color_heatmap, linewidths = 0.3)
plt.title("Most usage in single months and days", fontdict=font1, pad=20)
plt.xlabel("Month", fontdict=font2)
plt.ylabel("Weekday", fontdict=font2)
n_days = np.arange(len(days))+0.5
plt.yticks(n_days, days, rotation=0, ha='right')
n_months = np.arange(len(months))+0.5
plt.xticks(n_months, months, ha='center')

