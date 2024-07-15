import itertools
import os
import pandas as pd
import matplotlib.pyplot as plt
import constants as const
import shutil


base_path = const.base_path
base_path_output = f'{base_path}/output'
data_file_name = None
os.makedirs(base_path_output, exist_ok=True)


def clear_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')


def histogram_plot(df):
    df.hist(figsize=(10, 6))
    plt.suptitle('Histograms for Iris Dataset')
    plt.tight_layout()
    plt.subplots_adjust(top=0.9)
    plt.savefig(f'{base_path_output}/{data_file_name}_Histogram.png')
    plt.close()


def line_plot(df):
    # Select only numeric columns
    numeric_columns = df.select_dtypes(include=['number']).columns
    # Plot histogram for each numeric column
    for column in numeric_columns:
        plt.figure(figsize=(6, 6))
        numeric_data = df.select_dtypes(include='number')
        # print(numeric_data)
        plt.plot(numeric_data[column], color='green', label=column, linestyle='-', marker='o')
        plt.title('Line Plot')
        plt.xlabel('Index')
        plt.ylabel(column)
        plt.legend()
        plt.grid(True)
        plt.savefig(f'{base_path_output}/Output_{column}_LinePlot.png')
        plt.close()


def scatter_plot(df):
    numeric_columns = df.select_dtypes(include=['number']).columns
    for col1, col2 in itertools.combinations(numeric_columns, 2):
        plt.figure(figsize=(10, 6))
        plt.scatter(df[col1], df[col2], alpha=0.7)
        plt.title(f'Scatter Plot:{col1} vs {col2}')
        plt.xlabel(col1)
        plt.ylabel(col2)
        plt.grid(True)
        plt.savefig(f'{base_path_output}/scatter_{col1}_vs_{col2}.png')
        plt.close()


def box_plot(df):
    numeric_df = df.select_dtypes(include='number')
    for column in numeric_df.columns:
        plt.figure(figsize=(10, 6))
        plt.boxplot(numeric_df[column])
        plt.title(f'Box plot of {column}')
        plt.xlabel(column)
        plt.ylabel('Values')
        plt.savefig(f'{base_path_output}/box_{column}.png')
        plt.close()


def calculate_statistics(df):
    mean_values = df.mean(numeric_only=True)
    mode_values = df.mode().iloc[0]
    median_values = df.median(numeric_only=True)
    range_values = df.max(numeric_only=True) - df.min(numeric_only=True)
    std_div_values = df.std(numeric_only=True)
    correlation_matrix = df.corr(numeric_only=True)

    print(f"Mean for the columns:\n{mean_values}")
    print(f"Mode for the columns:\n{mode_values}")
    print(f"Range for the columns:\n{median_values}")
    print(f"Range for the columns:\n{range_values}")
    print(f'Standard Division for the columns:\n{std_div_values}')
    print(f"Correlation matrix for the columns:\n{correlation_matrix}")
    return mean_values, mode_values, median_values, range_values, std_div_values, correlation_matrix


def main():
    global data_file_name
    data_file = input('please enter data file path...').strip()
    data_file = os.path.normpath(data_file)
    df = pd.read_csv(data_file, delimiter=',')
    base_name = os.path.basename(data_file)

    # Split the base name to remove the extension (e.g., 'iris')
    data_file_name = os.path.splitext(base_name)[0]

    clear_directory(directory=base_path_output)

    excel_file = f'{base_path_output}/{data_file_name}.xlsx'
    df.to_excel(excel_file, index=False)
    print(f"Data has been successfully converted to {excel_file} ")

    mean_values, mode_values, median_values, range_values, std_div_values, correlation_matrix = calculate_statistics(df)

    histogram_plot(df)
    scatter_plot(df)
    box_plot(df)
    line_plot(df)


if __name__ == "__main__":
    main()
