from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_socketio import SocketIO, emit, join_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

socketio = SocketIO(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

@app.route('/create_document', methods=['GET', 'POST'])
@login_required
def create_document():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        new_document = Document(title=title, content=content, user_id=current_user.id)
        db.session.add(new_document)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('create_document.html')

@app.route('/documents')
@login_required
def documents():
    user_documents = Document.query.filter_by(user_id=current_user.id).all()
    return render_template('documents.html', documents=user_documents)

@app.route('/edit_document/<int:doc_id>', methods=['GET', 'POST'])
@login_required
def edit_document(doc_id):
    document = Document.query.get_or_404(doc_id)
    if request.method == 'POST':
        document.title = request.form.get('title')
        document.content = request.form.get('content')
        db.session.commit()
        return redirect(url_for('documents'))
    return render_template('edit_document.html', document=document)

@socketio.on('join')
def on_join(data):
    room = data['room']
    join_room(room)

@socketio.on('edit')
def on_edit(data):
    room = data['room']
    emit('update_content', data, room=room, include_self=False)

@app.route('/collaborate/<int:doc_id>')
@login_required
def collaborate(doc_id):
    document = Document.query.get_or_404(doc_id)
    return render_template('collaborate.html', document=document, room=doc_id)

class DocumentVersion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('document.id'))
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

@app.route('/versions/<int:doc_id>')
@login_required
def versions(doc_id):
    document_versions = DocumentVersion.query.filter_by(document_id=doc_id).all()
    return render_template('versions.html', versions=document_versions)

@app.route('/save_version/<int:doc_id>', methods=['POST'])
@login_required
def save_version(doc_id):
    document = Document.query.get_or_404(doc_id)
    new_version = DocumentVersion(document_id=doc_id, content=document.content)
    db.session.add(new_version)
    db.session.commit()
    return redirect(url_for('collaborate', doc_id=doc_id))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.username = request.form.get('username')
        db.session.commit()
        return redirect(url_for('profile'))
    return render_template('profile.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)