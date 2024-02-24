# Jobs in Data - A Brief Analysis

## Table of Contents
1. [Introduction](#introduction)
2. [Data Processing](#data-processing)
3. [Features](#features)
4. [Installation](#installation-instructions)
5. [Testing](#testing)
6. [License](#license)
7. [Acknowledgments](#acknowledgments)

## Introduction
This repository contains a Python application developed as part of the 'Fundamentals of Computing' course's final assignment in my pursuit of an MS in CS. The project aims to analyze a dataset related to jobs in the field of data science, extracting insights such as salary trends, job frequency, and correlations between variables. The application utilizes both built-in Python tools and external libraries to improve programming flexibility and facilitate result comparison, which can be achieved by running the included test file.

![Program Gif](/app/screenshot/app.gif)

## Data Processing
The main objective of this project is to process data from a csv file containing job-related information. The data processing pipeline involves several steps:

- **Data Retrieval**: The project retrieves the job data from a csv file using various methods including built-in file reading, pandas library, and csv library.
- **Data Treatment**: After retrieving the data, the following actions are taken:
    - Unnecessary columns are removed.
    - Remaining columns are renamed for clarity and consistency.
- **Data Analysis**: The processed data is then analyzed to extract various insights, including:
    - Average salary
    - Standard deviation of salaries
    - Frequency of job categories
    - Trends over time
    - Correlation between salary and years of experience
    - Identification of outliers
    - Percentage comparison between country averages and the global mean
    - Country-specific information

### Reasoning
Engaging in data analysis provides invaluable educational insights into prevalent job trends, salary distributions, and other essential facets within the computing domain. Through this process, learners gain practical experience in uncovering patterns, exploring trends, and discerning correlations, all of which are fundamental skills in the realm of data science and analysis. While the dataset itself may not offer significant real-world relevance, the exercise serves as a vital educational example, illustrating the importance of data analysis in informing decision-making and fostering a deeper understanding of complex datasets.

## Features
- **Data Visualization**: The application provides interactive visualizations to help users better understand the dataset. Users can choose from various visualization options, which are displayed with the support of the tabulate library.
- **Currency Conversion**: The application supports real-time currency conversion for salary data. Users can select their preferred currency, and the application will convert salary values accordingly. For reliability and redundancy, two conversion methods were implemented: Exchange Rate API and forex-python lib.
- **Export Capabilities**: Users can export results to a csv file for further analysis or reporting purposes.
- **User Interaction**: The application offers a CLI interface with prompts and menus to guide users through the process. Users can select analysis options and filter data. For improved visibility, the terminal window is refreshed with each interaction.
- **Error Handling**: The application includes robust error handling to ensure smooth operation even in the face of unexpected input or errors.
- **Modular Design**: The codebase is modular and well-organized, making it easy to maintain, extend, and debug. Each functionality is encapsulated in separate modules or classes, promoting code reusability and scalability.
- **Unit Testing**: The project includes comprehensive unit tests to verify the correctness of key functions and ensure reliable performance. Testing is automated using pytest, allowing for efficient regression testing and code validation.
- **Documentation**: The codebase is documented with inline comments and docstrings, providing insights into the functionality of each module, class, and function.

## Installation Instructions
To run this project, you'll need Python 3.10 or above installed on your machine. You can install the required dependencies using pip:

```bash
pip install pandas tabulate forex-python requests
```

Additionally, you might want to install the following to be able to run the test file:

```bash
pip install pytest numpy
```

### Dependencies
As mentioned above, the project relies on some libraries to run. An alternative approach is to create and activate a virtual environment, as below, that will install in isolation and automatically the dependencies listed in the requirements.txt file.

\- Open your terminal or command prompt.<br>
\- Navigate to the directory where you want to create the virtual environment.<br>
\- Run the following command to create a virtual environment named env:
```bash
python3 -m venv env
```

\- Then, activate by (Linux and macOS):
```bash
source env/bin/activate
```
Windows:
```
env\Scripts\activate
```

\- Install the dependencies:
```bash
pip install -r requirements.txt
```

\- When done, run:
```bash
deactivate
```

## Testing
This project includes a file for automated tests to ensure its functionality remains intact. To run the tests, follow these steps:

1. Make sure you have all the necessary dependencies installed.
2. Navigate to the project directory in your terminal or command prompt.
3. Run the following command to execute the test suite:

```bash
pytest test_main.py
```

The tests should pass without errors if no changes are made to the code.

## License
This repository is licensed under the [MIT License](LICENSE).

## Acknowledgments
- University of Abertay, Dundee, and the faculty for providing the educational resources and support.
- Kaggle for providing the dataset used in this project: [Jobs in Data](https://www.kaggle.com/datasets/hummaamqaasim/jobs-in-data).