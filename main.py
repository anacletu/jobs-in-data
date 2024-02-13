import csv
import locale
import pandas as pd
import os
from forex_python.converter import CurrencyRates
from tabulate import tabulate

locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
c = CurrencyRates()


def main():
    # using the built-in file reading function to read the data
    data_file = get_data_file()
    total_lines = len(data_file)
    
    print("\n************")
    print(f"Total number of lines: {total_lines} using file reading function - this method counts the header as a line")
    
    
    # using the pandas library to read the data (installation required: pip install pandas)
    data_obj = get_data_pd()
    total_lines = data_obj.shape[0]

    print("************")
    print(f"Total number of lines: {total_lines} using pandas")

    # using the built-in csv library to read the data
    data_list = get_data_csv()
    total_lines = len(data_list)

    print("************")
    print(f"Total number of lines: {total_lines} using csv library")
    print("************\n")

    # treating the data
    data_obj = treat_data(data_obj)
    
    while True:
        action_to_perform = get_user_input()
        if action_to_perform == 1:
            get_average_salary(data_obj)
        elif action_to_perform == 2:
            get_average_salary_by_country(data_obj)
        elif action_to_perform == 3:
            country = input("Type the desired country: ")
            get_country_info(data_obj, country)
        elif action_to_perform == 4:
            country = input("Type the desired country: ")
            get_country_summary(data_obj, country)
        else:
            break
        input("Press Enter to continue...\n")
        
        os.system("clear") # clear the terminal screen

def get_data_pd():
    """
    This function reads the data from the jobs_in_data.csv file and returns it as a pandas dataframe
    """
    try:
        data = pd.read_csv("db/jobs_in_data.csv")
        return data
    except FileNotFoundError:
        print("File not found.")
        return None
    except pd.errors.ParserError:
        print("Error parsing CSV file.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def get_data_file():
    """
    This function reads the data from the jobs_in_data.csv file and returns it as a list
    """
    try:
        with open("db/jobs_in_data.csv", "r") as file:
            data = file.readlines()
        return data
    except FileNotFoundError:
        print("File not found.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def get_data_csv():
    """
    This function reads the data from the jobs_in_data.csv file and returns it as a list of dictionaries
    """
    try:
        with open("db/jobs_in_data.csv", "r") as file:
            data = list(csv.DictReader(file))
        return data
    except FileNotFoundError:
        print("File not found.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def treat_data(data):
    """
    This function treats the data, removing any unnecessary columns and renaming the columns
    """
    try:
        columns_to_remove = ["work_year", "job_title", "salary_currency", "company_size"]
        data.drop(columns=columns_to_remove, inplace=True)

        data.rename(columns={"job_category": "Job category",
                             "employee_residence": "Country", 
                             "experience_level": "Experience level", 
                             "employment_type": "Employment type", 
                             "work_setting": "Work setting", 
                             "company_location": "Company location", 
                             "salary_in_usd": "Salary in USD", 
                             "salary": "Salary in local currency"}, inplace=True)
                                      
        return data  # Return the modified DataFrame
        
    except KeyError as e:
        print(f"Error: {e}. One or more columns to remove or rename were not found.")
        return None
    except Exception as e:
        print(f"Error: {e}. Failed to treat the data.")
        return None


def get_user_input():
    """
    This function gets the user input for a specific action
    """
    options = [
        "1. Check the global average salary in USD",
        "2. Check the average salary by country",
        "3. Type a country to see all available data",
        "4. Type a country to see a summary of the data",
        "5. Exit",
    ]  # future actions will be added here
    options_text = "\n".join(options)
    action = input(f"Type the number of the desired action: \n\n{options_text}\n")
    try:
        action = int(action)
        if action in range(1, len(options) + 1):
            return action
        else:
            print("Invalid action.")
            return get_user_input()

    except ValueError:
        print("Invalid action.")
        return get_user_input()


def get_average_salary(data):
    """
    This function calculates the average salary in USD
    """
    try:
        average_salary = data["Salary in USD"].mean()
    except KeyError:
        print("Salary in USD column not found.")
    except Exception as e:
        print(f"Error: {e}")
    else:
        formatted_salary = format_currency(average_salary)
        print(f"\nThe average salary in USD is: {formatted_salary} per year.\n")


def get_average_salary_by_country(data):
    """
    This function calculates the average salary by country
    """
    formatted_data = []
    try:
        average_salary_by_country = data.groupby("Country")[
            "Salary in USD"
        ].mean()
    except KeyError:
        print("Column data not found.")
    except Exception as e:
        print(f"Error: {e}")
    else:
        for country, salary in average_salary_by_country.items():
            formatted_salary = format_currency(salary)
            formatted_data.append(
                {"Country": country, "Average Salary": formatted_salary}
            )
        print(tabulate(formatted_data, headers="keys", tablefmt="pretty"))


def get_country_info(data, country):
    """
    This function gets the information of a specific country
    """
    try:
        country_info = data[data["Country"] == country].copy()
    except KeyError:
        print("Country not found.")
    except Exception as e:
        print(f"Error: {e}")
    else:
        if country_info.empty:
            print(f"No data found for {country}.")
            return
        
        # Format as currency
        country_info["Salary in USD"] = country_info["Salary in USD"].apply(format_currency)
        country_info["Salary in local currency"] = country_info["Salary in local currency"].apply(format_currency)
        
        print(tabulate(country_info, headers="keys", tablefmt="pretty"))


def get_country_summary(data, country, currency="USD"):
    """
    This function gets the summary of a specific country
    """
    try:
        country_info = data[data["Country"] == country].copy()
    except KeyError:
        print("Country not found.")
    except Exception as e:
        print(f"Error: {e}")
    else:
        if country_info.empty:
            print(f"No data found for {country}.")
            return
        if currency != "USD":
            try:
                country_info["Salary in USD"] = country_info["Salary in USD"].apply(
                lambda x: c.convert("USD", currency, x)
                )
            except Exception as e:
                print(f"Error converting currency: {e}")
                return
        
        average_salary = country_info["Salary in USD"].mean()
        number_of_responses = country_info.shape[0]
        
        summary = {
            "Country": country,
            "Average Salary": format_currency(average_salary, currency),
            "Number of Responses": number_of_responses,
        }
        print(tabulate([summary], headers="keys", tablefmt="pretty"))

        next_currency = input("\nIf you want to see the information in another currency, type the proper abbreviation (e.g. EUR) else type Enter.\n")
        if next_currency:
            get_country_summary(data, country, next_currency)


def format_currency(amount, currency="USD"):
    """
    Function to format salary as currency
    """
    if currency == "USD":
        return locale.currency(amount, grouping=True, symbol=True)
    else:
        return "{:,.2f} {}".format(amount, currency)


if __name__ == "__main__":
    main()
