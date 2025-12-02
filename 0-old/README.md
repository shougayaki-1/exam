# Exam Portal

This project is an interactive exam portal designed to facilitate various subject tests, including Math, Chemistry, Earth Science, and Language. The portal allows users to take tests based on questions stored in CSV or JSON formats.

## Project Structure

The project is organized as follows:

```
exam-portal
├── 202509
│   ├── index.html          # Main entry point for the exam portal
│   ├── math.html           # Math test page
│   ├── chemistry.html      # Chemistry test page
│   ├── earth.html          # Earth science test page
│   ├── language.html       # Language test page
│   ├── assets
│   │   └── style.css       # CSS styles for the exam portal
│   ├── data
│   │   ├── math.csv        # Questions and answers for the math test in CSV format
│   │   ├── chemistry.csv    # Questions and answers for the chemistry test in CSV format
│   │   ├── earth.csv       # Questions and answers for the earth science test in CSV format
│   │   ├── language.csv     # Questions and answers for the language test in CSV format
│   │   ├── math.json       # Questions and answers for the math test in JSON format
│   │   ├── chemistry.json    # Questions and answers for the chemistry test in JSON format
│   │   ├── earth.json      # Questions and answers for the earth science test in JSON format
│   │   ├── language.json     # Questions and answers for the language test in JSON format
│   │   └── convert_csv_to_json.py  # Python script to convert CSV files to JSON format
│   └── js
│       ├── main.js         # Main logic for loading test data and rendering questions
│       └── csv_to_json.js  # Functions to handle CSV data and convert to JSON
├── README.md                # Documentation for the project
```

## Setup Instructions

1. **Clone the Repository**: 
   Clone this repository to your local machine using:
   ```
   git clone <repository-url>
   ```

2. **Navigate to the Project Directory**:
   ```
   cd exam-portal
   ```

3. **Open the Project in a Web Browser**:
   Open `202509/index.html` in your preferred web browser to access the exam portal.

4. **Data Files**:
   The project includes CSV files for each subject. You can also find corresponding JSON files that can be used interchangeably. 

5. **Convert CSV to JSON**:
   If you need to convert CSV files to JSON format, run the Python script located in `202509/data/convert_csv_to_json.py`. Ensure you have Python installed on your machine.

## Usage

- Navigate to the main page to select a subject test.
- The test pages will load questions from either the CSV or JSON files.
- Follow the on-screen instructions to complete the tests.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.