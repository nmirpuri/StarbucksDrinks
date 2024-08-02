import pandas as pd
import streamlit as st

# Read and clean the Starbucks dataset
@st.cache
def load_data():
    starbucks = pd.read_csv('starbucks.csv')
    starbucks.replace("Varies", pd.NA, inplace=True)
    starbucks.replace("varies", pd.NA, inplace=True)
    starbucks_clean = starbucks.dropna()
    columns_to_include = ['Beverage', 'Calories', ' Total Fat (g)', ' Sugars (g)', ' Protein (g) ', 'Caffeine (mg)']
    return starbucks_clean[columns_to_include]

starbucks_clean_df = load_data()

# Function to filter the dataset based on user preferences
def filter_drinks(df, preferences):
    filters = {
        'Caffeine (mg)': map_level_to_values_caffeine(preferences.get('Caffeine (mg)')),
        'Calories': map_level_to_values_calories(preferences.get('Calories')),
        ' Sugars (g)': map_level_to_values_sugars(preferences.get(' Sugars (g)')),
        ' Protein (g) ': map_level_to_values_protein(preferences.get(' Protein (g) ')),
        ' Total Fat (g)': map_level_to_values_total_fat(preferences.get(' Total Fat (g)'))
    }

    filtered_df = df.copy()
    applied_filters = []

    # Apply filters based on user preferences
    for column, value_range in filters.items():
        if value_range is None:
            continue
        
        if column not in filtered_df.columns:
            st.write(f"Warning: The column '{column}' does not exist in the data.")
            continue
        
        # Convert column to numeric and handle errors
        filtered_df[column] = pd.to_numeric(filtered_df[column], errors='coerce')
        if filtered_df[column].isnull().all():
            st.write(f"Warning: The column '{column}' has no valid numeric data.")
            continue
        
        # Debug output
        st.write(f"Filtering column: {column} with range {value_range}")
        
        try:
            filtered_df = filtered_df[filtered_df[column].between(*value_range)]
        except Exception as e:
            st.write(f"Error filtering column '{column}': {e}")

        applied_filters.append(column)

    # Check if the filtered dataframe is empty
    if filtered_df.empty:
        st.write("No drinks match your preferences.")
        return filtered_df

    return filtered_df

# Mapping of levels to numeric values for filtering
def map_level_to_values_sugars(level):
    if level == 'High':
        return (40, float('inf'))
    elif level == 'Medium':
        return (15, 40)
    elif level == 'Low':
        return (0, 15)
    elif level == 'No Preference':
        return None

def map_level_to_values_calories(level):
    if level == 'High':
        return (260, float('inf'))
    elif level == 'Medium':
        return (120, 260)
    elif level == 'Low':
        return (0, 120)
    elif level == 'No Preference':
        return None

def map_level_to_values_protein(level):
    if level == 'High':
        return (10, float('inf'))
    elif level == 'Medium':
        return (5, 10)
    elif level == 'Low':
        return (0, 5)
    elif level == 'No Preference':
        return None

def map_level_to_values_total_fat(level):
    if level == 'High':
        return (4, float('inf'))
    elif level == 'Medium':
        return (0.5, 4)
    elif level == 'Low':
        return (0, 0.5)
    elif level == 'No Preference':
        return None

def map_level_to_values_caffeine(level):
    if level == 'High':
        return (150, float('inf'))
    elif level == 'Medium':
        return (50, 150)
    elif level == 'Low':
        return (1, 50)
    elif level == 'Zero':
        return (0, 0)
    elif level == 'No Preference':
        return None

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
    caffeine_level = st.selectbox("Select Caffeine level:", ['High', 'Medium', 'Low', 'Zero', 'No Preference'])
    calories_level = st.selectbox("Select Calories level:", ['High', 'Medium', 'Low', 'No Preference'])
    sugars_level = st.selectbox("Select Sugar level:", ['High', 'Medium', 'Low', 'No Preference'])
    protein_level = st.selectbox("Select Protein level:", ['High', 'Medium', 'Low', 'No Preference'])
    total_fat_level = st.selectbox("Select Total Fat level:", ['High', 'Medium', 'Low', 'No Preference'])

    preferences = {
        'Calories': calories_level,
        ' Protein (g) ': protein_level,
        ' Total Fat (g)': total_fat_level,
        ' Sugars (g)': sugars_level,
        'Caffeine (mg)': caffeine_level
    }

    filtered_starbucks = filter_drinks(starbucks_clean_df, preferences)

    if filtered_starbucks.empty:
        st.write("No drinks match your preferences.")
    else:
        filtered_starbucks = filtered_starbucks.drop_duplicates(subset=['Beverage']).head(5)
        st.write("Recommended Starbucks Drinks based on your preferences:")
        st.write(filtered_starbucks)

if __name__ == "__main__":
    main()



