import streamlit as st
import pandas as pd
from supabase import create_client

# Supabase Credentials
url = "https://xnmzivatgiaetmhbphdz.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhubXppdmF0Z2lhZXRtaGJwaGR6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzk5NjE0MTMsImV4cCI6MjA5NTUzNzQxM30.FCEd471MjR1DypuK6TpMWg5dNLlhiXflh4NhHjxdB3o"


supabase = create_client(url, key)

st.title("📤 Exam Room Upload")

uploaded_file = st.file_uploader(
    "Upload Excel File",
    type=["xlsx"]
)

if uploaded_file:

    # Read Excel
    df = pd.read_excel(uploaded_file)

    # Convert exam_date column to string
    if "exam_date" in df.columns:
        df["exam_date"] = pd.to_datetime(
            df["exam_date"]
        ).dt.strftime("%Y-%m-%d")

    st.subheader("Preview")
    st.dataframe(df)

    if st.button("Upload to Supabase"):

        try:
            records = df.to_dict(orient="records")

            supabase.table(
                "exam_rooms"
            ).insert(records).execute()

            st.success("✅ Data Uploaded Successfully!")

        except Exception as e:
            st.error(f"❌ Error: {e}")

st.title("Exam Room Finder")

roll = st.text_input("Enter Roll Number")

if st.button("Search"):

    result = supabase.table("exam_rooms")\
        .select("*")\
        .eq("roll_no", roll)\
        .execute()

    if result.data:
        data = result.data[0]

        st.success("Exam Details Found")

        st.write("🏢 Building:", data["building_name"])
        st.write("🚪 Room No:", data["room_no"])
        st.write("📅 Exam Date:", data["exam_date"])

    else:
        st.error("Roll Number Not Found")