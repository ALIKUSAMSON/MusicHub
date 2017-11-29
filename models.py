Example 12-1. app/models/user.py: The follows association table as a model
class Follow(db.Model):
__tablename__ = 'follows'
follower_id = db.Column(db.Integer, db.ForeignKey('users.id'),
primary_key=True)
followed_id = db.Column(db.Integer, db.ForeignKey('users.id'),
primary_key=True)
timestamp = db.Column(db.DateTime, default=datetime.utcnow)