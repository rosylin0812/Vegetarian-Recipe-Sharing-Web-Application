from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from veggyblog import db, login_manager # should be put under line 1 to avoid circular imports
from flask_login import UserMixin

# user_loader: reload the user object from the user ID stored in the session.
# extension knows this is the function to get a user by ID.
@login_manager.user_loader 
def load_user(user_id):
    
    return User.query.get(int(user_id))


# create class modules that will be in database stucture
# each class is its own table in the database


'''
for many-to-many relationships ( followes table ), you will need to define a helper table that is used for the relationship. 
Strongly recommended to not use a model but an actual table
'''
follows = db.Table('follows',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)
    #Note: In SQLAlchemy model, having 2 columns with primary_key=True creates a compound primary key.

class User(db.Model, UserMixin): # inherint from db.model
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(60), nullable = False)
    image_file = db.Column(db.String(20), nullable = True, default= 'default.jpg')
    posts = db.relationship('Post', backref= 'author', lazy=True)
    saved = db.relationship('PostSaved', foreign_keys='PostSaved.user_id', backref='user', lazy='dynamic')
    followed = db.relationship('User', secondary=follows,
        primaryjoin=(follows.c.follower_id == id),
        secondaryjoin=(follows.c.followed_id == id),
        backref=db.backref('follows', lazy='dynamic'), lazy='dynamic') #This relationship links User instances to other User instances
    
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            follows.c.followed_id == user.id).count() > 0
    
    
    def save_post(self, post):
        if not self.has_saved_post(post):
            save = PostSaved(user_id=self.id, post_id=post.id)
            db.session.add(save)

    def unsave_post(self, post):
        if self.has_saved_post(post):
            PostSaved.query.filter_by(
                user_id=self.id,
                post_id=post.id).delete()

    def has_saved_post(self, post):
        return PostSaved.query.filter(
            PostSaved.user_id == self.id,
            PostSaved.post_id == post.id).count() > 0
    
    def get_reset_token(self, expires_sec=1800): 
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec) # expiration time by defaul is 30mins here 
        return s.dumps({'user_id': self.id}).decode('utf-8') # create token and contain a payload of the current user id
    
    @staticmethod #telling python not to expect 'self' parameter as an argument and only accept token as an argument
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
    
    # whem the user object is printted out
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class PostSaved(db.Model):
    __tablename__ = 'post_saved'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    date_posted = db.Column(db.DateTime,  nullable = False, default=datetime.utcnow)
    content= db.Column(db.Text, nullable= False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    saves = db.relationship('PostSaved', backref='post', lazy='dynamic')
    
    # when the user object is printted out
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"