from flask import Flask,render_template,url_for
app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/userlog')
def userlog():
    return render_template('login/user.html')


@app.route('/adminlog')
def adminlog():
    return render_template('login/admin.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


