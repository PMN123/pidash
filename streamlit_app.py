import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import tempfile

# Load data
data = pd.read_csv('data.csv')

# Display app title
st.title("Performance Indicator Dashboard")

# Column names (adjust these if necessary to match your CSV exactly)
description_column = 'Description'
code_column = 'Code'

# Cluster columns (adjust to match the exact headers in your CSV)
clusters = [
    'Business Administration Core', 
    'Business Management and Administration', 
    'Entrepreneurship', 
    'Finance', 
    'Financial Literacy', 
    'Hospitality and Tourism', 
    'Marketing'
]

# Define acronyms for each cluster
cluster_acronyms = {
    'Business Administration Core': 'BAC',
    'Business Management and Administration': 'BMA',
    'Entrepreneurship': 'ENT',
    'Finance': 'FIN',
    'Financial Literacy': 'FL',
    'Hospitality and Tourism': 'HT',
    'Marketing': 'MKT'
}

# Create checkboxes for each cluster
selected_clusters = []
for cluster in clusters:
    if st.checkbox(cluster):
        selected_clusters.append(cluster)

# Filter data based on selected clusters
if selected_clusters:
    # Filter rows where any of the selected clusters have an "X"
    filtered_data = data[data[selected_clusters].apply(lambda row: row.str.contains('X').any(), axis=1)]
    st.write("### Selected Performance Indicators:")
    st.dataframe(filtered_data[[description_column, code_column] + selected_clusters])
else:
    st.write("Please select at least one cluster to display relevant Performance Indicators.")

# Generate acronym string for file name based on selected clusters
acronym_string = "_".join(cluster_acronyms[cluster] for cluster in selected_clusters)

# PDF generation function with ReportLab
def generate_pdf(filtered_data, pdf_filename):
    # Create a temporary file for the PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        pdf_path = tmp_file.name

    # Document setup with increased margins
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=50,
        bottomMargin=50,
        title=pdf_filename  # Set the title of the PDF document
    )
    elements = []

    # Styles
    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    header_style = styles["Heading2"]
    body_style = styles["BodyText"]

    # Title and Terms of Use
    elements.append(Paragraph("Performance Indicator Report", title_style))
    elements.append(Spacer(1, 0.2 * inch))
    terms = (
        "Terms of Use: The information provided in this document is proprietary and "
        "intended for educational or informational purposes only. Unauthorized distribution "
        "or use of this information without prior consent is prohibited."
    )
    elements.append(Paragraph(terms, body_style))
    elements.append(Spacer(1, 0.3 * inch))

    # Key Section
    key_content = """
    <b>Key</b><br/>
    <b>PQ</b>: Prerequisite level performance indicator content develops employability and job-survival skills and concepts, including work ethics, personal appearance, and general business behavior.<br/>
    <b>CS</b>: Career Sustaining level performance indicator content develops skills and knowledge needed for continued employment in or study of business based on the application of basic academics and business skills.<br/>
    <b>SP</b>: Specialist level performance indicator content provides in-depth, solid understanding and skill development in all business functions.<br/>
    <b>SU</b>: Supervisor Content provides the same in-depth, solid understanding and skill development in all business functions as in the specialist curriculum, and in addition, incorporates content that addresses the supervision of people.<br/>
    <b>MN</b>: Manager Content develops strategic decision-making skills in all business functions needed to manage a business or department within an organization.<br/>
    <b>ON</b>: Owner Content develops strategic decision-making skills in all aspects of business that are needed to own and operate a business.
    """
    elements.append(Paragraph(key_content, body_style))
    elements.append(Spacer(1, 0.3 * inch))

    # Header for Selected Clusters
    selected_clusters_text = "Selected Clusters: " + ", ".join(selected_clusters)
    elements.append(Paragraph(selected_clusters_text, header_style))
    elements.append(Spacer(1, 0.3 * inch))

    # Add each relevant PI from the filtered data with padding above and below each entry
    for _, row in filtered_data.iterrows():
        pi_code = f"Code: {row[code_column]}"
        pi_description = row[description_column]

        # Add padding above the entry
        elements.append(Spacer(1, 0.15 * inch))

        # Add the code as a simple text line
        elements.append(Paragraph(pi_code, body_style))

        # Preserve formatting with line breaks and wrap text
        first_line, rest_of_text = split_first_line(pi_description)
        rest_of_text = rest_of_text.replace('\n', '<br />')  # Preserve line breaks for wrapping
        formatted_text = f'<b>{first_line}</b><br />{rest_of_text}'
        elements.append(Paragraph(formatted_text, body_style))
        
        # Add padding below the entry
        elements.append(Spacer(1, 0.3 * inch))

    # Build the PDF
    doc.build(elements, onFirstPage=add_page_number, onLaterPages=add_page_number)

    return pdf_path


def split_first_line(text):
    """Splits the text into the first line and the rest."""
    lines = text.split('\n', 1)
    if len(lines) > 1:
        return lines[0], lines[1]
    return lines[0], ''  # If there's no line break, return the whole text as the first line

# Function to add page numbers
def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 10)
    canvas.drawString(4.25 * inch, 0.5 * inch, f"Page {doc.page}")
    canvas.restoreState()

# Download the filtered data as a PDF
if selected_clusters and st.button("Generate PDF"):
    # Construct the filename with the acronym string
    pdf_filename = f"Performance_Indicator_Report_{acronym_string}.pdf"
    
    # Generate the PDF with the desired filename
    pdf_path = generate_pdf(filtered_data, pdf_filename)

    # Allow the user to download the generated PDF
    with open(pdf_path, "rb") as pdf_file:
        pdf_bytes = pdf_file.read()
        st.download_button(
            label="Download PDF",
            data=pdf_bytes,
            file_name=pdf_filename,
            mime="application/pdf"
        )
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        bottom: 0;
        width: 100%;
        color: black;
        text-align: center;
        padding: 10px;
        font-size: 12px;
    }
    </style>
    <div class="footer">
        &copy; Praniil Nagaraj, 2025
    </div>
    """,
    unsafe_allow_html=True
)
