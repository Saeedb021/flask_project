from flask import Flask, flash ,Response,  render_template, request , redirect, url_for
from flask_login import UserMixin ,current_user, LoginManager,login_user, logout_user,login_required
import psycopg2
import config
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = os.path.join('static/upload')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

login_manager = LoginManager()
app = Flask(__name__)
login_manager.init_app(app)
login_manager.login_message = "You need to be logged in to view this page"
login_manager.login_message_category = "warning"
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
login_manager.login_view = "login"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS





def insert_blog(url, title, body, image):
    cur = conn.cursor()

    sql = """INSERT INTO blog(url, title, body,image) VALUES(%s, %s, %s, %s);"""

    cur.execute(sql, (url, title, body, image))

    # commit the changes to the database
    conn.commit()
    # close communication with the database
    cur.close()


def read_db(url):
    cur = conn.cursor()

    cur.execute("SELECT url, title , body, image FROM blog WHERE url = %s ", (url,))
    all = cur.fetchall()
    if len(all) == 0:
        return ('404')
    else :
        blog = all[0]
        title = blog[1]
        body = blog[2]
        image = blog[3]

        cur.close()

        return(title, body,image)





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
        if 'file' not in request.files:
            flash('No file part', 'warning')
            return redirect(request.url)
        file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
        if file.filename == '':
            flash('No selected file','warning')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        insert_blog(url, title, description, filename)            # check if the post request has the file part



        return redirect(f'/{url}')
    return render_template('post_blog.html')

@app.route('/<page>')
def show_blog(page):

    if read_db(page) == '404':
        return render_template('404.html')

    else :

        title, body, image = read_db(page)
        text = body.split('\n')
        text= body.replace('\n', '<br>')
        image = 'static/upload/'+ image
        return render_template('blogs.html', title = title , text = text ,image = image , m = is_login('blog'))

@app.route('/post_blog', methods=['GET', 'POST'])
def upload_file():


    return render_template('postp.html')










@app.route('/login', methods=['GET', 'POST'] )
def login ():
    if request.method == 'POST':
        username = request.form['user']
        password = request.form['pass']
        if username == "saeed" and password == "pass":

           login_user(user)
           return redirect('/')
        if user != 'saeed' or password != 'pass' :

           flash('username or password is wrong', 'danger')

    return render_template('login.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Logged out', 'success')
    return redirect('/login')


@login_manager.user_loader
def load_user(userid):
    return User(userid)







if __name__ == "__main__":
    app.run(port = 4500 , debug = True)
