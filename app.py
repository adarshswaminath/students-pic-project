from flask import Flask,render_template,url_for,request,flash
import os
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = "static"
ALLOWED_EXTENSIONS = {"png",'jpg'}


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__,template_folder='templates/')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'admin@!23'


@app.route("/")
def index():
    image_names = os.listdir('static')
    return render_template("index.html",image_name=image_names)


@app.route("/upload")
def upload():
    return render_template("upload.html")

@app.route("/upload",methods=["POST"])
def upload_image():
    email = request.form['email']
    regno = request.form['reg-no']
    file = request.files['image']
    about = request.form['about']
    new_name = f"{regno}.png"

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"],new_name))
    payload = f"{email},{regno},{about}\n"
    data = open("data.csv",'a')
    data.write(payload)
    return render_template("upload.html",msg="File Submitted Succesfully We will Send you a Email when file in web")


@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/admin',methods=['POST'])
def admin_auth():
    username = request.form['username']
    password = request.form['password']
    if(username != 'admin' or password != 'password'):
        flash('Wrong Username and password')
        return render_template('admin.html')
    else:
        return render_template('dashboard.html')


if __name__ == "__main__":
    app.run(debug=True)