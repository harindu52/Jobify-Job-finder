from pdfquery import PDFQuery
from openai import OpenAI

OPENAI_API_KEY = ""

pdf = PDFQuery('static\\data\\data-scientist-resume-example.pdf')
pdf.load()
# Use CSS-like selectors to locate the elements
text_elements = pdf.pq('LTTextLineHorizontal')
# Extract the text from the elements
text = [t.text for t in text_elements]

client = OpenAI(api_key=OPENAI_API_KEY)


def get_job_name(name):
    pdf1 = PDFQuery(f'static\\data\\{name}.pdf')
    pdf1.load()

    # Use CSS-like selectors to locate the elements
    text_elements1 = pdf1.pq('LTTextLineHorizontal')
    # Extract the text from the elements
    text1 = [t.text for t in text_elements1]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Help me find a job"},
            {"role": "user", "content": f"What is the most suitable job for this resume : {text}"},
            {"role": "assistant", "content": "Data Scientist"},
            {"role": "user", "content": f"What is the best matching job for this resume :{text1}"}
        ]
    )
    job = response.choices[0].message.content
    job.replace(" ", "-")
    return job


def job_detail_arrange(job_details):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Help me find a job"},
            {"role": "user", "content": f"Arrange this job details in proper format : {job_details}"},
        ]
    )

    details = response.choices[0].message.content
    return details


def job_letter(name, details):
    pdf1 = PDFQuery(f'static\\data\\{name}.pdf')
    pdf1.load()

    # Use CSS-like selectors to locate the elements
    text_elements1 = pdf1.pq('LTTextLineHorizontal')
    # Extract the text from the elements
    text1 = [t.text for t in text_elements1]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Help me find a job"},
            {"role": "user",
             "content": f"Write a cover letter for this job : {details} using below mentioned resume {text1}"},
        ]
    )
    letter = response.choices[0].message.content
    return letter


def job_eligibility(name, details):
    pdf1 = PDFQuery(f'static\\data\\{name}.pdf')
    pdf1.load()

    # Use CSS-like selectors to locate the elements
    text_elements1 = pdf1.pq('LTTextLineHorizontal')
    # Extract the text from the elements
    text1 = [t.text for t in text_elements1]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Help me find a job"},
            {"role": "user",
             "content": f"Describe the eligibility for this job : {details} using below mentioned resume {text1}"},
        ]
    )
    eligible = response.choices[0].message.content
    return eligible
