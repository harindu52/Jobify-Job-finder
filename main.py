import os
import json
from flask import Flask, render_template, redirect, url_for, request
from Reader import job_detail_arrange, job_letter, job_eligibility
from Backend import get_job_data
import pandas as pd
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "static\\data"


@app.route('/')
def index_page():
    return render_template("form.html")


@app.route('/', methods=['GET', 'POST'])
def get_all_posts():

    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename))
            USER = uploaded_file.filename[:len(uploaded_file.filename)-4]
            print(USER)
            posts = get_job_data(USER)
            print(posts)
            return render_template("index.html", all_posts=posts)
        # return redirect(url_for('get_all_posts'))


# @app.route('/home')
# def get_all_posts():
#     # posts = get_job_data(USER)
#     print(posts)
#     return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/post/<int:index>")
def show_post(index):
    file = open("jobdata.json")
    posts = json.load(file)
    requested_post = None
    for job_post in posts:
        if job_post["id"] == index:
            requested_post = job_post
            requested_post["Job_detail"] = job_detail_arrange(requested_post["Job_detail"])
            print(requested_post["Job_detail"])
            requested_post["Letter"] = job_letter("software-engineer-resume-example", requested_post["Job_detail"])
            requested_post["Eligible"] = job_eligibility("software-engineer-resume-example", requested_post["Job_detail"])
    return render_template("post.html", post=requested_post)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
