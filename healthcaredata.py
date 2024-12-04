import requests
import pandas as pd

# Your Data.gov API key
API_KEY = 'Create personal API key at Data.gov'

# Dataset URL for COVID-19 cases and deaths
dataset_url = 'https://api.covidtracking.com/v1/states/current.json'

# Define query parameters (optional for this dataset)
params = {
    'api_key': API_KEY,
}

# Make the API request
response = requests.get(dataset_url, params=params)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    # Convert the data to a DataFrame
    covid_df = pd.DataFrame(data)
    print(covid_df.head())  # Display the first few rows
else:
    print(f"Error: {response.status_code}, {response.text}")

# Total cases and deaths by state
state_cases = covid_df[['state', 'positive', 'death']].copy()
state_cases.columns = ['State', 'Cases', 'Deaths']

# Sorting by the number of cases in descending order
state_cases = state_cases.sort_values(by='Cases', ascending=False)

# Display the top 10 states with the highest cases
print(state_cases.head(10))

import matplotlib.pyplot as plt

# Plotting the top 10 states with the highest COVID-19 cases
top_states = state_cases.head(10)

plt.figure(figsize=(12, 8))
plt.barh(top_states['State'], top_states['Cases'], color='blue')
plt.xlabel('Number of Cases')
plt.title('Top 10 U.S. States with the Most COVID-19 Cases')
plt.gca().invert_yaxis()  # Invert to have the largest at the top
plt.show()

# Fetch historical data (from past dates)
dataset_url = 'https://api.covidtracking.com/v1/us/daily.json'

response = requests.get(dataset_url, params=params)

if response.status_code == 200:
    data = response.json()
    covid_trends_df = pd.DataFrame(data)
    print(covid_trends_df.head())
