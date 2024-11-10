
# Performance Indicator Dashboard

This project is a Streamlit application that generates a PDF report based on selected performance indicators (PIs) across various business clusters. Users can select the business clusters they're interested in, view relevant PIs, and download a formatted PDF report that preserves the formatting and structure of each PI description.

## Features

- **Cluster Selection**: Allows users to select business clusters (e.g., Finance, Marketing, Entrepreneurship) and view only relevant performance indicators.
- **PDF Generation**: Generates a PDF report based on the selected clusters. The report includes the cluster code, a bolded first line for each PI, and retains original formatting like line breaks and bullet points.
- **Customizable File Name**: The downloaded PDF file name includes acronyms of the selected clusters, making it easy to identify.
- **Formatted PDF Layout**: Ensures padding at the top and bottom of each page, with a professional layout that includes page numbers and a document title that matches the file name.

## Technologies Used

- **Python**: Core language used to build the application.
- **Streamlit**: Provides an interactive web interface for selecting clusters and downloading the report.
- **ReportLab**: Used for generating and formatting the PDF output.

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/performance-indicator-dashboard.git
   cd performance-indicator-dashboard
   ```

2. **Install dependencies**:
   Make sure you have Python installed, then install required packages:
   ```bash
   pip install streamlit pandas reportlab
   ```

3. **Prepare the Data**:
   Ensure your data is saved as `data.csv` in the same directory as `app.py`. The CSV file should have columns corresponding to performance indicators, codes, and clusters. The specific columns expected include:
   - **Code**: Cluster code (e.g., "CS", "SP").
   - **Description**: The description of the performance indicator.
   - Additional columns for each cluster with values like "X" to indicate a PI belongs to that cluster.

4. **Run the Application**:
   Launch the Streamlit application:
   ```bash
   streamlit run app.py
   ```

5. **Using the Application**:
   - Select the clusters you are interested in by checking the appropriate boxes.
   - View the selected performance indicators in a table format.
   - Click **Download PDF** to generate and download a PDF report based on your selection.

## Example CSV Structure

Here’s a sample structure for `data.csv`:

| Code | Description                                           | Business Administration Core | Finance | Marketing | ... |
|------|-------------------------------------------------------|------------------------------|---------|-----------|-----|
| CS   | Accept checks from customers                          | X                            |         |           |     |
| SP   | Analyze financial statements                          |                              | X       |           |     |
| CS   | Develop a marketing plan                              |                              |         | X         |     |

## Configuration and Customization

- **Adjust Margins**: You can customize the top and bottom margins in the `generate_pdf` function to control the amount of padding on each page.
- **Change Cluster Names**: Modify the `clusters` and `cluster_acronyms` lists to include or exclude specific clusters.
- **Terms of Use Text**: Modify the terms of use text in the `generate_pdf` function if you need to update the disclaimer in the PDF report.

## Known Issues

- **Line Breaks and Special Characters**: If the description text has special formatting requirements, ensure that these are handled properly in `split_first_line` and `generate_pdf` functions to avoid formatting issues in the PDF.
- **Anonymous PDF Title**: Ensure the file name passed to the PDF generator matches the desired document title to avoid the "anonymous" title in some PDF viewers.

## Future Enhancements

- **Dynamic Cluster Management**: Add functionality to dynamically detect clusters from the CSV file, allowing for flexible changes to cluster names without modifying the code.
- **User-Defined Terms of Use**: Allow users to customize the terms of use text within the Streamlit interface before generating the PDF.
- **Styling Options**: Add more customization for font styles, colors, and layouts in the PDF output.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
