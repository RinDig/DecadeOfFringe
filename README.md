# Edinburgh Fringe Festival Venue Accessibility Dashboard

## Overview

This interactive web application provides a dashboard to visualize the accessibility of venues participating in the Edinburgh Fringe Festival over different years. It uses a map-based interface with filtering options and a traffic light color system (Green: High, Orange: Medium, Red: Low) to represent accessibility levels.

![image](https://github.com/user-attachments/assets/052a0f22-4df7-4897-ad92-603bb6999046)


## Features

*   **Interactive Map:** Displays venues on an Edinburgh map (using OpenStreetMap).
*   **Traffic Light Colors:** Venue markers are colored based on their accessibility level:
    *   Green: High Accessibility
    *   Orange: Medium Accessibility
    *   Red: Low Accessibility
*   **Filtering:** Filter venues by:
    *   Year(s)
    *   Venue Address(es)
    *   Accessibility Level(s)
    ![image](https://github.com/user-attachments/assets/36e6b819-aa98-4439-8640-cc3d82d309fd)

*   **Hover Information:** Hover over a venue marker to see details:
    *   Venue Name
    *   Year
    *   Number of Performances
    *   Accessibility Level
    *   Accessibility Details (truncated if long)
  ![image](https://github.com/user-attachments/assets/d35df83f-9fdf-4766-8b33-6a9fed414d4f)

*   **Summary Statistics:** Displays the total number of filtered venues and the count for each accessibility category (High, Medium, Low).
![image](https://github.com/user-attachments/assets/1fc21670-2755-497f-90b7-c8bc4d3e855e)

## Data Source

The application currently uses the following file, which should be in the same directory as `app.py`:

*   `FringeDataCombined.xlsx`: An Excel file containing venue information, including address, latitude, longitude, year, number of performances, accessibility level, and detailed accessibility descriptions.

**Data Cleaning Steps (within `app.py`):**
1.  Loads the Excel file.
2.  Converts the 'Year' column to numeric, handling errors.
3.  Drops rows with missing 'Latitude', 'Longitude', or 'Year'.
4.  Determines the appropriate traffic light color ('access_color') based on the 'Accessibility level' column.

## Setup

1.  **Clone the repository or download the files.**
2.  **Ensure you have Python installed.** (Version 3.6+ recommended)
3.  **Create a virtual environment (optional but recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
4.  **Install the required Python libraries:**
    ```bash
    pip install dash pandas plotly openpyxl
    ```
    *(Note: `openpyxl` is needed by pandas to read `.xlsx` files)*
5.  **Place the `FringeDataCombined.xlsx` file in the same directory as `app.py`.**

## Running the Application

1.  Navigate to the project directory in your terminal.
2.  Run the Dash application script:
    ```bash
    python app.py
    ```
3.  The terminal will output messages including `Loading data...` and `Starting server...`.
4.  Open your web browser and go to the address provided (usually `http://127.0.0.1:8050/`).

## Potential Future Enhancements

*   **Performance Names:** Integrate performance names from additional data sources into the hover information or a separate details panel (would require providing a combined data file).
*   **Click Interaction:** Allow users to click on a venue marker to see more detailed information in a sidebar or modal window.
*   **Advanced Filtering:** Add more complex filtering options (e.g., filtering by specific accessibility features mentioned in the details). 
