import pandas as pd

# Read and clean the Starbucks dataset
starbucks = pd.read_csv('/Users/nikhi/OneDrive/Desktop/OPT Application/Mirpuri Family Pics/Dubai/Starbucks McDonals Data/starbucks.csv')
starbucks.replace("Varies", pd.NA, inplace=True)
starbucks.replace("varies", pd.NA, inplace=True)
starbucks_clean = starbucks.dropna()

# Define the columns to include in the cleaned DataFrame
columns_to_include = ['Beverage', 'Calories', ' Total Fat (g)', ' Sugars (g)', ' Protein (g) ', 'Caffeine (mg)']
starbucks_clean_df = starbucks_clean[columns_to_include]

# Function to get nutritional preferences from the user
def get_nutritional_preferences():
    levels = ['High', 'Medium', 'Low']
    caff_levels = ['High', 'Medium', 'Low', 'Zero']

    calories_level = ''
    protein_level = ''
    total_fat_level = ''
    caffeine_level = ''
    sugars_level = ''
    milk_type = ''

    while caffeine_level not in caff_levels:
        caffeine_level = input("Enter Caffeine level (High, Medium, Low, Zero): ").capitalize()

    while calories_level not in levels:
        calories_level = input("Enter Calories level (High, Medium, Low): ").capitalize()

    while sugars_level not in levels:
        sugars_level = input("Enter Sugar level (High, Medium, Low): ").capitalize()

    while protein_level not in levels:
        protein_level = input("Enter Protein level (High, Medium, Low): ").capitalize()

    while total_fat_level not in levels:
        total_fat_level = input("Enter Total Fat level (High, Medium, Low): ").capitalize()

    return {
        'Calories': calories_level,
        ' Protein (g) ': protein_level,
        ' Total Fat (g)': total_fat_level,
        ' Sugars (g)': sugars_level,
        'Caffeine (mg)': caffeine_level,
    }

# Mapping of levels to numeric values for filtering
def map_level_to_values_sugars(level):
    if level == 'High':
        return (40, float('inf'))
    elif level == 'Medium':
        return (15, 40)
    elif level == 'Low':
        return (0, 15)

def map_level_to_values_calories(level):
    if level == 'High':
        return (260, float('inf'))
    elif level == 'Medium':
        return (120, 260)
    elif level == 'Low':
        return (0, 120)

def map_level_to_values_protein(level):
    if level == 'High':
        return (10, float('inf'))
    elif level == 'Medium':
        return (5, 10)
    elif level == 'Low':
        return (0, 5)

def map_level_to_values_total_fat(level):
    if level == 'High':
        return (4, float('inf'))
    elif level == 'Medium':
        return (0.5, 4)
    elif level == 'Low':
        return (0, 0.5)

def map_level_to_values_caffeine(level):
    if level == 'High':
        return (150, float('inf'))
    elif level == 'Medium':
        return (50, 150)
    elif level == 'Low':
        return (1, 50)
    elif level == 'Zero':
        return (0, 0)

# Function to filter the dataset based on user preferences with prioritized relaxation
def filter_drinks(df, preferences):
    filters = {
        'Caffeine (mg)': map_level_to_values_caffeine(preferences['Caffeine (mg)']),
        'Calories': map_level_to_values_calories(preferences['Calories']),
        ' Sugars (g)': map_level_to_values_sugars(preferences[' Sugars (g)']),
        ' Protein (g) ': map_level_to_values_protein(preferences[' Protein (g) ']),
        ' Total Fat (g)': map_level_to_values_total_fat(preferences[' Total Fat (g)'])
    }

    filtered_df = df.copy()

    # Apply filters in the order of importance
    for column, value_range in filters.items():
        if column == 'Beverage_prep':
            filtered_df = filtered_df[filtered_df[column] == value_range]
        else:
            filtered_df = filtered_df[filtered_df[column].astype(float).between(*value_range)]
        if not filtered_df.empty:
            break  # Stop relaxing filters if we have results

    return filtered_df

# Main function
def main():
    preferences = get_nutritional_preferences()

    filtered_starbucks = filter_drinks(starbucks_clean_df, preferences)

    if filtered_starbucks.empty:
        print("No exact matches found. Relaxing filters step by step.")
        filtered_starbucks = filter_drinks(starbucks_clean_df, preferences)

    filtered_starbucks = filtered_starbucks.drop_duplicates(subset=['Beverage']).head(5)

    print("\nRecommended Starbucks Drinks based on your preferences:")
    print(filtered_starbucks)

if __name__ == "__main__":
    main()
