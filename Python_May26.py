# Python Intermediate Workshop
# May 2026

# Day 1 - Abbie
import os 
os.chdir("Desktop/Positron Directory/Python/IntPy_May2026")
os.getcwd()

# strings, numerics, float
name = "Abbie"
age = 31
height = 66.5

print(name)

f"{name} is {age} years old."

# Libraries

import pandas as pd
import os
import datetime
import glob

# change directory - not doing this b/c I did at the top
# os.chdir
os.getcwd()

# how to manually create data by hand when using pandas
# create a data series (column) object 

stations = pd.Series(['Oxford', 'Abbeville', 'Water Valley', 'Holly Springs', 
'Senatobia', 'Houston', 'Batesville', "Myrtle"])

stations

# assigning station codes
pd.Series({'MS-LY-14': 'Oxford',
 'MS-LY-4' : 'Abbeville',
 'MS-YL-3' : 'Water Valley', 
 'MS-MS-6' : 'Holly Springs', 
 'MS-TT-1' : 'Seantobia', 
 'MS-CN-5' : 'Houston', 
 'MS-PN-7' : 'Batesville', 
 'MS-UN-3' : 'Myrtle' }, 
 name = 'Stations')

# creating a df in python
df_stations = pd.DataFrame({"Station ID" : ['MS-LY-14', 
'MS-LY-4', 
'MS-YL-3', 
'MS-MS-6', 
'MS-TT-1', 
'MS-CN-5', 
'MS-PN-7', 
'MS-UN-3'], 
"Station Name" : ['Oxford', 'Abbeville', 'Water Valley', 'Holly Springs', 'Senatobia', 
'Houston', 'Batesville', 'Myrtle'], 
"Date" : ['04/08/2026', '04/09/2026', '04/08/2026', '04/10/2026', 
'04/08/2026', '04/09/2026', '04/08/2026', '04/10/2026'], 
'Precipitation' : [0.05, 0.04, 0.01, 0.07, 0.08, 1.00, 0.99, 0.25]})

# print df
print(df_stations)

# importing a csv into a df
df_coco_2026 = pd.read_csv("data/CoCoRaHS_2026.csv")
print(df_coco_2026)

# making it more readable - calling head and tail
df_coco_2026.head()
df_coco_2026.head(8)
df_coco_2026.tail()

# calling info on the df
df_coco_2026.info()

# 
for filename in ['data/CoCoRaHS_2026.csv', 'data/CoCoRaHS_2025.csv'] : 
    data = pd.read_csv(filename)
    print(filename, data['ObservationDate'].max())

# import glob
print(f"All CoCoRaHS CSV files in data directory: {glob.glob('data/C*.csv')}")

# importing multiple csvs
for csv in glob.glob('data/C*.csv') : 
    data = pd.read_csv(csv, encoding = "UTF-8")
    print(csv, data['TotalPrecipAmt'].max())

# pulling the year in each file name
for csv in glob.glob('data/C*.csv') : 
    year = csv[14:18]
    print(f'Filename: {csv} year: {year}')

# making the master df
dfs = []
counter = 1

for csv in glob.glob('data/C*.csv') : 
    year = csv[14:18]
    data = pd.read_csv(csv, encoding = "UTF-8")
    data['Year'] = year
    print(f'{counter} Saving {len(data)} rows from {csv}')
    dfs.append(data)
    counter += 1

print(f'Number of saved DataFrames: {len(dfs)}')

# the big df
df_coco = pd.concat(dfs, ignore_index = True)
f'Number of rows in df: {len(df_coco)}'

# BREAK

# info on the large df
df_coco.info()
df_coco.shape # dimensions, no parenthesis, method not function
df_coco.describe() # you can see the only current numeric columns are lat/long 

df_coco = df_coco.rename(columns = {'ObservationDate' : 'ObsDate', 
'ObservationTime' : 'ObsTime', 
'StationNumber' : 'StationID', 
'Latitude' : 'Lat', 
'Longitude' : 'Long', 
'TotalPrecipAmt' : 'Precip'})

df_coco.columns

# changing data types of different columns
# first, join the columns and change the dates to date time
df_coco['ObsDateTime'] = pd.to_datetime(
    df_coco['ObsDate'] + ' ' + df_coco['ObsTime']
)

df_coco['ObsDateTime']

# creating new columns
df_coco['Year'] = df_coco.ObsDateTime.dt.year
df_coco['Month'] = df_coco.ObsDateTime.dt.month
df_coco['MonthName'] = df_coco.ObsDateTime.dt.strftime('%b')
df_coco['Day'] = df_coco.ObsDateTime.dt.day

df_coco.dtypes

df_coco = df_coco.replace({' T':0, ' NA': 'nan'})

df_coco['Precip'] = df_coco['Precip'].astype(float)

# to convert data types for multiple columns; calling columns with index values
cols = df_coco.columns[8:12]
df_coco[cols] = (
    df_coco[cols].apply(pd.to_numeric, errors = "coerce").astype(float)
)

df_coco.dtypes

# dropping columns from df
df_coco = df_coco.drop(columns = ['ObsDate', 'ObsTime', 'EntryDateTime', 'DateTimeStamp'])

# checking those dropped columns
df_coco.columns

# max and min values
print(f"max precipitation: {df_coco['Precip'].max()}")
print(f"max precipitation: {df_coco['Precip'].min()}")

# pulling unique values
print(f'Number of unique stations: {df_coco['StationName'].nunique()}')
# 279 unique stations

# getting the list of individual stations
print(df_coco['StationName'].unique())

# group by 
df_coco.groupby('StationName')['Precip'].sum()
df_coco.groupby('StationName')['Precip'].mean()

rain_by_station = df_coco.groupby('StationName')['Precip'].sum()
rain_by_station.sort_values(ascending = False).head(10)

# What if we wanted to look at a particular station? 
# filter to the Oxford station using a condition

df_coco['StationName'] == 'Oxford 3.9 N'

# creating a new var
ox = (df_coco['StationName'] == " Oxford 3.9 N")
df_coco.loc[ox] # loc slices based on row and column names 
df_coco.iloc[2:5] #iloc slices based on integer location
df_coco.iloc[:, 1]

df_coco.loc[ox, 'Precip']
df_coco.loc[ox, ['ObsDateTime', 'Precip']]

# creating a new df that only includes the oxford locations; we filtered earlier 
df_ox = df_coco.loc[ox]

# to save a df to a csv file
df_ox.to_csv('data/CoCoRaHS_ox.csv')

# to save as a df and not as csv; save as a pickle file
df_coco.to_pickle('data/CoCoRaHS_all.pkl')

####################
# Day 2 - Shelby

import pandas as pd
os.getcwd()

# using the NOAA dataset
df = pd.read_csv(r'data/NOAA_MSclimatedata.csv')
df.info()

# how many unique weather stations
pd.unique(df.STATION)
# unique station names
pd.unique(df.NAME)

# two different ways to call a column in pandas: df.column OR df['column']
df['NAME'].value_counts()
# audience question: how to get the percentages? SW didn't know
df['NAME'].value_counts(normalize = True) # I asked Gemini
df['NAME'].value_counts(normalize = True) * 100 # if I want whole numbers vs. decimals

df_uni = df[df['NAME'] == 'UNIVERSITY, MS US']
df_uni.info()

# only retain columns with station information, precipitation, and tempterature
df_uni = df_uni[['STATION', 'NAME', 'DATE', 'PRCP', 'SNOW', 'TMAX', 'TMIN']]
df_uni

# renaming
df_uni = df_uni.rename(columns = {'NAME' : 'station_name', 
'STATION' : 'station_id', 
'DATE' : 'full_date', 
'PRCP' : 'precip', 
'SNOW' : 'snow', 
'TMAX' : 'tmax', 
'TMIN' : 'tmin'})

# dates
df_uni['full_date'] = pd.to_datetime(df_uni['full_date'])
df_uni.info() #good: two strings, 1 date, 4 floats

# dates, continued
df_uni['year'] = df_uni.full_date.dt.year
df_uni['month'] = df_uni.full_date.dt.month
df_uni['month_name'] = df_uni.full_date.dt.strftime('%b') # %b is shorthand for abbrev, name of month

df_uni

# setting the index 
df_uni.set_index('full_date') # this doesn't overwrite the df
df_uni.set_index('full_date', inplace = True) # overwrites the df

######## Visualizations #########

import matplotlib.pyplot as plt

import seaborn as sns

# simple plot
df_uni.plot() # index is x-axis variable and then it tries to plot all the numeric vars

%matplotlib inline
df_uni['tmax'].plot() # didn't plot correctly, did now (SL added code above)

# filtering the df to 1926
year_1926 = df_uni.loc['1926-01-01':'1926-12-31']
year_1926

# then plotting the max temp year for the filtered df
year_1926['tmax'].plot()

year_1926['tmax'].plot(title = "Max Daily Temp for University, MS during 1926", color = "red", 
xlabel = "Date", 
ylabel = "Max Temp (F)")

# matplotlib vocab to know: 
# figure: The top level container for all plot elements (axes, titles, legends, etc)
# axes: an area where points can be specified using x, y, or polar coordintes; 
# this of this as the data layer for the plot
# axis: an object that sets scales, limits, and tick marks/tick labels; 
# think of this as information for the reader

# histogram with annual precipitation
# creating a new df first
yearlyprecip = df_uni.groupby(df_uni['year'], as_index = False)['precip'].sum().round(2)
yearlyprecip['year']= pd.to_datetime(yearlyprecip['year'], format = '%Y')
# now plotting using seaborn
sns.histplot(data = yearlyprecip, x = 'precip')
 
 # let's plot what we already created using matplotlib and seaborn
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

plt.figure(figsize = [15,5])
ax = sns.lineplot(data = year_1926, 
    x = 'full_date', 
    y = 'tmax', 
    color = 'red')
plt.title("Max Daily Temp for University, MS during 1926")
plt.xlabel("Date")
plt.ylabel("Max Temp (F)")
# set major tick marks to be months
ax.xaxis.set_major_locator(mdates.MonthLocator())
# format major tick marks to be the shortened names of the months
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))

# rolling average
year_1926['rolling_avg_high'] = year_1926['tmax'].rolling(window=5).mean()

# adding another layer to the plot we created before
plt.figure(figsize = [15,5])
ax = sns.lineplot(data = year_1926, 
    x = 'full_date', 
    y = 'tmax', 
    color = 'gray', alpha = 0.3)
sns.lineplot(data = year_1926, x = 'full_date', y = 'rolling_avg_high', color = 'red', label = '5-Day Average')
plt.title("Max Daily Temp for University, MS during 1926")
plt.xlabel("Date")
plt.ylabel("Max Temp (F)")
# set major tick marks to be months
ax.xaxis.set_major_locator(mdates.MonthLocator())
# format major tick marks to be the shortened names of the months
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))

# Activity: create a plot of maximum and minimum temps and rolling averages for both max and min
# change the titles and labels

# rolling average max
year_1926['rolling_avg_high'] = year_1926['tmax'].rolling(window=5).mean()
# rolling average min
year_1926['rolling_avg_low'] = year_1926['tmin'].rolling(window=5).mean()

# now plot all four lines together - max, min, rolling max, rolling min
plt.figure(figsize = [15,5])
ax = sns.lineplot(data = year_1926, 
    x = 'full_date', 
    y = 'tmax', 
    color = 'gray', alpha = 0.3)
sns.lineplot(data = year_1926, x = 'full_date', y = 'tmin', color = "black", alpha = 0.3)
sns.lineplot(data = year_1926, x = 'full_date', y = 'rolling_avg_high', color = 'red', label = '5-Day Average')
sns.lineplot(data = year_1926, x = 'full_date', y = 'rolling_avg_low', color = 'blue', label = '5-Day Average')
plt.title("University, MS High and Low Temps in 2026")
plt.xlabel("Date")
plt.ylabel("Max Temp (F)")
# set major tick marks to be months
ax.xaxis.set_major_locator(mdates.MonthLocator())
# format major tick marks to be the shortened names of the months
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))


## adding a line to set the style of the plot - see sns.set_style and final line of code
# also adding y ticks every 10 degrees
# adding saving a plot
plt.figure(figsize = [15,5])
sns.set_style("whitegrid")
ax = sns.lineplot(data = year_1926, 
    x = 'full_date', 
    y = 'tmax', 
    color = 'gray', alpha = 0.3)
sns.lineplot(data = year_1926, x = 'full_date', y = 'tmin', color = "black", alpha = 0.3)
sns.lineplot(data = year_1926, x = 'full_date', y = 'rolling_avg_high', color = 'red', label = '5-Day Average')
sns.lineplot(data = year_1926, x = 'full_date', y = 'rolling_avg_low', color = 'blue', label = '5-Day Average')
plt.title("University, MS High and Low Temps in 2026")
plt.xlabel("Date")
plt.ylabel("Max Temp (F)")
plt.yticks([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
# set major tick marks to be months
ax.xaxis.set_major_locator(mdates.MonthLocator())
# format major tick marks to be the shortened names of the months
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
ax.grid(axis = "x") # that takes off the y-axis lines in the background
# saving the plot
plt.savefig("temps1926.png", dpi = 300) # need to run this in the same code chunk as the plot or it saves an empty plot


# barplot - month by month precipitation
mo_precip = df_uni.groupby(df_uni['month'], as_index = False)['precip'].sum()
mo_precip['date'] = pd.to_datetime(mo_precip['month'], format = '%m')
mo_precip['month_name'] = mo_precip.date.dt.strftime("%b")
mo_precip

rainfall = sns.barplot(data = mo_precip, x = 'date', y = 'precip')
# fixing the x-axis names
rainfall.set_xticks(range(0, 12))
rainfall.set_xticklabels(mo_precip['month_name'].to_list())
rainfall.set_title("Total Rainfall by Month, 1910 - 2026")
# note to self, unlike ggplot, you need to run all this as a single block code

# Interactive Visualizations with Plotly
import plotly.express as px
df_coco = pd.read_csv("data/CoCoRaHS_2026.csv")

df_coco['ObservationDate'] = pd.to_datetime(df_coco['ObservationDate'])
df_coco.info()

df_coco.sort_values('ObservationDate', ascending = True, inplace = True)
df_coco.reset_index(drop = True, inplace = True)

january = df_coco.iloc[:3039]
january

# A month's worth precip
fig = px.line(january, x = 'ObservationDate', y = 'TotalPrecipAmt', color = 'StationName', 
title = "Precipitation by Station, January 2026")
fig.show()
january.info() # total precip is currently a string, need to change that!

january['TotalPrecipAmt'].unique().tolist() # there's T (trace) and NA

january['TotalPrecipAmt'] = january.TotalPrecipAmt.replace({' T': 0, ' NA': 'nan'}) # still a string
# turn to numeric
january['TotalPrecipAmt'] = january['TotalPrecipAmt'].astype(float)
january.info()

jan_subset = january[january['StationNumber'].isin([' MS-CK-4', 
' MS-JC-24', 
' MS-LY-4', 
' MS-LY-14', 
' MS-OK-26'])]

jan_subset
fig = px.line(jan_subset, 
    x = 'ObservationDate', 
    y = 'TotalPrecipAmt', 
    color = 'StationName', 
    title = 'Precipitation by Station, January 2026')
fig.show()


fig_bar = px.bar(yearlyprecip, 
    x = 'year', 
    y = 'precip', 
    title = 'Precipitation by Year, University, MS', 
    labels = {'precip': 'Annual Total Precipitation (in)'})
fig_bar.show()

# add a rolling average
yearlyprecip['rollingavg'] = yearlyprecip['precip'].rolling(window = 3).mean()

fig_bar2 = px.bar(yearlyprecip, 
    x = 'year', 
    y = 'precip', 
    title = 'Annual Precipitation by Year, University, MS', 
    labels = {'precip': 'Annual Total Precipitation (in)'})
fig_bar2.add_scatter(x = yearlyprecip['year'], 
    y = yearlyprecip['rollingavg'], 
    mode = 'lines', 
    name = '3 Year Rolling Avg')
fig_bar2.show()

# html! interactive & can view in your broswer
fig_bar2.write_html('barchart.html') # save to the working directly and will 
# open in your browser

# Last Example
# Animated Visualization

df_uni2 = df_uni.reset_index()
df_uni2

# Total precip by month across years
# Have to group by both year and month
df_rainfall = df_uni2.groupby([df_uni2['full_date'].dt.year.rename('year'), 
    df_uni2['month_name'].rename('month')])['precip'].sum().round(1).reset_index()

df_rainfall # precip totals for each month for every year in the df
# problem - months are alphabetical and we need to fix that
df_rainfall['date'] = df_rainfall['month'] + ' ' + df_rainfall['year'].astype(str)
df_rainfall['date'] = pd.to_datetime(df_rainfall['date'], format = '%b %Y')
df_rainfall.sort_values(by = 'date', inplace = True)
df_rainfall

# animated plot
anim_bar = px.bar(df_rainfall, 
    x = 'month', 
    y = 'precip', 
    animation_frame = 'year', 
    range_x = [-1, 12], 
    range_y = [0, 20], 
    title = 'Monthly Total Rainfall, 1910 - 2026')
anim_bar.show()

## Day 3 - Sian ## 
## tiny.cc/pyday3

os.getcwd() # set my wd and I downloaded the Kaggle train.csv to my directory
# libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# titantic dataset
df = pd.read_csv("data/train.csv")
df

# inspect the df
df.shape # like dimensions

df.head()
df.tail()
df.info()

# descriptive stats for numeric
df.describe()
df.describe(include = "all")
df.describe(include = "object")

# check missing values
df.isna().sum() 

# unique values for cat vars
df['Sex'].unique()
df['Embarked'].unique()
df['Pclass'].unique()

# Step 2: Data Cleaning and Preprocessing

# handle missing data
# 177 rows missing values for Age

df[df['Age'].isna()] # pulls rows with NA in Age

# median, mean, mode of Age column
df['Age'].median() # 28
df['Age'].mean() # 29.7
df['Age'].mode() # 24

median_age = df['Age'].median()

# Fill missing Age values with the median
df['Age'].fillna(median_age)
# overwrite the df
df['Age'] = df['Age'].fillna(median_age)
df.isna().sum() # the NAs are gone

# cabin still has 687 missing; embarked has 2 missing
# drop the two rows with embarked missing
df[df['Embarked'].isna()]
len(df) # 891 rows in df

# drop rows where embarked is missing and update the df
df = df.dropna(subset = ['Embarked'])
df.isna().sum()
len(df)

# create a new column to flag missing cabin data
df['Cabin'].isna()
df['Cabin'].notna().astype(int)
df['HasCabin'] = df['Cabin'].notna().astype(int)

df.columns
df.isna().sum()

# so now we drop the cabin column and use the hascabin column as the proxy
df = df.drop(columns = ['Cabin'])
df.columns

# select far and embarked columns
df[['Fare', 'Embarked']]

# Create a list of columns you want to select: exclude 'passenderID' 'name' and 'ticket'
df.columns
cols = ['Survived', 'Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked', 'HasCabin']
cols

# overwriting the df with just those cols
df = df[cols]

# renaming columns
df = df.rename(columns = {'Parch' : 'ParCh', 'Sex' : 'Gender'})
df

# filtering rows
# useful for remove outliers
# show rows where 'Fare' value is 0
df[df['Fare'] == 0]

# selecting rows where Fare > 0
df = df[df['Fare'] > 0]
df

# Feature Engineering
# creating feaatures that might help separate out later re: survival
# creating a family size variable based on siblings and parents
df['FamilySize'] = df['SibSp'] + df['ParCh'] + 1 # the one is him/herself
df

# IsAlone = 1 if FamilySize == 1 else 0
(df['FamilySize'] == 1).astype(int)
df['IsAlone'] = (df['FamilySize'] == 1).astype(int)
df

# save cleaned data
df.to_csv("titantic_cleaned.csv", index = False) # if you don't include that index = F, then the index becomes a column in the df

# Step 3: Exploratory Data Analysis (EDA)
df.info()

# seaborn package
# Univerate EDA
# outcome / target variable distribution
sns.countplot(x = "Survived", data = df)
plt.show()
# gender distribution
sns.countplot(x = "Gender", data = df)
plt.show()

# calculate and print the percentage of each gender
df['Gender'].value_counts(normalize = True) * 100

# passenger class
sns.countplot(x = "Pclass", data = df)
plt.show()

# percentage
df['Pclass'].value_counts(normalize = True)
plt.show()

# age distribution
sns.histplot(data = df, x = "Age", kde = True, bins = 8)
plt.show()

# fare distribution
sns.histplot(data = df, x = "Fare", kde = True, bins = 50)
plt.show()

# IsAlone distribution
sns.countplot(x = 'IsAlone', data = df)
plt.show()

## Bivariate EDA

# is alone and gender
sns.countplot(data = df, x = 'IsAlone', hue = 'Gender')
plt.show()

# relationships between fare and pclass
sns.boxplot(data = df, x = 'Pclass', y = 'Fare')
plt.show()


# Relationship with Target Variable (survived or not)
# barplot displays the mean of the variable with a 95% CI
sns.barplot(x = 'Gender', y = 'Survived', data = df)
plt.show()

df.groupby('Gender')['Survived'].mean()*100

# survival rate by passenger class
sns.barplot(x = 'Pclass', y = 'Survived', data = df)
plt.show()

# fare and survival
sns.boxplot(x = 'Survived', y = 'Fare', data = df)
plt.show()

# survival rate by family size
sns.barplot(x = 'FamilySize', y = 'Survived', data = df, estimator = 'mean', errorbar = None, color = 'skyblue')
plt.show()

# average survival rate by class and gender
grouped_a = df.groupby(['Pclass', 'Gender'])['Survived'].mean().reset_index()
print(grouped_a) # yup, women were most likely to survive, followed by wealth status

#### Step 4: Machine Learning
# logistic regression, decision tree, random forest
# install scikit-learn
# ML Libraries
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay, classification_report

# convert text columns into numeric form
df['Embarked'].unique()
df['Gender'].unique()

# convert gender to numeric
df['Gender'] = df['Gender'].map({'female':1, 'male':0})

# convert 'embarked' into dummy (0/1) columns
df = pd.get_dummies(df, columns=['Embarked'], drop_first= True)

# check the result
df.head()

# separate the features and target

features = df.drop(columns=['Survived']).columns
features

target = 'Survived'

x = df[features]
y = df[target]

x
y

# Split into train and test dataset (proportions: 80% train, 20% test)
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 42, stratify = y)

# check the proportions (0 vs. 1)
y.value_counts(normalize = True)
y_train.value_counts(normalize= True)
y_test.value_counts(normalize = True)
# yeah, the proportions are the same: approx 61% died, 38% survived

## Train Three Models: Logistic Regression, Decision Tree, and Random Forest

# standardization: logistic regression is sensitive to scales of features
scaler = StandardScaler()
scaler.fit(x_train) # learn mean/sd from training only
x_train_s = scaler.transform(x_train)
x_test_s = scaler.transform(x_test)

x_train_s

# Train Model
lr_model = LogisticRegression(max_iter = 2000)
lr_model.fit(x_train_s, y_train)

# make predictions on the test set
lr_y_pred = lr_model.predict(x_test_s)

# create confusion matrix: y_test (actual) vs. lr_y_pred (prediction)
cm = confusion_matrix(y_test, lr_y_pred)
cm
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot(cmap = "Blues")
plt.title("Logistic Regression Confusion Matrix")
plt.show()

# performance metrics: accuracy, precision, recall, and F1-score
print(classification_report(y_test, lr_y_pred))

## Decision Tree, tree based model

# Train Model
tree_model = DecisionTreeClassifier(random_state=42, max_depth = 3)
tree_model.fit(x_train, y_train) # not sensitive to scale, so no need to standardize

# Make predictions on the Test set
tree_y_pred = tree_model.predict(x_test)

# create confusion matrix: y_test (actual) vs. tree_y_pred (prediction)
cm = confusion_matrix(y_test, tree_y_pred)
cm
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot(cmap = "Blues")
plt.show()

# visualize the decision tree structure - I LIKE THIS
plt.figure(figsize = (20, 10))
plot_tree(tree_model, feature_names = x_train.columns, class_names = ['0', '1'])
plt.title("Decision Tree Vis")
plt.show() # note: lower gini score is better; gini impurity score (mixing between 0 and 1)

# get and plot feature importance
importances = tree_model.feature_importances_
print(importances)

tree_fi_df = pd.DataFrame({'Feature': x_train.columns, 'Importance' : importances}).sort_values('Importance', ascending = False)
tree_fi_df # more important features are gender, Pclass, family size, age, hascabin

plt.figure(figsize = (8, 5))
plt.barh(tree_fi_df['Feature'], tree_fi_df['Importance'])
plt.gca().invert_yaxis()

## Random Forest - tree based model
# previously we used a single decision tree, random forest generates many different decision trees and then makes a final prediction

# Train the random forest model
rf_model = RandomForestClassifier(random_state =42)
rf_model.fit(x_train, y_train)

# make predictions on the Test set
rf_y_pred = rf_model.predict(x_test)

# create and display confusion matrix: y_test (actual) vs. y_pred (prediction)
cm = confusion_matrix(y_test, rf_y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot(cmap = "Blues")
plt.title("Random Forest - Confusion Matrix")
plt.show()

# Performance Metrics: accuracy, precision, recall, and F1-score
print(classification_report(y_test, rf_y_pred))

# can calculate feature importance but can't get the visual like in decision tree
importances = rf_model.feature_importances_
print(importances)

rf_fi_df = pd.DataFrame({'Feature': x_train.columns, 'Importance' : importances}).sort_values('Importance', ascending = False)
rf_fi_df # different than the decision tree 

## k-Fold Cross Validation
# provides a more robust and reliable performance evaluation by testing the model on multiple data splits
# helps tune hyperparamters and select the best model during the training phrase without touching the test dataset
# check performance of each iteration and then average all those

# compare model performance using 10-fold cross-validation accuracy
lr_score = cross_val_score(lr_model, x, y, cv = 10, scoring = 'accuracy')
tree_score = cross_val_score(tree_model, x, y, cv = 10, scoring = 'accuracy')
rf_score = cross_val_score(rf_model, x, y, cv = 10, scoring = 'accuracy')

lr_score
tree_score
rf_score

lr_score.mean()
lr_score.std()

tree_score.mean()
tree_score.std()

rf_score.mean()
rf_score.std()

# print results in a nice summary
## didn't get this final code
print('=== 10-Fold Cross-Validation Results ===')
print("Logistic Regression: Mean = {:.3f}, SD = {:.3f}".format(lr_score.mean(), lr_score.std()))
print("Decision Tree: Mean = {:.3f}, SD = {:.3f}".format(tree_score.mean(), tree_score.std()))
print("Random Forest: Mean = {:.3f}, SD = {:.3f}".format(rf_score.mean(), rf_score.std()))
