import pandas as pd
import numpy as np
from datetime import datetime
import time
import os


def display_elements(df, colname):
    colnames_list = list(pd.unique(df[colname]))
    print('*' * 100)
    print(pd.DataFrame({colname: colnames_list}))
    print('*' * 100)
    return colnames_list


def get_inputs():
    element_num = int(input('Type the corresponding number here:'))
    return element_num


def element_filter(df, colname):
    print('*' * 100)
    colname_list = display_elements(df, colname)
    print('*' * 100)
    element_num = get_inputs()
    print(f"Thanks! You chose: {colname_list[element_num]}")
    print('*' * 100)
    return df[df[colname] == colname_list[element_num]]


def criteria_filters(df):
    options = ['Country Ship To', 'Grade Desc', 'Region/Country']
    while len(options) != 0:
        print('*' * 100)
        print('\n')
        txt = "Grade/Country Filter"
        print(txt.center(90))
        print('*' * 100)
        print("Here are the options: ")
        print('\n')
        print(pd.DataFrame({'Options': options}))
        print('\n')
        print('*' * 100)
        colnum = int(input('Enter one of the option: '))
        print(f"Thanks! You chose: {options[colnum]}")
        df_1 = element_filter(df, options[colnum])
        options.remove(options[colnum])
        print('*' * 100)
        print('\n')
        ans = input(
            "Done Filtering? Enter 'Y' to exit to previous menu, 'N' to continue: ")
        print('\n')
        if ans.upper() == 'Y':
            return df_1
        print('*' * 100)
        print(txt.center(90))
        print('*' * 100)
        print('\n')
        print(pd.DataFrame({'Options': options}))
        print('*' * 100)
        print('\n')
        colnum = int(input('Enter one of the option: '))
        print(f"Thanks! You chose: {options[colnum]}")
        df_2 = element_filter(df_1, options[colnum])
        options.remove(options[colnum])
        print('*' * 100)
        print('\n')
        ans = input(
            "Done Filtering? Enter 'Y' to previous page, 'N' to continue: ")
        if ans.upper() == 'Y':
            return df_2
        print('*' * 100)
        print(txt.center(90))
        print('*' * 100)
        print(pd.DataFrame({'Options': options}))
        print('*' * 100)
        print('\n')
        colnum = int(input('Enter one of the option: '))
        print(f"Thanks! You chose: {options[colnum]}")
        df_3 = element_filter(df_2, options[colnum])
        options.remove(options[colnum])
    return df_3


def display_time_range(df):
    print('*' * 100)
    print(pd.Series(df.index).describe())
    print('*' * 100)


def time_range_selection(df):
    print('*' * 100)
    txt = "Date Range Selection"
    print('*' * 100)
    start_date = input(
        "Enter the starting date in the following format 'YYYY-MM-DD': ")
    print('\n')
    print(f"You entered: {start_date}")
    print('*' * 100)
    end_date = input(
        "Enter the ending date in the following format 'YYYY-MM-DD': ")
    print('\n')
    print(
        f"You entered: {end_date}, the date range is {start_date} - {end_date}")
    print('*' * 100)
    return df[start_date: end_date]


def time_period_filter(df):
    display_time_range(df)
    return time_range_selection(df)


def get_sampling_method():
    print('*' * 100)
    txt = "Sampling Method Selection"
    print(txt.center(90))
    print('*' * 100)
    return input("""
    How would you like to view the table:
    Enter 'Y' for by year,
    Enter 'M' for by month,
    Enter 'D' for by day
    """)


def get_agg_function():
    print('*' * 100)
    txt = 'Calculation Based on Sampling Method'
    print(txt.center(90))
    print('*' * 100)
    print('Here are the calculation options: ')
    print('\n')
    print(pd.DataFrame({'Calculation Method': [
          'Max Price', 'Min Price', 'Mean Price', 'Median Price']}))
    print('*' * 100)
    return int(input("How would you like view the pricing information(Enter a number please): "))


def time_based_filtering(df):
    agg_functions = ['max', 'min', 'mean', 'median']
    print('*' * 100)
    method = get_sampling_method().upper()
    print(f'Thanks, You entered: {method}')
    print('*' * 100)
    func = get_agg_function()
    print(f"Thanks! You chose: {agg_functions[func ]}")
    print('*' * 100)
    return df.resample(method).agg(agg_functions[func])


def get_month():
    ans_ls = []
    ans = 0
    while ans != 13:
        print('*' * 100)
        txt = 'Month Filter'
        print(txt.center(90))
        print('*' * 100)
        print(f'Month Selected so far: {ans_ls}')
        ans = int(
            input("Type the month you would like to select(type 13 to quit): "))
        print("*" * 100)
        if ans in range(1, 13):
            ans_ls.append(ans)
    return ans_ls


def get_month_df(df):
    ans_ls = get_month()
    return df[df.index.month.map(lambda x: x in ans_ls)]


def filter_all(df):
    ans = ""
    while True:
        print('*' * 100)
        txt = 'Filters Menu'
        print(txt.center(90))
        print('*' * 100)
        ans = int(input("""
        Select the type of filtering you would like,
        \n
        0 for criteria filters(Country/Grade),
        1 for time-based filter(by year/ by month/ by day),
        2 for time-period filter(by start date, end date),
        3 for month-based filter(same months in each year,)
        4 to proceed to the volitilty, delta calculations,
        5 to exit to main menu.
        \n
        """))
        print('*' * 100)
        print('\n')
        if ans == 0:
            print('\n')
            print('*' * 100)
            df = criteria_filters(df)
            print('*' * 100)
            print('\n')
        elif ans == 1:
            print('\n')
            print('*' * 100)
            df = time_based_filtering(df)
            print('*' * 100)
            print('\n')
        elif ans == 2:
            print('\n')
            print('*' * 100)
            df = time_period_filter(df)
            print('*' * 100)
            print('\n')
        elif ans == 3:
            print('\n')
            print('*' * 100)
            df = get_month_df(df)
            print('*' * 100)
            print('\n')
        elif ans == 4:
            return df
        elif ans == 5:
            return 5


def calculate_delta(df, num):
    print('Price Change')
    delta = df[['Average Selling Price']].dropna().diff(num)
    print(delta)
    print('Percentage Change')
    pct_change = (df[['Average Selling Price']].pct_change(num) * 100).round(2)
    print(pct_change)
    print('Price Change Graph')
    delta[['Average Selling Price']].plot()
    print("Percentage Change Graph")
    pct_change[['Average Selling Price']].plot()
    return delta, pct_change


def diff_operation(df):
    while True:
        print('*' * 100)
        txt = 'Delta Filters'
        txt.center(90)
        print('*' * 100)
        print('\n')
        print("Note: The following operation is only valid if you choose to view the table by month! ")
        print('\n')
        options = ['Monthly', 'Quaterly', 'Six Months']
        print(pd.DataFrame({'Delta Options': options}))
        ans = int(input("Please Enter the Corresponding number: "))
        if ans == 0:
            return calculate_delta(df, 1)
        elif ans == 1:
            return calculate_delta(df, 3)
        elif ans == 2:
            return calculate_delta(df, 6)
        else:
            print("Enter a valid number please")


def scenario_operations(df, month_list, criteria_dictionary):
    for key, value in criteria_dictionary.items():
        df_tmp = df[df[key] == value]
    df_tmp_months = df_tmp[df_tmp.index.month.map(lambda x: x in month_list)]
    print('\n')
    print("Choose a Grade")
    df_tmp_filtered = element_filter(df_tmp_months, 'Grade Desc')
    print('*' * 100)
    print('\n')
    txt1 = 'Volatility'
    print('*' * 100)
    txt1.center(90)
    print('*' * 100)
    print(df_tmp_filtered.std(skipna=True))
    print('*' * 100)
    txt2 = 'Monthly Delta'
    print('*' * 100)
    txt2.center(90)
    print('*' * 100)
    return df_tmp_filtered, diff_operation(df_tmp_filtered)


def get_criterias(df):
    print('\n')
    print('Here are the criterias: ')
    print('\n')
    colnames = list(df.columns)
    print(pd.DataFrame({"Criterias": colnames}))
    print('\n')
    print('*' * 100)
    colnum = int(
        input('Choose a Criteria to Select from(Only Allow One Criteria): '))
    colname_list = display_elements(df, colnames[colnum])
    print('*' * 100)
    element_num = get_inputs()
    print('*' * 100)
    element_name = colname_list[element_num]
    dict_value = {colnames[colnum]: colname_list[element_num]}
    return dict_value


def create_scenarios(df):
    sce_name = input("Enter a name to start creating the scenario: ")
    months_ls = get_month()
    dict_value = get_criterias(df)
    return sce_name, months_ls, dict_value


def scenarios_processing(df, scenarios_dc):
    while True:
        print('*' * 100)
        txt = 'Scenario Selection'
        print(txt.center(90))
        print('*' * 100)
        print('Here are the availiable scenarios')
        scenarios = list(scenarios_dc.keys())
        print(pd.DataFrame({'scenario list': scenarios}))
        print('*' * 100)
        print('*' * 100)
        ans = input("""
        You can either access the current scenario calculations or create custom scenarios
        Enter Y to create custom scenarios
        Enter N to access scenarios
        Enter Q to quit exit the current page
        """)
        if ans.upper() == 'Y':
            txt1 = 'Custom Scenario Creation'
            print('*' * 90)
            txt1.center(90)
            print('*' * 90)
            sce_name, months_ls, dict_value = create_scenarios(df)
            scenarios_dc[sce_name] = (months_ls, dict_value)
            print('*' * 100)
            print('Thank You! Will return to the Scenarios Page')
            print('*' * 100)
            continue
        elif ans.upper() == 'N':
            txt2 = 'Scenarios List'
            print('*' * 90)
            txt2.center(90)
            print('*' * 90)
            print('\n')
            sce = int(input("Choose the scenario you would like to do: "))
            print(pd.DataFrame({'scenario list': scenarios}))
            print('*' * 100)
            print('\n')
            print(f"Thank you! You chose: {scenarios[sce]}")
            df_tmp_filterd, deltas = scenario_operations(
                df, scenarios_dc[scenarios[sce]][0], scenarios_dc[scenarios[sce]][1])
            print('\n')
            print('*' * 100)
            df_tmp_filterd.to_excel(os.path.join(
                'project outputs', scenarios[sce]+'.xlsx'))
            deltas[0].to_excel(os.path.join(
                'project outputs', scenarios[sce]+' delta.xlsx'))
            deltas[1].to_excel(os.path.join(
                'project outputs', scenarios[sce]+' pct_change.xlsx'))
        elif ans.upper() == 'Q':
            break


def get_files():
    print('*' * 100)
    txt = 'PLESE SELECT AN EXCEL FILE TO PROCEED: '
    print(txt.center(90))
    print('*' * 100)
    file_ls = os.listdir()
    file_ls_xls = []
    for file in file_ls:
        if ('xlsx' in file):
            file_ls_xls.append(file)
    print(pd.DataFrame({"Files inside the directory": file_ls_xls}))
    try:
        dirnum = int(input(
            'Please input the number corresponding to the excel you want to open(Enter -1 to quit the program): '))
        if dirnum == -1:
            return ""
        df = pd.read_excel(file_ls_xls[dirnum], sheet_name=0, parse_dates=[
            'Calendar Year/Month'], index_col='Calendar Year/Month')
        return df
    except Exception as e:
        print('Please enter a valid file number')


def table_selection_interface(txt1):
    while True:
        print('*' * 100)
        print('*' * 100)
        print(txt1.center(90))
        print('*' * 100)
        print('*' * 100)
        print("""
        Hi, This program is calculates the deltas or the
        volitilites based on selected filters. Please choose the appropriate filters.
        """)
        df = get_files()
        if (isinstance(df, str)):
            quit()
        else:
            return df


def main_operation():
    sc_delta, sc_pct_change, delta, pct_change, df_1 = None, None, None, None, None
    scenarios_dc = {'Winter in China': ([11, 12, 1, 2], {'Region/Country': 'China'}),
                    'Summer in Middle East': ([6, 7, 8, 9], {'Super Region1 (Shpto': 'Middle East'}),
                    'Rainy Season in Vietnam': ([6, 7, 8, 9], {'Region/Country': 'Vietnam'})}
    txt = "Main Menu"
    txt1 = 'WELCOME!'
    df = table_selection_interface(txt1)
    while True:
        print('*' * 100)
        print(txt.center(90))
        print('*' * 100)
        ans1 = input("""
        What type of calculations would you like to perform?
        Enter Y to access scenarios,
        Enter N to access other calculation types
        Enter T to exit to Table Selection
        Enter Q to quit the program
        """)
        print('*' * 100)
        print('\n')
        if ans1.upper() == 'Y':
            scenarios_processing(df, scenarios_dc)
            continue
        elif ans1.upper() == 'N':
            df_1 = filter_all(df)
            if (isinstance(df_1, int)):
                continue
            while True:
                print('*' * 100)
                ans = int(input(
                    """
                    What operations would you like to perform:
                    1. Month-over-month delta
                    2. Volatility Calcualtion
                    3. Export filtered table to excel format
                    4. Exit to Main Menu
                    """))
                print('*' * 100)
                if ans == 1:
                    delta, pct_change = diff_operation(df_1)
                    delta.to_excel(os.path.join('project outputs', datetime.fromtimestamp(
                        time.time()).strftime('%Y-%m-%d %H:%M:%S')+' delta.xlsx'))
                    pct_change.to_excel(os.path.join('project outputs', datetime.fromtimestamp(
                        time.time()).strftime('%Y-%m-%d %H:%M:%S')+' pct_change.xlsx'))
                elif ans == 2:
                    df_std = df_1.std(skipna=True)
                    print(df_std)
                    df_std.to_excel(os.path.join('project outputs', datetime.fromtimestamp(
                        time.time()).strftime('%Y-%m-%d %H:%M:%S')+' volatility.xlsx'))
                elif ans == 3:
                    df_1.to_excel(os.path.join('project outputs', datetime.fromtimestamp(
                        time.time()).strftime('%Y-%m-%d %H:%M:%S')+' filtered.xlsx'))
                elif ans == 4:
                    break
        elif ans1.upper() == 'T':
            df = table_selection_interface(txt1)
        elif ans1.upper() == 'Q':
            quit()
