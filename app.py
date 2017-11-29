import os
from flask import *
from flask_mysqldb import MySQL
from forms import *
from passlib.hash import sha256_crypt
from functools import wraps
from werkzeug import secure_filename


madi = Flask(__name__)
madi.secret_key = "loongo music"

madi.config['ALLOWED_EXTENSIONS'] = set(['jpg','jpeg','png','gif'])
madi.config['ALLOWED_EXTENSIONS1'] = set(['mp3'])


UPLOAD_FOLDER =  'static/uploads/images'
UPLOAD_FOLDER1 =  'static/uploads/audios'

madi.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
madi.config['UPLOAD_FOLDER1'] = UPLOAD_FOLDER1
madi.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

#config myswl db
madi.config['MYSQL_HOST'] = 'localhost'
madi.config['MYSQL_USER'] = 'root'
madi.config['MYSQL_PASSWORD'] = 'dengima'
madi.config['MYSQL_DB'] = 'Music'
madi.config['MYSQL_CURSORCLASS'] = 'DictCursor'



#init MYSQL_DB
mysql = MySQL(madi)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1] in madi.config['ALLOWED_EXTENSIONS']

def allowed_file1(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1] in madi.config['ALLOWED_EXTENSIONS1']

@madi.route('/')
@madi.route('/index')
def index():

    cur = mysql.connection.cursor()

    result = cur.execute("SELECT * FROM songs")
    audios = cur.fetchall()

    if result > 0:
        return render_template('index.html', audios=audios)
    else:
        msg = 'No News found'
        return render_template('index.html', msg=msg)

    cur.close()
    return render_template('index.html')

@madi.route('/audio/<string:id>')
def audio(id):
    cur = mysql.connection.cursor()

    result = cur.execute('SELECT * FROM songs WHERE id = %s',[id])

    audio = cur.fetchone()

    return render_template('audio.html', audio=audio)

@madi.route('/audios')
def audios():


    cur = mysql.connection.cursor()

    result = cur.execute("SELECT * FROM songs")
    audios = cur.fetchall()

    if result > 0:
        return render_template('audios.html', audios=audios)
    else:
        msg = 'No News found'
        return render_template('audios.html', msg=msg)

    cur.close()

    return render_template('audios.html')

@madi.route('/videos')
def videos():
    return render_template('videos.html')

@madi.route('/artists')
def artists():
    return render_template('artists.html')

@madi.route('/new/<string:id>')
def new(id):

    cur = mysql.connection.cursor()

    result = cur.execute('SELECT * FROM news WHERE id = %s',[id])

    new = cur.fetchone()

    return render_template('new.html', new=new)

@madi.route('/news')
def news():

    cur = mysql.connection.cursor()

    result = cur.execute("SELECT * FROM news")
    news = cur.fetchall()

    if result > 0:
        return render_template('news.html', news=news)

    else:
        msg = 'No News found'
        return render_template('news.html', msg=msg)

    cur.close()
    return render_template('news.html')

@madi.route('/contact')
def contact():
	form = ContactForm()
	return render_template('contact.html', form=form)

@madi.route("/login", methods=['GET','POST'])
def login():
    #if 'email' in session:
    #        return redirect(url_for('home'))
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password_candidate = form.password.data
        
        #create cursor
        cur = mysql.connection.cursor()

        #get user by email
        result = cur.execute('SELECT * FROM users WHERE username = %s', [username] )
        if result > 0:
            data = cur.fetchone()
            password = data['password']

            #comapare passwords
            if sha256_crypt.verify(password_candidate, password):
                #passed
                session['logged_in'] = True
                session['username'] = username
                #app.logger.info("pwd matched")
                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash("Wrong Password, Try again", 'danger')
                #app.logger.info("pwd not matched")
                #return render_template("login.html", error=error)
                return redirect(url_for('login'))


            cur = close()
        else:
            #app.logger.info("no user")
            flash("Username not found, enter correcct username",'danger')
            #return render_template("login.html", error=error)
            return redirect(url_for('login'))      
    return render_template("login.html", form=form)


@madi.route('/signup', methods=['POST','GET'])
def signup():
    form = RegistrationForm(request.form, csrf_enabled=False)
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))

        #create cursor
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO users(username,email,password) VALUES(%s,%s,%s)',(username,email,password) )
        
        #commit to db
        mysql.connection.commit()
        
        #close db
        cur.close()

        flash('You are now registered and can log in','success')

        return redirect(url_for('login'))

    return render_template('signup.html', form=form)

@madi.route("/logout")
def logout():
    session.clear()
    flash("You are now logged out",'success')
    return redirect(url_for('index'))

@madi.route("/dashboard")
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    return render_template('dashboard.html')

@madi.route("/news_dashboard")
def news_dashboard():

    cur = mysql.connection.cursor()

    result = cur.execute("SELECT * FROM news")
    news = cur.fetchall()

    if result > 0:
        return render_template('news_dashboard.html', news=news)
    else:
        msg = 'No news found'
        return render_template('news_dashboard.html', msg=msg)

    cur.close()

    return render_template('news_dashboard.html')

@madi.route("/music_dashboard")
def music_dashboard():

    cur = mysql.connection.cursor()

    result = cur.execute("SELECT * FROM songs")
    songs = cur.fetchall()

    if result > 0:
        return render_template('music_dashboard.html', songs=songs)
    else:
        msg = 'No songs found'
        return render_template('music_dashboard.html', msg=msg)

    cur.close()

    return render_template('music_dashboard.html')


@madi.route('/edit_song/<string:id>', methods=['POST','GET'])
def edit_song(id):
    if 'username' not in session:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    
    result = cur.execute("SELECT * FROM songs WHERE id = %s",[id])    

    song = cur.fetchone()

    form = UploadSongForm(request.form)
    form.song_title.data = song['song_title']
    form.artist_name.data = song['artist_name']
    form.upload.data = song['upload']

    if request.method == 'POST' and form.validate():
        song_title = request.form['story_title']
        artist_name = request.form['artist_name']
        song_upload = request.form['upload']

        cur = mysql.connection.cursor()

        sql = "UPDATE songs SET song_title=%s, artist_name=%s, song_upload=%s WHERE id=%s"
        args = [song_title,artist_name,song_upload,id]
        cur.executemany(sql, args)

        mysql.connection.commit()

        cur.close()
        flash("Music Upadted Successfully", 'success')
        return redirect(url_for("music_dashboard"))

    return render_template('edit_song.html', form=form)

@madi.route("/edit_news/<string:id>", methods=['POST','GET'])
def edit_news(id):
    if 'username' not in session:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    
    result = cur.execute("SELECT * FROM news WHERE id = %s",[id])    

    new = cur.fetchone()

    form = UploadNewsForm(request.form)

    form.story_title.data = new['story_title']
    form.upload.data = new['upload']
    form.body.data =new['body']

    if request.method == 'POST' and form.validate():
        story_title = request.form['story_title']
        news_image = request.form['upload']
        body = request.form['body']

        cur = mysql.connection.cursor()

        cur.execute("UPDATE news SET story_title=%s, news_image=%s, body=%s WHERE id=%s", [story_title,news_image,body,id])
        
        mysql.connection.commit()

        cur.close()
        flash("News Upadted Successfully", 'success')
        return redirect(url_for("news_dashboard"))
    return render_template('edit_news.html', form=form)

@madi.route("/upload_audio", methods=['POST','GET'])
def upload_audio():
    form = UploadSongForm(request.form)
    if request.method == 'POST' and form.validate():
        song_title = form.song_title.data
        artist_name = form.artist_name.data
        song_upload = request.files['upload']
        filename = ' ';

        if song_upload and allowed_file1(song_upload.filename):
            filename = secure_filename(song_upload.filename)
            song_upload.save(os.path.join(madi.config['UPLOAD_FOLDER1'], filename))
            #image_url = images.url(news_image.save(os.path.join(madi.config['UPLOAD_FOLDER'], filename)))
        else:
            flash('Only mp3 allowed','danger')
            return render_template("upload_audio.html", form=form)

        cur = mysql.connection.cursor()
        #cur.execute('INSERT INTO songs(song_title,artist_name,song_upload) VALUES(%s,%s,%s)',(song_title,artist_name,song_upload,session['username']))

        sql = "INSERT INTO songs(song_title,artist_name,song_upload) VALUES({})".format(', '.join(['%s']*3))
        args = (song_title,artist_name,filename)
        cur.executemany(sql, [args])

        mysql.connection.commit()

        cur.close()
        flash("created successfully", 'success')
        return redirect(url_for('dashboard')) 
    return render_template('upload_audio.html', form=form)

@madi.route("/upload_video", methods=['POST','GET'])
def upload_video():
    if 'username' not in session:
        return redirect(url_for('login'))

    form = UploadSongForm()

    if request.method == 'POST' and form.validate():
        story_title = form.title.data
        song_upload = form.upload.data
        body = form.body.data

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO news(story_title,body,song_upload) VALUES(%s,%s,%s)',(story_title,body,song_upload,session['username']))

        mysql.connection.commit()

        cur.close()
        flash("created successfully", 'success')
        return redirect(url_for('dashboard')) 
    return render_template('upload_video.html', form=form)

@madi.route("/upload_news", methods=['POST','GET'])
def upload_news():
    if 'username' not in session:
        return redirect(url_for('login'))

    form = UploadNewsForm(request.form)
    if request.method == 'POST' and form.validate():
        story_title = form.story_title.data
        body =form.body.data
        #news_image = form.upload.data
        news_image = request.files['upload']
        filename = ' ';

        if news_image and allowed_file(news_image.filename):
            filename = secure_filename(news_image.filename)
            news_image.save(os.path.join(madi.config['UPLOAD_FOLDER'], filename))
            #image_url = images.url(news_image.save(os.path.join(madi.config['UPLOAD_FOLDER'], filename))
        else:
            flash('Only jpg ,jpeg, png and gif allowed','danger')
            return render_template("upload_news.html", form=form)

        cur = mysql.connection.cursor()
        #cur.executemany('INSERT INTO news(story_title,news_image,body) VALUES(%s,%s,%s);',(story_title,news_image,body,session['username']))
        sql = "INSERT INTO news(story_title,news_image,body) VALUES({})".format(', '.join(['%s']*3))
        args = (story_title,filename,body)
        cur.executemany(sql,[args])
        mysql.connection.commit()
        cur.close()
        flash("created successfully", 'success')
        return redirect(url_for('news_dashboard', filename=filename ))  
    return render_template('upload_news.html', form=form)



@madi.route("/delete_news/<string:id>" ,methods=['POST'])
def delete_news(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    else:

        cur = mysql.connection.cursor()
        
        cur.execute("DELETE FROM news WHERE id=%s",[id])

        mysql.connection.commit()

        cur.close()

        flash("News Deleted", 'success')

        return redirect(url_for('news_dashboard'))
    return render_template('news_dashboard.html')


@madi.route("/delete_music/<string:id>" ,methods=['POST'])
def delete_music(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    else:

        cur = mysql.connection.cursor()
        
        cur.execute("DELETE FROM songs WHERE id=%s",[id])

        mysql.connection.commit()

        cur.close()

        flash("Song Deleted", 'success')

        return redirect(url_for('music_dashboard'))
    return render_template('music_dashboard.html')


if __name__ == '__main__':
    madi.run(debug=True)