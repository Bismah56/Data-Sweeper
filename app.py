import streamlit as st # type: ignore
import pandas as pd # type: ignore
import os
from io import BytesIO

# setting up our app
st.set_page_config(page_title="💿 Data Sweeper",layout="wide")


st.title("💿 Data Sweeper")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization!")

# upload files button
uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type=["csv","xlsx"], accept_multiple_files=True)

if uploaded_files:
    
    st.success("🎉 All files processed successfully!")  # Display success message when all files are processed
    for eachFile in uploaded_files:
        file_ext = os.path.splitext(eachFile.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(eachFile)
        elif file_ext == ".xlsx":
            df = pd.read_excel(eachFile)
        else:
            # Show an error message if the eachFile type is unsupported
            st.error(f"Unsupported eachFile type: {file_ext}")
            continue

        # Display Info about the eachFile
        st.write(f"**File Name:** {eachFile.name}")
        st.write(f"**File Size:** {round(eachFile.size/1024,1)} KB")

        # Preview the first 5 rows of the uploaded eachFile
        st.write("🔍 Preview of the Uploaded File:")
        if not df.empty:
            st.dataframe(df.head())# Display a scrollable preview of the data
        else:
            st.error("Uploaded eachFile is empty.") 

        # Section for data cleaning options
        st.subheader("🛠️ Data Cleaning Options")
        if st.checkbox(f"Clean Data for {eachFile.name}"):
            col1 , col2 = st.columns(2) #split cleaning options into two equal columns
            with col1:
                # Button to remove duplicate rows from the DataFrame
                if st.button(f"Remove Duplicates from {eachFile.name}"):
                    df.drop_duplicates()
                    st.write("✅ Duplicates Removed!")
            with col2:
                # Button to fill missing numeric values with column means
                if st.button(f"Fill Missing Values for {eachFile.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("✅ Missing Values in Numeric Columns Filled with Column Means!")
            
        # Section to choose specific columns to convert
        st.subheader("🎯 Select Columns to Convert")
        columns = st.multiselect(f"Choose Columns for {eachFile.name}", df.columns, default=df.columns)
        df = df[columns]  # Filters the DataFrame to the selected columns

        # Visualization section for uploaded data
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"Show Visualization for {eachFile.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])  # Plot the first two numeric columns as a bar chart
        
        # Section to choose eachFile conversion type (CSV or Excel)
        st.subheader("🔄 Conversion Options")
        conversion_type = st.radio(f"Convert {eachFile.name} to:", ["CSV", "Excel"], key=eachFile.name)
        if st.button(f"Convert {eachFile.name}"):
            buffer = BytesIO()  # Creates in-memory buffer for eachFile output
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)  # Save DataFrame as CSV in buffer
                file_name = eachFile.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False, engine='openpyxl')  # Save as Excel using openpyxl
                file_name = eachFile.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)
            
            # Download button for the converted eachFile
            st.download_button(
                label=f"⬇️ Download {eachFile.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

