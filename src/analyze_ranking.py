import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def analyze_ranking():
    # Load the data
    # The file has 3 header rows essentially:
    # 0: Column codes (Q8_1, etc.)
    # 1: Full question text
    # 2: Metadata/Import IDs (e.g., {"ImportId":"QID8_1"})
    # We'll read the header from row 0 and skip rows 1 and 2 for the data.

    filepath = 'data/Alternative CPA Pathways Survey_December 31, 2025_09.45.csv'

    # Read just the header to get column names
    df_header = pd.read_csv(filepath, nrows=0)
    columns = df_header.columns.tolist()

    # Read the data, skipping the 2nd and 3rd rows (indices 1 and 2)
    # Note: header=0 reads the first row as header. skiprows=[1, 2] skips the next two.
    df = pd.read_csv(filepath, header=0, skiprows=[1, 2])

    # Define the mapping for Q8 columns
    ranking_columns = {
        'Q8_1': 'Auditing',
        'Q8_2': 'Taxation',
        'Q8_3': 'Financial Accounting',
        'Q8_4': 'Management Accounting',
        'Q8_5': 'Information Systems',
        'Q8_6': 'Data Analytics',
        'Q8_7': 'Other Business Management'
    }

    # Filter for the relevant columns
    cols_to_use = list(ranking_columns.keys())

    # Check if columns exist
    missing_cols = [c for c in cols_to_use if c not in df.columns]
    if missing_cols:
        print(f"Warning: Missing columns: {missing_cols}")
        return

    df_rankings = df[cols_to_use].copy()

    # Convert columns to numeric, coercing errors to NaN
    for col in cols_to_use:
        df_rankings[col] = pd.to_numeric(df_rankings[col], errors='coerce')

    # Drop rows with all NaNs in these columns (optional, but good practice)
    df_rankings.dropna(how='all', inplace=True)

    # Calculate the mean rank for each discipline
    # Lower rank (1) is better/more beneficial.
    mean_ranks = df_rankings.mean().sort_values()

    # Rename index using the mapping
    mean_ranks.index = mean_ranks.index.map(ranking_columns)

    # Create the plot
    plt.figure(figsize=(12, 8))
    sns.set_style("whitegrid")

    # Plot bar chart
    # Since rank 1 is "Most Beneficial", we might want to invert the axis or just explain it.
    # A lower bar is "better".
    ax = sns.barplot(x=mean_ranks.index, y=mean_ranks.values, hue=mean_ranks.index, palette="viridis", legend=False)

    plt.title('Average Ranking of Graduate Program Specializations\n(Lower Score = More Beneficial)', fontsize=16)
    plt.ylabel('Average Rank (1 = Most Beneficial, 7 = Least Beneficial)', fontsize=12)
    plt.xlabel('Discipline', fontsize=12)
    plt.xticks(rotation=45, ha='right')

    # Add value labels on top of bars
    for i, v in enumerate(mean_ranks.values):
        ax.text(i, v + 0.1, f'{v:.2f}', ha='center', va='bottom', fontsize=10)

    plt.tight_layout()

    # Save the plot
    output_dir = 'outputs'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'rank_order.png')
    plt.savefig(output_path, dpi=300)
    print(f"Ranking plot saved to {output_path}")

    # Print the ranking to console as well
    print("\nCalculated Average Rankings:")
    print(mean_ranks)

if __name__ == "__main__":
    analyze_ranking()
