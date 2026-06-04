import streamlit as st
import pandas as pd
from supabase import create_client

# =========================
# SUPABASE CONFIGURATION
# =========================
url = "https://xnmzivatgiaetmhbphdz.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhubXppdmF0Z2lhZXRtaGJwaGR6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzk5NjE0MTMsImV4cCI6MjA5NTUzNzQxM30.FCEd471MjR1DypuK6TpMWg5dNLlhiXflh4NhHjxdB3o"

supabase = create_client(url, key)

# =========================
# SIDEBAR NAVIGATION
# =========================
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select Page",
    ["🎓 Student", "📤 Admin"]
)

# =========================
# STUDENT PAGE
# =========================
if page == "🎓 Student":

    st.title("🎓 Exam Room Finder")

    roll = st.text_input("Enter Roll Number")

    if st.button("Search"):

        try:
            result = (
                supabase.table("exam_rooms")
                .select("*")
                .eq("roll_no", roll)
                .execute()
            )

            if result.data:

                data = result.data[0]

                st.success("Exam Details Found")

                st.write(f"🏢 Building Name: {data['building_name']}")
                st.write(f"🚪 Room Number: {data['room_no']}")
                st.write(f"📅 Exam Date: {data['exam_date']}")

            else:
                st.error("Roll Number Not Found")

        except Exception as e:
            st.error(f"Error: {e}")

# =========================
# ADMIN PAGE
# =========================
elif page == "📤 Admin":

    st.title("📤 Admin Upload")

    uploaded_file = st.file_uploader(
        "Upload Excel File",
        type=["xlsx"]
    )

    if uploaded_file:

        df = pd.read_excel(uploaded_file)

        # Convert date column
        if "exam_date" in df.columns:
            df["exam_date"] = pd.to_datetime(
                df["exam_date"],
                errors="coerce"
            ).dt.strftime("%Y-%m-%d")

        st.subheader("Preview")
        st.dataframe(df)

        if st.button("Upload Data"):

            try:
                records = df.fillna("").to_dict(
                    orient="records"
                )

                supabase.table(
                    "exam_rooms"
                ).insert(records).execute()

                st.success(
                    f"✅ {len(records)} records uploaded successfully!"
                )

            except Exception as e:
                st.error(f"❌ Upload Failed: {e}")