import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

url = "https://pokeapi.co/api/v2/pokemon/charizard"

response = requests.get(url)

print(response.json())

if response.status_code == 200:
    # Get the JSON data
    pokemon_data = response.json()
    
    # Create a dictionary with the data we want to analyze
    cleaned_data = {
        'name': pokemon_data['name'],
        'height': pokemon_data['height'],
        'weight': pokemon_data['weight'],
        'base_experience': pokemon_data['base_experience'],
        'abilities': [ability['ability']['name'] for ability in pokemon_data['abilities']],
        'types': [type_info['type']['name'] for type_info in pokemon_data['types']],
        'stats': {stat['stat']['name']: stat['base_stat'] for stat in pokemon_data['stats']}
    }

    # Convert to DataFrame for easier analysis
    pokemon_df = pd.DataFrame([cleaned_data])
    
    # Explode the abilities and types lists into separate rows
    abilities_df = pd.DataFrame(cleaned_data['abilities'], columns=['abilities'])
    types_df = pd.DataFrame(cleaned_data['types'], columns=['types'])
    
    # Create a stats DataFrame
    stats_df = pd.DataFrame([cleaned_data['stats']])
    
    print("\nCleaned Pokemon Data:")
    print(pokemon_df.drop(['abilities', 'types', 'stats'], axis=1))
    print("\nAbilities:")
    print(abilities_df)
    print("\nTypes:")
    print(types_df)
    print("\nStats:")
    print(stats_df)
else:
    print(f"Error fetching data: {response.status_code}")
    # Create visualizations for Pokemon stats
    plt.figure(figsize=(12, 6))

    # Bar plot of base stats
    plt.subplot(1, 2, 1)
    stats_df.T.plot(kind='bar', color='skyblue')
    plt.title(f'{pokemon_data["name"].title()} Base Stats')
    plt.xlabel('Stat')
    plt.ylabel('Value') 
    plt.xticks(rotation=45)

    # Radar/Spider plot of stats
    plt.subplot(1, 2, 2)
    stats = stats_df.iloc[0].values
    stats_labels = stats_df.columns
    angles = np.linspace(0, 2*np.pi, len(stats_labels), endpoint=False)
    
    # Close the plot by appending first value
    stats = np.concatenate((stats,[stats[0]]))
    angles = np.concatenate((angles,[angles[0]]))
    
    ax = plt.subplot(1, 2, 2, projection='polar')
    ax.plot(angles, stats)
    ax.fill(angles, stats, alpha=0.25)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(stats_labels)
    plt.title(f'{pokemon_data["name"].title()} Stats Radar')

    plt.tight_layout()
    plt.show()
