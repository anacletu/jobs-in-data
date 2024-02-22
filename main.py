import csv
import locale
import os
import platform
import requests

import pandas as pd
from tabulate import tabulate
from forex_python.converter import CurrencyRates


locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
c = CurrencyRates()


def main():
    df = get_data_pd()
    data_obj = treat_axis(df)
    removed = False  # boolean to control if the outliers have been removed or not

    while True:
        if platform.system() == "Windows":
            os.system("cls")
        else:
            os.system(
                "clear"
            )  # clear the terminal screen after each action from the user, making the visualization more pleasant

        action_to_perform = get_user_input()
        match action_to_perform:
            case 1:
                get_total_lines(data_obj, removed)
            case 2:
                get_average_salary(data_obj)
            case 3:
                get_average_salary_by_country(data_obj)
            case 4:
                country = input("Type the desired country: ")
                get_country_info(data_obj, country)
            case 5:
                group_by_job_category(data_obj)
            case 6:
                country = input("Type the desired country: ")
                get_country_summary(data_obj, country)
            case 7:
                if not removed:
                    z_score_default = 3
                    z_score_from_user = input(
                        f"Inform the desired threshold for the Z-score method (default is {z_score_default}): "
                    )
                    try:
                        z_score_from_user = float(z_score_from_user)
                    except ValueError:
                        print("Invalid input. Using default value.")
                        z_score_from_user = z_score_default
                    rmv_outliers, outliers = detect_outliers(
                        data_obj, z_score_from_user
                    )
                    if rmv_outliers is not None:
                        removed, data_obj = remove_outliers(
                            rmv_outliers, data_obj, outliers
                        )
                else:
                    print("Outliers already removed.")
            case 8:
                vanilla_analyzer = VanillaPythonAnalysis("db/jobs_in_data.csv")
                vanilla_analyzer.get_insights()
            case 9:
                removed, data_obj = restore_dateset(removed, data_obj, df)
            case _:
                break
        input("\nPress Enter to continue...\n")


def get_total_lines(data, removed=False):
    """
    This function calls different ways to open a db for demonstration purposes
    and prints the total number of lines in the csv file
    args: removed (bool) - if the outliers have been removed or not (yet)
    """

    if not removed:
        # using the built-in file reading function to read the data
        data_file = get_data_file()
        total_lines = len(data_file)

        print("\n************")
        print(
            f"Total number of lines: {total_lines} using file reading function - this method counts the header as a line"
        )

        # using the built-in csv library to read the data
        data_list = get_data_csv()
        total_lines = len(data_list)

        print("************")
        print(f"Total number of lines: {total_lines} using CSV library")
        print("************")

    else:
        # using Pandas to read the data
        total_lines = data.shape[0]

        print("\n************")
        print(f"Total number of lines: {total_lines} using Pandas")
        print("************")


def get_data_pd():
    """
    This function reads the data from the jobs_in_data.csv file
    and returns it as a DataFrame
    """
    try:
        data = pd.read_csv("db/jobs_in_data.csv")
    except FileNotFoundError:
        print("File not found.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    else:
        return data


def get_data_file():
    """
    This function reads the data from the
    jobs_in_data.csv file and returns it as a list
    """
    try:
        with open("db/jobs_in_data.csv", "r") as file:
            data = file.readlines()
    except FileNotFoundError:
        print("File not found.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    else:
        return data


def get_data_csv():
    """
    This function reads the data from the jobs_in_data.csv
    file and returns it as a list of dictionaries
    """
    try:
        with open("db/jobs_in_data.csv", "r") as file:
            data = list(csv.DictReader(file))
    except FileNotFoundError:
        print("File not found.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    else:
        return data


def treat_axis(data):
    """
    This function is responsible for making the data more readable
    by renaming and removing some columns from the dataset
    args: data (DataFrame)
    """
    new_data = data.copy()
    try:
        remove_cols = [
            "work_year",
            "job_title",
            "salary_currency",
            "salary",
            "company_size",
        ]
        new_data.drop(columns=remove_cols, inplace=True)

        new_data.rename(
            columns={
                "job_category": "Job category",
                "employee_residence": "Country",
                "experience_level": "Experience level",
                "employment_type": "Employment type",
                "work_setting": "Work setting",
                "company_location": "Company location",
                "salary_in_usd": "Salary in USD",
            },
            inplace=True,
        )
    except:
        print("Failed to treat the data.")
        return None
    else:
        return new_data


def get_user_input():
    """
    This function gets the user input for a specific action
    """
    options_for_the_user = [
        "1. Check the total number of lines in the file",
        "2. Check the global average salary in USD",
        "3. Check the average salary by country",
        "4. Type a country to see all available data",
        "5. Filter data by job category and country",
        "6. Type a country to see a summary of the data",
        "7. Detect outliers using Z-score method",
        "8. Check some general insights from the data",
        "9. Restore the original data with the outliers",
        "0. Exit program",
    ]
    options = "\n".join(options_for_the_user)
    user_action = input(
        f"What would you like to do? Type the corresponding number: \n\n{options}\n"
    )
    try:
        action = int(user_action)
    except ValueError:
        print("Invalid choice.")
        return get_user_input()
    else:
        if action in range(0, len(options_for_the_user)):
            return action
        else:
            print("Invalid choice.")
            return get_user_input()


def get_average_salary(data):
    """
    This function calculates the average salary in USD
    args: data (DataFrame)
    """
    try:
        average_salary = data["Salary in USD"].mean()
    except KeyError:
        print("Data not found.")
        return
    else:
        formatted_salary = format_currency(average_salary)
        print(f"\nThe average salary in USD is: {formatted_salary} per year.")


def get_average_salary_by_country(data):
    """
    This function calculates the average salary by country
    and the percentage variation compared to the global mean salary
    args: data (DataFrame)
    """
    try:
        overall_mean_salary = data["Salary in USD"].mean()
        average_salary_by_country = data.groupby("Country")["Salary in USD"].mean()
    except KeyError:
        print("Data not found.")
        return
    else:
        formatted_data = []
        for country, salary in average_salary_by_country.items():
            variation_in_percentage = (
                (salary - overall_mean_salary) / overall_mean_salary
            ) * 100
            formatted_salary = format_currency(
                salary
            )  # formattig 'on the fly' prevents issues with other calculations
            formatted_data.append(
                {
                    "Country": country,
                    "Average Salary": formatted_salary,
                    "Variation from global mean(%)": f"{variation_in_percentage:.2f}",
                }
            )
        print(tabulate(formatted_data, headers="keys", tablefmt="pretty"))


def group_by_job_category(data):
    """
    This function groups the data by job category
    args: data (DataFrame)
    """
    try:
        grouped_data = (
            data.groupby(["Country", "Job category"])["Salary in USD"]
            .mean()
            .reset_index()
        )
    except:
        print("Failed to group the data.")
        return
    else:
        grouped_data["Salary in USD"] = grouped_data["Salary in USD"].apply(
            format_currency
        )
        print(tabulate(grouped_data, headers="keys", tablefmt="pretty"))
        filter_country = input(
            "\nIf you want to isolate one country, specify it. Else press Enter to continue.\n"
        )
        if filter_country:
            filtered_data = grouped_data.loc[grouped_data["Country"] == filter_country]
            if filtered_data.empty:
                print("Country not found.")
            else:
                print(tabulate(filtered_data, headers="keys", tablefmt="pretty"))
                return


def get_country_info(data, country):
    """
    This function gets the information of a specific country
    args: data (DataFrame), country (str)
    """
    try:
        country_info = data[data["Country"] == country].copy()
    except KeyError:
        print("Country not found.")
        return
    else:
        if country_info.empty:
            print(f"No data found for {country}.")
            return

        # Format the salary as currency
        country_info["Salary in USD"] = country_info["Salary in USD"].apply(
            format_currency
        )

        print(tabulate(country_info, headers="keys", tablefmt="pretty"))


def get_country_summary(data, country, currency="USD"):
    """
    This function gets the summary of a specific country.
    In addition, it allows the user to convert the currency as requested.
    It is a long function, but it serves the purpose of showing the data in a more organized way.
    args: data (DataFrame), country (str), currency (str)
    """
    try:
        country_info = data[
            data["Country"] == country
        ].copy()  # using the copy method in case the user wants to convert the currency (keeping the original data intact)
    except KeyError:
        print("Country not found.")
        return
    else:
        if country_info.empty:
            print(f"No data found for {country}.")
            return
        if currency != "USD":
            try:
                country_info["Salary in USD"] = country_info["Salary in USD"].apply(
                    lambda s: c.convert("USD", currency, s)
                )
            except:
                try:
                    country_info["Salary in USD"] = country_info["Salary in USD"].apply(
                        lambda x: convert_currency("USD", currency, x)
                    )  # plan B in case python-forex is not working, it goes offline sometimes
                except:
                    print("Error converting currency")
                    return

        average_salary = country_info["Salary in USD"].mean()
        number_of_responses = country_info.shape[0]
        most_common_job = country_info["Job category"].mode().values[0]
        highest_salary = country_info["Salary in USD"].max()
        lowest_salary = country_info["Salary in USD"].min()
        most_common_emp_type = country_info["Employment type"].mode().values[0]

        summary = {
            "Country": country,
            "Average Salary": format_currency(average_salary, currency),
            "Number of Responses": number_of_responses,
            "Most Common Job": most_common_job,
            "Highest Salary": format_currency(highest_salary, currency),
            "Lowest Salary": format_currency(lowest_salary, currency),
            "Most Common Employment Type": most_common_emp_type,
        }
        print(tabulate([summary], headers="keys", tablefmt="pretty"))

        other_currency = input(
            "\nIf you want to see the information in another currency, type the proper abbreviation (e.g. EUR) else press Enter.\n"
        )
        if other_currency:
            get_country_summary(data, country, other_currency)


def convert_currency(base, target, amount):
    """
    This function converts the currency using the forex-python library
    args: base (str), target (str), amount (float)
    """
    url = "https://api.exchangerate-api.com/v4/latest/" + base
    api_response = requests.get(url)
    data = api_response.json()
    return amount * data["rates"][target]


def format_currency(amount, currency="USD"):
    """
    Function to format salary as currency
    args: amount (float), currency (str)
    """
    if currency == "USD":
        return locale.currency(amount, grouping=True, symbol=True)
    else:
        return "{:,.2f} {}".format(amount, currency)


def detect_outliers(data, threshold=3):
    """
    This function checks for outliers in the data using Z-score method.
    The threshold is set to 3 by default as per 'empirical rule':
    https://en.wikipedia.org/wiki/68%E2%80%9395%E2%80%9399.7_rule for more info
    args: data (DataFrame), threshold (int)
    """
    try:
        z_scores = data["Salary in USD"].apply(
            lambda x: (x - data["Salary in USD"].mean()) / data["Salary in USD"].std()
        )
        outliers = data[abs(z_scores) > threshold].copy()
        outliers["Salary in USD"] = outliers["Salary in USD"].apply(format_currency)
    except:
        print("Failed to check for outliers.")
        return None, None
    else:
        print(tabulate(outliers, headers="keys", tablefmt="pretty"))
        print(f"\nTotal number of outliers: {outliers.shape[0]}\n")
        if outliers.empty:
            print("No outliers found.")
            return None, None
        else:
            print(f"Do you want to remove the outliers from the dataset?")
            return (input("Type 'yes' or 'no': ").lower().strip(), outliers)


def remove_outliers(rmv_outliers, data, outliers=None, removed=False):
    """
    This function removes the outliers from the dataset
    as per the user's request
    args: rmv_outliers (str), data (DataFrame), outliers (DataFrame), removed (bool)
    """
    if rmv_outliers in [
        "yes",
        "y",
        "yeah",
        "yep",
        "sure",
        "ok",
    ]:  # trying to catch some misspelling before returning as invalid input
        confirmation = input(
            "\nAre you sure you want to remove the outliers from the dataset? Type 'yes' or 'no': "
        )
        if confirmation.lower().strip() in ["yes", "y", "yeah", "yep", "sure", "ok"]:
            filtered_data = data[~data.index.isin(outliers.index)]
            print("\nOutliers removed.")
            removed = True
            return removed, filtered_data
        else:
            print("\nOutliers not removed.")
            return removed, data
    elif rmv_outliers in ["no", "n", "nope"]:
        print("\nOutliers not removed.")
        return removed, data
    else:
        print("\nInvalid input. Outliers not removed.")
        return removed, data


def restore_dateset(removed, data, dataframe):
    """
    This function restores the original dataset
    args: removed (boolean), data (DataFrame), dataframe (DataFrame) - original
    """
    if not removed:
        print("No changes were made to the dataset.")
    else:
        ans = input(
            "Are you sure you want to restore the original data? Type 'yes' to confirm or Enter to continue. "
        )
        if ans in ["yes", "y", "yeah", "sure"]:
            removed = False
            data = treat_axis(dataframe)
            print("Original data restored.")
        else:
            print("No changes were made to the dataset.")

    return removed, data


class VanillaPythonAnalysis:
    def __init__(self, file_path):
        self.data = self.read_data(file_path)
        self.salaries = [float(item.get("salary_in_usd", 0)) for item in self.data]
        self.job_categories = [
            item.get("job_category", "Not Available") for item in self.data
        ]
        self.countries = [
            item.get("employee_residence", "Not Available") for item in self.data
        ]
        self.years = [int(item.get("work_year", 0)) for item in self.data]

    def read_data(self, file_path):
        with open(file_path, "r") as file:
            data = list(csv.DictReader(file))
        return data

    def get_average_salary(self):
        average_salary = sum(self.salaries) / len(self.salaries)
        return average_salary

    def get_salary_deviaton(self):
        average_salary = self.get_average_salary()
        salary_deviation = [salary - average_salary for salary in self.salaries]
        deviation_squared = [dev**2 for dev in salary_deviation]
        deviation_squared_mean = sum(deviation_squared) / len(deviation_squared)
        std_dev_salaty = deviation_squared_mean**0.5
        return std_dev_salaty

    def get_years_deviaton(self):
        mean_years = sum(self.years) / len(self.years)
        years_deviation = [year - mean_years for year in self.years]
        deviation_squared = [dev**2 for dev in years_deviation]
        deviation_squared_mean = sum(deviation_squared) / len(deviation_squared)
        std_dev_years = deviation_squared_mean**0.5
        return std_dev_years, mean_years

    def get_job_category_frequency(self):
        frequency = {}
        for category in self.job_categories:
            frequency[category] = frequency.get(category, 0) + 1
        return sorted(frequency.items(), key=lambda x: x[1], reverse=True)

    def get_correlation_salary_years(self):
        mean_salary = self.get_average_salary()
        salary_deviation = self.get_salary_deviaton()
        work_years_deviation, mean_years = self.get_years_deviaton()

        covariance = sum(
            (year - mean_years) * (salary - mean_salary)
            for year, salary in zip(self.years, self.salaries)
        ) / len(self.years)

        correlation = covariance / (work_years_deviation * salary_deviation)
        return correlation

    def get_tendency_per_year(self):
        salary_by_year = {}
        for year, salary in zip(self.years, self.salaries):
            salary_by_year[year] = salary_by_year.get(year, []) + [salary]
        average_salary_by_year = {
            year: sum(salaries) / len(salaries)
            for year, salaries in salary_by_year.items()
        }
        return sorted(average_salary_by_year.items())

    def get_lowest_salary(self):
        lowest_salary = min(self.salaries)
        return lowest_salary

    def get_highest_salary(self):
        highest_salary = max(self.salaries)
        return highest_salary

    def get_insights(self):
        print("\n===================== Salary Analysis =====================\n")
        salary_mean = self.get_average_salary()
        std_dev_salary = self.get_salary_deviaton()
        print(f"Global Salary Mean: ${salary_mean:,.2f}")
        print(f"Salary Standard Deviation: ${std_dev_salary:,.2f}\n")
        print(
            f"A standard deviation of ${std_dev_salary:,.2f} is relatively high, indicating a large variation in wages."
        )
        print(
            f"In other words, although the average salary is ${salary_mean:,.2f}, many employees earn significantly more or less than this amount."
        )
        print("\n===========================================================\n")

        print("\n==================== Frequency Analysis ====================\n")
        frequency = self.get_job_category_frequency()
        for category, count in frequency:
            print(f"Category: {category}, Count: {count}")
        print(
            "\nThis analysis shows the count for each job category in the data source."
        )
        print("This number illustrates how common a job category is.")
        print("\n============================================================\n")

        print("\n=================== Correlation Analysis ===================\n")
        correlation = self.get_correlation_salary_years()
        print(f"Correlation between work years and salary: {correlation:.2f}\n")
        print("Values close to 1 or -1 indicate a strong correlation.")
        if correlation > 0:
            print(
                "A positive correlation suggests that salary and years tend to move in the same direction."
            )
        elif correlation < 0:
            print(
                "A negative correlation suggests that salary tends to move in the opposite direction of years."
            )
        print("\n============================================================\n")

        print("\n==================== Tendency Over Time ====================\n")
        tendency = self.get_tendency_per_year()
        for year, avg_salary in tendency:
            print(f"Year: {year}, Average Salary: ${avg_salary:,.2f}")
        print("\nThis analysis shows the overall behavior of the salaries.")
        print("This is an important information to side with the above correlation.")
        print("\n============================================================\n")

        print("\n======================= Salary Range =======================\n")
        lowest_salary = self.get_lowest_salary()
        highest_salary = self.get_highest_salary()
        print(f"Lowest Salary: ${lowest_salary:,.2f}")
        print(f"Highest Salary: ${highest_salary:,.2f}\n")
        print("This range shows the spread of salaries in the dataset.")
        print("The lowest salary is the minimum amount earned by an employee.")
        print("The highest salary is the maximum amount earned by an employee.")
        print("\n============================================================\n")


if __name__ == "__main__":
    main()
