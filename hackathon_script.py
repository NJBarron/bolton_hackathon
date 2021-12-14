# helpful link for matplotlib resources
# https://www.w3schools.com/python/matplotlib_plotting.asp
# w3schools also has alot of good resources on pandas ect

# imports
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# remove limits fo columns/rows when using data_set.head()
pd.options.display.max_columns = None
pd.options.display.max_rows = None

# read the csv file and read columns
# data_set must be in same directory as script
data = pd.read_csv('data_set.csv')

# print all columns in raw data file
# [print(col) for col in data.columns]

# create new data frame and add columns to it

data_set = pd.DataFrame()

def create_excel_doc(data_frame, output='output.xlsx'):

	# creates excel document using argument data_frame
	# outputs file as output argument
	# example of calling function
	# create_excel_doc(data_set, 'bolton_data.xlsx')

	try:
		data_frame.to_excel(output)
	except:
		print(output, ' might already exist')


# get Region either north east/west
data_set['Region'] = data['Region']

# local area
data_set['Local'] = data['Local Authority']

# K
data_set['Population'] = data['Mid-year Population (thousands)']

# 2010-2019
data_set['Year'] = data['Calendar Year']

# sub sector
data_set['Sector'] = data['LA CO2 Sub-sector']

# Emissions are measured in Kt CO2.
# data_set['Emissions'] = data['Territorial emissions (kt CO2)']

# some graphs don't have issues with negative values so we use this column of emissions 
# same results overall
data_set['Emissions'] = data['Emissions within the scope of influence of LAs (kt CO2)']

# remove regions that arent in var regions
regions = ['North West', 'North East']
data_set = data_set[data_set['Region'].isin(regions)]

# remove years not inbetween 2010-2019

# range is between 2010 and 2020 because
# of the way python range function works 
# still returns a list of numbers between 2010 and 2019

years = list(range(2010, 2020))
data_set = data_set[data_set['Year'].isin(years)]

# sort some data

# here we run some functions on all the records of columns
# we round the emissions
# then change population from 90.112 to 90112

data_set['Population'] = data_set['Population'].apply(lambda x: int(str(x).replace('.', '')))
data_set['Emissions'] = data_set['Emissions'].apply(lambda x: round(x, 2))

def pie_example():

	data_bolton = data_set.loc[data_set['Local'] == 'Bolton']
	data_bolton = data_bolton.loc[data_set['Emissions'] > 5]
	data_bolton = data_bolton.loc[data_set['Year'] == 2019]

	plt.pie(data_bolton['Emissions'], labels=data_bolton['Sector'], autopct='%1.1f%%')
	plt.title("Bolton 2019 Emissions Per Sector")
	plt.show()


# function for some reason won't work unless we pass data_set as an argument but oh well
def bar_example(data_set):

	data_set = data_set.loc[data_set['Year'] == 2019]
	plt.bar(data_set['Local'], data_set['Emissions'])

	plt.title("Local's Emissions in 2019")

	plt.xticks(rotation=90)

	plt.xlabel("Local")
	plt.ylabel("Emission")

	plt.show()


# running this has showed that since 2010-2019
# on avg a local has reduced its annual carbon emissions by 50%

def get_information(data_set):

	# var valv is a list which we store dictionaries into
	# each dictionary represents one record storing information on Local, Year, Emissions
	valv = [

	]

	default = data_set

	# var LocalAreas defines what Local Authorities we want to depcict in our graph
	LocalAreas = ['Bolton', 'Bury', 'Preston', 'Wigan']

	# for loop summed up
	# for every single area and for every year of that area
	for Local in LocalAreas:
		for yr in years:

			# because we edit data_set later in for loop we set it back 
			# each iteration to it's original value
			data_set = default

			# here we get the sort data removing data that isn't == to yr or Local vars.
			data_set = data_set.loc[data_set['Year'] == yr]
			data_set = data_set.loc[data_set['Local'] == Local]

			# define t_emission as total emissions at one Local area during one year
			t_emission = sum(data_set['Emissions'])
			
			# round val
			t_emission = round(t_emission, 2)

			record = {"Local": Local, "Year": yr, "Emissions": t_emission}
			valv.append(record)

	return valv

def cool_graph(data_set):

	values = get_information(data_set)
	values = pd.DataFrame().from_dict(values)

	fig = plt.figure(figsize=(30,10))
	plt.title('Carbon Emissions (kT) Per Local (2010-2019)')

	sns.set(font_scale=1)
	sns.barplot(y='Emissions',x='Year',hue='Local',data=values,palette='deep');
	plt.ylabel('Emissions')
	plt.xticks(rotation=45)
	plt.yticks(rotation=90)
	plt.tight_layout()
	plt.show()


# call graphs stored under functions
pie_example()
bar_example(data_set)
cool_graph(data_set)

