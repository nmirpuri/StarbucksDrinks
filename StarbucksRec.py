import pandas as pd
import streamlit as st

# Read and clean the Starbucks dataset
@st.cache
def load_data():
    starbucks = pd.read_csv(r'starbucks.csv')
    starbucks.replace("Varies", pd.NA, inplace=True)
    starbucks.replace("varies", pd.NA, inplace=True)
    starbucks_clean = starbucks.dropna()
    columns_to_include = ['Beverage', 'Calories', ' Total Fat (g)', ' Sugars (g)', ' Protein (g) ', 'Caffeine (mg)', 'Beverage_prep']
    return starbucks_clean[columns_to_include]

starbucks_clean_df = load_data()

# Function to filter the dataset based on user preferences with prioritized relaxation
def filter_drinks(df, preferences):
    filters = {
        'Caffeine (mg)': map_level_to_values_caffeine(preferences['Caffeine (mg)']),
        'Calories': map_level_to_values_calories(preferences['Calories']),
        ' Sugars (g)': map_level_to_values_sugars(preferences[' Sugars (g)']),
        'Beverage_prep': preferences['Beverage_prep'],
        ' Protein (g) ': map_level_to_values_protein(preferences[' Protein (g) ']),
        ' Total Fat (g)': map_level_to_values_total_fat(preferences[' Total Fat (g)'])
    }

    filtered_df = df.copy()
    applied_filters = []

    # Apply filters based on user preferences
    for column, value_range in filters.items():
        if column == 'Beverage_prep':
            filtered_df = filtered_df[filtered_df[column] == value_range]
        else:
            # Ensure the column is numeric for filtering
            filtered_df[column] = pd.to_numeric(filtered_df[column], errors='coerce')
            filtered_df = filtered_df[filtered_df[column].between(*value_range)]
        applied_filters.append(column)
    
    # Check if the filtered dataframe is empty
    if filtered_df.empty:
        st.write("No exact matches found. Relaxing filters step by step.")
        # Relax filters one by one
        for column in applied_filters:
            if column == 'Beverage_prep':
                continue
            value_range = filters[column]
            filtered_df = df.copy()
            for applied_column in applied_filters:
                if applied_column == column:
                    continue
                if applied_column == 'Beverage_prep':
                    filtered_df = filtered_df[filtered_df[applied_column] == filters[applied_column]]
                else:
                    filtered_df[applied_column] = pd.to_numeric(filtered_df[applied_column], errors='coerce')
                    filtered_df = filtered_df[filtered_df[applied_column].between(*filters[applied_column])]
            filtered_df = filtered_df[filtered_df[column].between(*value_range)]
            if not filtered_df.empty:
                break

    return filtered_df

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

# Streamlit app
def main():
    st.title("Starbucks Drink Recommender")

    st.markdown(
        """
        <div style='text-align:center;'>
            <img src='https://upload.wikimedia.org/wikipedia/en/thumb/d/d3/Starbucks_Corporation_Logo_2011.svg/1200px-Starbucks_Corporation_Logo_2011.svg.png' alt='Starbucks Logo' width='200'/>
        </div>
        """,
        unsafe_allow_html=True
    )

    # User input for preferences
    caffeine_level = st.selectbox("Select Caffeine level:", ['High', 'Medium', 'Low', 'Zero'])
    calories_level = st.selectbox("Select Calories level:", ['High', 'Medium', 'Low'])
    sugars_level = st.selectbox("Select Sugar level:", ['High', 'Medium', 'Low'])
    protein_level = st.selectbox("Select Protein level:", ['High', 'Medium', 'Low'])
    total_fat_level = st.selectbox("Select Total Fat level:", ['High', 'Medium', 'Low'])
    milk_type = st.selectbox("Select Milk type:", ['2% Milk', 'Grande Nonfat Milk', 'Short Nonfat Milk', 'Soymilk', 'Tall Nonfat Milk', 'Venti Nonfat Milk', 'Whole Milk'])

    preferences = {
        'Calories': calories_level,
        ' Protein (g) ': protein_level,
        ' Total Fat (g)': total_fat_level,
        ' Sugars (g)': sugars_level,
        'Caffeine (mg)': caffeine_level,
        'Beverage_prep': milk_type
    }

    filtered_starbucks = filter_drinks(starbucks_clean_df, preferences)

    if filtered_starbucks.empty:
        st.write("No exact matches found. Relaxing filters step by step.")
        filtered_starbucks = filter_drinks(starbucks_clean_df, preferences)

    filtered_starbucks = filtered_starbucks.drop_duplicates(subset=['Beverage']).head(5)

    st.write("\nRecommended Starbucks Drinks based on your preferences:")
    st.write(filtered_starbucks)

if __name__ == "__main__":
    main()
