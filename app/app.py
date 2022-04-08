from unicodedata import name
from django.shortcuts import render
from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for
)
from flask_sqlalchemy import SQLAlchemy
import torch
from vncorenlp import VnCoreNLP
from transformers import AutoTokenizer,EncoderDecoderModel,AutoModelForSeq2SeqLM

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
db = SQLAlchemy(app)
tokenizer = AutoTokenizer.from_pretrained("./content/checkpoint-52000")
model = AutoModelForSeq2SeqLM.from_pretrained("./content/checkpoint-52000")
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

def text(input_text):
    with torch.no_grad():
        tokenized_text = tokenizer(input_text, truncation=True, padding=True, return_tensors='pt')
    
        source_ids = tokenized_text['input_ids'].to(device, dtype = torch.long)
        source_mask = tokenized_text['attention_mask'].to(device, dtype = torch.long)
    
        generated_ids = model.generate(
        input_ids = source_ids,
        attention_mask = source_mask, 
        max_length=512,
        num_beams=5,
        repetition_penalty=1, 
        length_penalty=1, 
        early_stopping=True,
        no_repeat_ngram_size=2
    )
        pred = tokenizer.decode(generated_ids[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)

    return pred

class User(db.Model):
    ID_User = db.Column(db.Integer, primary_key= True)
    User_Name = db.Column(db.String(200), nullable=False )
    Email = db.Column(db.String(200), nullable=False )
    Password = db.Column(db.String(200), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/homepage', methods = ['GET','POST'])
def homepage():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        inputtext = request.form['contentText']
        result = text(str(inputtext))
        return render_template('index.html',contentText = inputtext, result = result)
    
        

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    
    if request.method == 'POST':
        useraccount = User.query.filter_by(Email = request.form['username']).first()
        if useraccount != None: 
            password =  useraccount.Password
            if str(request.form['password']) != str(password):
                error = 'Sai tên đăng nhập hoặc mật khẩu !!!.'
            else:
                return redirect("./homepage")
        else:
            error = 'Sai tên đăng nhập hoặc mật khẩu !!!.'
    return render_template('login.html')

@app.route('/profile')
def profile():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('profile.html')

@app.route('/register', methods = ['POST', 'GET'])
def register():
    error = None
    if request.method == 'POST':
        useraccountcheck = User.query.filter_by(Email = request.form['email']).first()
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        repassword = request.form['repassword']
        if useraccountcheck == None:
            if repassword == password : 
                new_user = User(User_Name = username,Password = password,Email = email)
                db.session.add(new_user)
                db.session.commit()
                return redirect('/login')
            else:
                error = 'Mật khẩu không trùng khớp!!!'
        else:
            error = "User account exist!"
    return render_template('register.html',error = error)


if __name__=="__main__":
    app.run(host= "localhost",port = "5000")
