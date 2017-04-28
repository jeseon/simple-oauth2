from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.ext.hybrid import hybrid_method

db = SQLAlchemy()


class BaseMixin(object):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=func.now(), onupdate=func.now())

    def __repr__(self):
        values = ', '.join('%s=%r' % (n, getattr(self, n)) for n in self.__table__.c.keys())
        return '%s(%s)' % (self.__class__.__name__, values)


class User(db.Model, BaseMixin):
    __tablename__ = 'users'

    email = db.Column(db.Unicode(255), nullable=False)
    encrypted_password = db.Column(db.Unicode(255), nullable=False)
    is_admin = db.Column(db.Integer)
    reset_password_token = db.Column(db.Unicode(255))
    reset_password_sent_at = db.Column(db.DateTime)
    sign_in_count = db.Column(db.Integer, nullable=False, default=0)
    current_sign_in_at = db.Column(db.DateTime)
    last_sign_in_at = db.Column(db.DateTime)
    current_sign_in_ip = db.Column(db.Unicode(255))
    last_sign_in_ip = db.Column(db.Unicode(255))
    role = db.Column(db.Integer)
    affiliate_id = db.Column(db.Integer)
    advertiser_id = db.Column(db.Integer)
    usertype = db.Column(db.Integer)
    username = db.Column(db.Unicode(255))
    company = db.Column(db.Unicode(255))

    @hybrid_method
    def to_dict(self):
        return dict(
            id=self.id,
            email=self.email,
            username=self.username,
            current_ip=self.current_sign_in_ip
        )

    @hybrid_method
    def is_authenticated(self):
        return True

    @hybrid_method
    def is_active(self):
        return True

    @hybrid_method
    def get_id(self):
        return self.id

    def __unicode__(self):
        return self.username


class Client(db.Model, BaseMixin):
    __tablename__ = 'client'

    client_id = db.Column(db.Unicode(40), nullable=False)
    client_secret = db.Column(db.Unicode(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    _redirect_uris = db.Column(db.Text)
    _default_scopes = db.Column(db.Text)

    user = db.relationship('User', backref=db.backref('clients'))

    @property
    def client_type(self):
        return 'public'

    @property
    def redirect_uris(self):
        if self._redirect_uris:
            return self._redirect_uris.split()
        return []

    @property
    def default_redirect_uri(self):
        return self.redirect_uris[0]

    @property
    def default_scopes(self):
        if self._default_scopes:
            return self._default_scopes.split()
        return []


class Grant(db.Model, BaseMixin):
    __tablename__ = 'grant'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    client_id = db.Column(db.Unicode(40), db.ForeignKey('client.client_id'), nullable=False)
    code = db.Column(db.Unicode(255), nullable=False)
    redirect_uri = db.Column(db.Unicode(255))
    expires = db.Column(db.DateTime)
    _scopes = db.Column(db.Text)

    user = db.relationship('User')
    client = db.relationship('Client')

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []


class Token(db.Model, BaseMixin):
    __tablename__ = 'token'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    client_id = db.Column(db.Unicode(40), db.ForeignKey('client.client_id'), nullable=False)
    token_type = db.Column(db.Unicode(40))
    access_token = db.Column(db.Unicode(255), unique=True)
    refresh_token = db.Column(db.Unicode(255), unique=True)
    expires = db.Column(db.DateTime)
    _scopes = db.Column(db.Text)

    client = db.relationship('Client')
    user = db.relationship('User')

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []
