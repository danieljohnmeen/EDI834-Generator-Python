# MSSQL to EDI 834 Converter for Blue Cross Blue Shield Carriers

This project involves converting records from a MySQL database to the EDI 834 format, specifically tailored for Blue Cross Blue Shield carriers and CIGNA.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
  
## Prerequisites

- Python 3.x
- A MSSQL server

## Configuration

1. **Constants Configuration**: 

    Before you run the application, it's essential to set up the required constants in the `constants.py` file.

    - **MySQL Database Details**: Define all necessary MySQL database connection details.
    - **Column Fields**: Specify the column fields required for the conversion.
    - **SSH Keys**: If applicable, set up your SSH key details.
    - ... (Include any other constants that the user needs to define.)

2. Any other configurations that the user needs to know about should be outlined here.

## Usage

To run the application:

```
python main_with_json.py

```