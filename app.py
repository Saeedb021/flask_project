from flask import Flask, flash ,Response,  render_template, request , redirect
from flask_login import UserMixin ,current_user, LoginManager,login_user, logout_user,login_required
import psycopg2
import config

login_manager = LoginManager()
app = Flask(__name__)
login_manager.init_app(app)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
login_manager.login_view = "login"

conn = psycopg2.connect( host= config.host, database= config.database , user= config.user
        , password=config.password)

cur = conn.cursor()

class User(UserMixin):

    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return (self.id)


user = User(0)

def is_login(place):
    if place == "blog":
        if current_user.is_authenticated:
            m ="bace_blag.html"
        else :
            m ="bace_blag_anon.html"
        return(m)
    if place == 'pages':
        if current_user.is_authenticated:
            m ="bace_pages.html"
        else :
            m ="bace_pages_anon.html"
        return(m)





def insert_blog(url, title, body):
    cur = conn.cursor()

    sql = """INSERT INTO blog_tb(url, title, body) VALUES(%s, %s, %s);"""

    cur.execute(sql, (url, title, body))

    # commit the changes to the database
    conn.commit()
    # close communication with the database
    cur.close()


def read_db(url):
    cur = conn.cursor()

    cur.execute("SELECT url, title , body FROM blog_tb WHERE url = %s ", (url,))
    all = cur.fetchall()
    if len(all) == 0:
        return ('404')
    else :
        blog = all[0]
        title = blog[1]
        body = blog[2]

        cur.close()

        return(title, body)





@app.route('/')
@app.route('/index.html')
def home():
    return render_template('index.html' ,m = is_login('pages'))

@app.route('/about')
def about():
    return render_template('about.html', m = is_login('pages'))


@app.route('/contacts')
def contacts():
    return render_template('contacts.html', m = is_login('pages'))


@app.route('/post_blog', methods=['GET', 'POST'])
@login_required
def blog ():
    if request.method == 'POST':
        url = request.form['Url']
        title = request.form['title']
        description = request.form['description']
        insert_blog(url, title, description)


        return redirect(f'/{url}')
    return render_template('post_blog.html')

@app.route('/<page>')
def show_blog(page):



    if read_db(page) == '404':
        return render_template('404.html')

    else :

        title, body = read_db(page)
        text = body.split('\n')
        text= body.replace('\n', '<br>')
        return render_template('blogs.html', title = title , text = text , m = is_login('blog'))









@app.route('/login', methods=['GET', 'POST'] )
def login ():
    if request.method == 'POST':
        username = request.form['user']
        password = request.form['pass']
        if username == "saeed" and password == "pass":

           login_user(user)
           return redirect('/post_blog')
        if user != 'saeed' or password != 'pass' :

           flash('user or pass is wrong')

    return render_template('login.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/login')


@login_manager.user_loader
def load_user(userid):
    return User(userid)







if __name__ == "__main__":
    app.run(port = 4500 , debug = True)
