import pandas as pd

# Read the CSV file
# Note: You may need to adjust the path to where your file is stored
file_path = "/home/garcon/Documents/github/data_and_ia/src/data/eCO2mix_RTE_Bretagne_Annuel-Definitif_2022.csv"  # Replace with your actual file path

# Reading the file with appropriate parameters
# The data appears to use comma as separator and quotes around text fields
df = pd.read_csv(file_path, sep=',', quotechar='"', encoding='utf-8')

# Initial exploration of the data
print("DataFrame shape:", df.shape)
print("\nColumn names:")
print(df.columns.tolist())
print("\nFirst few rows:")
print(df.head())

# Convert numeric columns that might be read as strings due to "-" or other special characters
# This function will convert columns to numeric, coercing errors (like "-") to NaN
def convert_to_numeric(df, columns):
    for col in columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

# List of columns that should be numeric (you may need to adjust this list)
numeric_columns = ['Consommation', 'Thermique', 'Eolien', 'Solaire', 'Hydraulique', 
                  'Pompage', 'Stockage batterie', 'Eolien terrestre', 'Eolien offshore',
                  'TCO Thermique (%)', 'TCH Thermique (%)', 'TCO Eolien (%)',
                  'TCH Eolien (%)', 'TCO Solaire (%)', 'TCH Solaire (%)',
                  'TCO Hydraulique (%)', 'TCH Hydraulique (%)']

# Convert columns to numeric
df = convert_to_numeric(df, numeric_columns)

# Calculate means for numeric columns
means = df[numeric_columns].mean()

print("\nMean values for numeric columns:")
print(means)

# If you want to filter data before calculating means, e.g., by date or region
# For example, calculate means for a specific region
if 'Nature' in df.columns:
    bretagne_data = df[df['Nature'] == 'Bretagne']
    bretagne_means = bretagne_data[numeric_columns].mean()
    print("\nMean values for Bretagne:")
    print(bretagne_means)

# You can also group by other columns like Date or Nature to get means by group
if 'Date' in df.columns:
    date_means = df.groupby('Date')[numeric_columns].mean()
    print("\nMean values by date:")
    print(date_means.head())  # Showing just the first few dates

# Save the means to a CSV file
means.to_csv('mean_values.csv')
print("\nMean values have been saved to 'mean_values.csv'")