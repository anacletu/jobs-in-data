import csv


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
