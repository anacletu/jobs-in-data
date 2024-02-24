import os
import platform

from classes import VanillaPythonAnalysis
from functions import *


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
                country = input("Type the desired country: ").title().strip()
                country_info = get_country_info(data_obj, country)
                if country_info is not None:
                    download_data = input(
                        "Would like to export the data for this country? Type 'yes' or press Enter to continue: "
                    )
                    if download_data:
                        export_country_data(country_info, download_data, country)
            case 5:
                group_by_job_category(data_obj)
            case 6:
                country = input("Type the desired country: ").title().strip()
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
                vanilla_analyzer = VanillaPythonAnalysis(file_path)
                vanilla_analyzer.get_insights()
            case 9:
                removed, data_obj = restore_dateset(removed, data_obj, df)
            case _:
                break
        input("\nPress Enter to continue...\n")


if __name__ == "__main__":
    main()
