# submitted by
# Muhammed Shahin Mohammed Ali Ayanippurath
# Student No: mm117408


import os
from urllib.request import urlopen


# Download the stock files from the URL and store it in the input folder
def download_data(stock_name):
    url = 'https://query1.finance.yahoo.com/v7/finance/download/' + stock_name + '?period1=1587042293&period2=1618578293&interval=1d&events=history&includeAdjustedClose=true'
    file_name = stock_name + '.csv'
    local_path = os.path.join('input', file_name)
    with urlopen(url) as file, open(local_path, 'wb') as f:
        f.write(file.read())


# Search for chv files in the directory and return the list of csv files
def get_csv_files(dir_path):
    files_list = os.listdir(dir_path)
    csv_files = []
    proj_folder = os.path.abspath('')
    for file in files_list:
        if file.endswith('.csv'):
            csv_files.append(os.path.join(proj_folder, 'input', file))
    return csv_files


# Add 'Pct Change' as a new heading by appending it to first line,
# and for every other line, calculate the percentage change and append
def calculate_csv(file_name):
    result_data = []
    with open(file_name, 'r') as f:
        lines = f.readlines()
        header = lines.pop(0)
        result_data.append(header.strip().split(',') + ['Pct Change'])
        for line in lines:
            daily_data = line.strip().split(',')
            open_price, close_price = float(daily_data[1]), float(daily_data[4])
            percentage_change = round(((close_price - open_price) / open_price) * 100, 2)
            result_data.append(daily_data + [str(percentage_change)])
        return result_data


# Check if file exists, if so, remove it and creat a new file with the same name and
# and write the data to it
def write_csv(file_name, write_data):
    if os.path.exists(file_name):
        os.remove(file_name)
    with open(file_name, 'a') as f:
        for data in write_data:
            f.write(','.join(data) + '\n')


# The list of required stock names are iterated, and for each of them, data in downloaded.
# For each csv files in input folder, the calculation is done
# and the result data is written overwriting the previous version
if __name__ == '__main__':
    stock_names = ['MSFT', 'GOOG', 'IBM']
    for stock_name in stock_names:
        download_data(stock_name)
    for csv_file in get_csv_files('./input'):
        write_csv(csv_file, calculate_csv(csv_file))
