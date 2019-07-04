from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), unique=True, nullable=False)
    director = db.Column(db.String(30), unique=False, nullable=False)
    genre = db.Column(db.String(30), unique=False, nullable=False)
    collection = db.Column(db.Integer, unique=False, nullable=False)
    
    def __init__(self, title, director, genre, collection):
        self.title = title
        self.director = director
        self.genre = genre
        self.collection = collection
        
    def json(self):
        return {'Title': self.title, 'Director': self.director, 'Genre': self.genre, 'Collection': self.collection}
    
    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter_by(title=title).first()
    
    def save_to(self):
        db.session.add(self)
        db.session.commit()
        
    def delete_(self):
        db.session.delete(self)
        db.session.commit()
        
    

