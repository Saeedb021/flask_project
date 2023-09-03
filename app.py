from flask import Flask, flash ,Response,  render_template, request , redirect
from flask_login import LoginManager, login_user, UserMixin

login_manager = LoginManager()
app = Flask(__name__)
#login_manager.init_app(app)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

class User(UserMixin):

    def __init__(self, id):
        self.id = id
    def is_active (self):
        return(True)
    def __repr__(self):
        return "%d" % (self.id)


user = User(1)

@app.route('/')
@app.route('/index.html')
def home():
    return render_template('index.html')

@app.route('/about.html')
def about():
    return render_template('about.html')
@app.route('/<page>.html')
def pages (page):
    page_url = page + '.html'
    return render_template(page_url)
@app.route('/login.html', methods=['GET', 'POST'] )
def login ():
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['pass']
        if user == "saeed" and password == "pass":

          # login_user(user)
           return redirect('/')
        if user != 'saeed' or password != 'pass' :

           flash('user or pass is wrong')

    return render_template('login.html')


if __name__ == "__main__":
    app.run(port = 4500 , debug = True)
