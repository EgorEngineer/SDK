from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from flask_login import LoginManager, login_required, current_user
from datetime import datetime

app = Flask(__name__)  # Измените 'name' на '__name__'

# Подключение к базе данных PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@127.0.0.1:5432/postgres_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализация базы данных и миграций
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Пример моделей
class User(db.Model):
    __tablename__ = 'users'  # Измените 'tablename' на '__tablename__'
    user_id = db.Column(db.BigInteger, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Feature(db.Model):
    __tablename__ = 'features'  # Измените 'tablename' на '__tablename__'
    feature_id = db.Column(db.BigInteger, primary_key=True)
    app_id = db.Column(db.BigInteger, db.ForeignKey('apps.app_id'))
    feature_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Flask-Login и другие маршруты...

if __name__ == '__main__':  # Измените 'name' на '__name__'
    app.run(debug=True)

