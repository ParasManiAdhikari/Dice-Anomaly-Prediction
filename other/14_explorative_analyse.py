import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Connect to SQLite database and load data
conn = sqlite3.connect('Anomalie_Zustand.db')
query = "SELECT * FROM mockdata " 
df = pd.read_sql_query(query, conn)
conn.close()

# Convert timestamp to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'], format='%d-%m-%Y %H:%M:%S:%f')

# Settng label column
df['label'] = df['label'].astype('category')

# Characteristics to analyze
characteristics = ['ax', 'ay', 'az', 'gx', 'gy', 'gz']


# Perform  analysis for each label

dfs = []

for label in df['label'].unique():
    label_df = df[df['label'] == label]
    
    # Calculate summary statistics for each characteristic
    summary_statistics_label = pd.DataFrame(columns=['Label', 'Characteristic', 'Mean', 'Min', 'Max', 'Std'])
    for characteristic in characteristics:
        mean = label_df[characteristic].mean()
        min_val = label_df[characteristic].min()
        max_val = label_df[characteristic].max()
        std = label_df[characteristic].std()
        
        # Append summary statistics to the DataFrame
        summary_statistics_label = pd.concat([summary_statistics_label, pd.DataFrame({'Label': label,
                                                                                     'Characteristic': characteristic,
                                                                                     'Mean': mean,
                                                                                     'Min': min_val,
                                                                                     'Max': max_val,
                                                                                     'Std': std}, index=[0])], ignore_index=True)
    dfs.append(summary_statistics_label)

# Concatenate DataFrames for all labels
summary_statistics = pd.concat(dfs, ignore_index=True)

# Export summary statistics as a table (CSV)
summary_statistics.to_csv('summary_statistics_by_label.csv', index=False)

# Print summary statistics
print("Summary Statistics by Label:")
print(summary_statistics)


# Distribution plots for each characteristic
for characteristic in characteristics:
    plt.figure(figsize=(10, 5))
    sns.histplot(df, x=characteristic, hue='label', kde=True, element="step")
    plt.title(f'Distribution of {characteristic} by Label')
    plt.show()

# Correlation matrix for all data with hue
plt.figure(figsize=(12, 8))
sns.heatmap(df[characteristics].corr(), annot=True, cmap='coolwarm')
plt.title('Correlation Matrix for all data')
plt.show()

# Calculate and plot correlation matrices for each label
for label in df['label'].unique():
    label_df = df[df['label'] == label]
    corr_matrix = label_df[characteristics].corr()
    print(corr_matrix)
    plt.figure(figsize=(12, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
    plt.title(f'Correlation Matrix for {label} class')
    plt.show()
