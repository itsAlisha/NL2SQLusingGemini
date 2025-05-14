
from dotenv import load_dotenv
import streamlit as st
import os
import sqlite3
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get response from Gemini model
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    
    sql_query = response.text.strip()
    sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
    
    return sql_query

def check_and_fix_schema(db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    
    cur.execute("PRAGMA table_info(STUDENT);")
    columns = [col[1] for col in cur.fetchall()]
    
    if "Course_ID" not in columns:
        print("⚠️ Adding missing column: Course_ID in STUDENT table")
        cur.execute("ALTER TABLE STUDENT ADD COLUMN Course_ID INTEGER;")
        conn.commit()
    
    conn.close()

# Function to execute SQL query and return results
def execute_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        conn.commit()
    except sqlite3.OperationalError as e:
        return f"SQL Error: {e}"
    except Exception as e:
        return f"Unexpected Error: {e}"
    finally:
        conn.close()

    return rows if rows else "No results found."

# Define prompt for SQL query generation
prompt = [
    """
    You are an expert at converting English questions into SQL queries.
    The database contains these tables:
    
    1. STUDENT(Student_ID, NAME, CLASS, SECTION, MARKS, Course_ID)
    2. TEACHERS(Instructor_ID, Name, Department)
    3. COURSES(Course_ID, Course_Name, Instructor_ID)
    
    **Guidelines:**
    - Convert the given English question into **correct SQL**.
    - **DO NOT** include backticks, markdown formatting, or extra words like "sql".
    - Use **JOINs** properly to link students, courses, and teachers when necessary.
    - If a query cannot be generated, return `"Invalid query"`.

    """
]

# Streamlit UI Setup
st.set_page_config(page_title="SQL Query Generator & Executor")
st.header("🔍 Gemini-powered SQL Query App")

check_and_fix_schema("student.db")

question = st.text_input("🔹 Enter your query:", key="input")
submit = st.button("🚀 Generate SQL & Fetch Data")

if "query_memory" not in st.session_state:
    st.session_state["query_memory"] = []  # Store (question, SQL query, result)

# On button click
if submit:
    sql_query = get_gemini_response(question, prompt)

    # Print the generated query in the terminal
    print("\n🔹 Generated SQL Query:")
    print(sql_query)

    result = execute_sql_query(sql_query, "student.db")

    st.session_state["query_memory"].append((question, sql_query, result))
    
    if len(st.session_state["query_memory"]) > 5:
        st.session_state["query_memory"].pop(0)

    st.subheader("📝 Generated SQL Query:")
    st.code(sql_query, language="sql")

    st.subheader("🗣 Response:")
    if isinstance(result, str):  
        st.error(result)
    else:
        for row in result:
            st.write(f"✅ {row}")

# Sidebar for history
st.sidebar.header("🕒 Query History (Last 5)")
for q, s, r in st.session_state["query_memory"]:
    st.sidebar.write(f"🔹 Q: {q}")
    st.sidebar.code(s, language="sql")
    st.sidebar.write(f"📝 Response: {r[:2]}...")  
