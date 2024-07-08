# app.py
import streamlit as st
import pandas as pd
from Connecting_Code_1 import get_response

prompt = """
You will be provided with three paragraphs and three questions. Your task is to provide the answers to these questions using only the information present in the paragraphs. Ensure that your answers are strictly one or two words. If the answer is not found within the paragraphs, return "Not in the context".

**Instructions:**
1. Provide answers strictly based on the given paragraphs.
2. Ensure each answer is one or two words. If more than two words are found, summarize to one or two key words.
3. Validate that the answer exists in the paragraph and is contextually correct.
4. If the answer is not found in the paragraphs, return "Not in the context".

Here are the paragraphs:

Paragraph 1: Inside cells, glucose is swiftly transformed into glucose-6-phosphate, creating a gradient that favors glucose entry into cells. Insulin facilitates glucose storage as glycogen in liver and muscle cells and promotes protein synthesis in muscles. It also enables muscle protein breakdown for energy during starvation. Post-meal, dietary fats and sugars are used for immediate energy, with excess glucose stored as glycogen or fat, and dietary fat stored as triglycerides in adipose tissue. This process is depicted in Figure 24.21 during the absorptive state.

Paragraph 2: Inside cells, glucose is swiftly changed into glucose-6-phosphate. This creates a gradient, with higher glucose in blood than cells, enabling glucose to flow into cells. Insulin triggers glucose storage as glycogen in liver and muscle cells for future energy. It also boosts muscle protein synthesis. Muscle protein can be broken down for energy during starvation. Dietary fats and sugars are processed for immediate energy post-meal. Unused glucose is stored as glycogen or fat, and excess dietary fat as triglycerides in fat tissues. Figure 24.21 illustrates these metabolic processes during the absorptive state.

Paragraph 3: Inside these cells, glucose is immediately converted into glucose-6-phosphate. By doing this, a concentration gradient is established where glucose levels are higher in the blood than in the cells. This allows for glucose to continue moving from the blood to the cells where it is needed. Insulin also stimulates the storage of glucose as glycogen in the liver and muscle cells where it can be used for later energy needs of the body. Insulin also promotes the synthesis of protein in muscle. As you will see, muscle protein can be catabolized and used as fuel in times of starvation. If energy is exerted shortly after eating, the dietary fats and sugars that were just ingested will be processed and used immediately for energy. If not, the excess glucose is stored as glycogen in the liver and muscle cells, or as fat in adipose tissue; excess dietary fat is also stored as triglycerides in adipose tissues. Figure 24.21 summarizes the metabolic processes occurring in the body during the absorptive state.

Questions:

Question 1: What type of tissue is used to store the triglycerides?

Question 2: What is the role of Insulin?

Question 3: What is the process called where the glucose is converted to glucose-6-phosphate?

Please provide questions and answers seperately for all the above questions for all the paragraphs.

"""

text = get_response(prompt, "gpt-35-turbo-16k")

# Remove any leading newlines
text = text.lstrip()

# Process the text and create a DataFrame
# Split the text into paragraphs
paragraphs = text.strip().split("\n\nParagraph")

# Initialize lists to store the data
questions = []
answers_p1 = []
answers_p2 = []
answers_p3 = []

# Helper function to extract questions and answers from a paragraph
def extract_qa(paragraph):
    q_list = []
    a_list = []
    lines = paragraph.strip().split("\n")
    for line in lines:
        if line.startswith("Question"):
            q_list.append(line.split(": ", 1)[1].strip())
        elif line.startswith("Answer"):
            a_list.append(line.split(": ", 1)[1].strip())
    return q_list, a_list

# Process each paragraph
for i, paragraph in enumerate(paragraphs):
    q_list, a_list = extract_qa(paragraph)
    if i == 0:
        questions = q_list  # Only store questions from the first paragraph
        answers_p1 = a_list
    elif i == 1:
        answers_p2 = a_list
    elif i == 2:
        answers_p3 = a_list

# Ensure all lists are the same length
assert len(questions) == len(answers_p1) == len(answers_p2) == len(answers_p3), "Lists are not of the same length."

# Create the DataFrame
data = {
    "Questions": questions,
    "Paragraph_1_answers": answers_p1,
    "Paragraph_2_answers": answers_p2,
    "Paragraph_3_answers": answers_p3
}

df = pd.DataFrame(data)

# Title of the Streamlit app
st.title("Generated Data Table")

# Display the DataFrame
st.write("Here is the generated data:")
st.dataframe(df)

# Function to convert DataFrame to CSV
@st.cache
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

# Download button
csv = convert_df_to_csv(df)
st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='generated_data.csv',
    mime='text/csv'
)
