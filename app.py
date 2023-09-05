from flask import Flask, flash ,Response,  render_template, request , redirect
from flask_login import UserMixin ,current_user, LoginManager,login_user, logout_user,login_required
login_manager = LoginManager()
app = Flask(__name__)
login_manager.init_app(app)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
login_manager.login_view = "login"


class User(UserMixin):

    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return (self.id)


user = User(0)




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


@app.route('/post_blog.html', methods=['GET', 'POST'])
@login_required
def blog ():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']

        return show_blog(title, description)
        return redirect('/page3.html')
    return render_template('post_blog.html')

@app.route('/page3.html')
@login_required
def show_blog(title, body):
    print (body)
    #text = body.split('\n')
    text= body.replace('\n', '<br>')


    return render_template('page3.html', title = title , text = text)


@app.route('/login.html', methods=['GET', 'POST'] )
def login ():
    if request.method == 'POST':
        username = request.form['user']
        password = request.form['pass']
        if username == "saeed" and password == "pass":

           login_user(user)
           return redirect('/post_blog.html')
        if user != 'saeed' or password != 'pass' :

           flash('user or pass is wrong')

    return render_template('login.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/login.html')




@login_manager.user_loader
def load_user(userid):
    return User(userid)







if __name__ == "__main__":
    app.run(port = 4500 , debug = True)
