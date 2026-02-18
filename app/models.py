from app import db
from flask_security import UserMixin, RoleMixin
from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Float, DateTime, ForeignKey

"""
STEP 4: app/models.py - Definiera dina databastabeller

Models är Python-klasser som representerar tabeller i databasen.
SQLAlchemy konverterar dessa klasser till SQL automatiskt.

Vi använder mapped_column - det moderna sättet (SQLAlchemy 2.0+)
"""

# TODO 1: Importera vad du behöver
# - from app import db
# - from flask_login import UserMixin
# - from datetime import datetime
# - from sqlalchemy.orm import mapped_column
# - from sqlalchemy import String, Integer, Float, DateTime, ForeignKey

# TODO 2: Skapa User-modellen

user_roles = db.Table('user_roles',
                      db.Column('user_id', db.Integer, db.ForeignKey(
                          'users.id'), primary_key=True),
                      db.Column('role_id', db.Integer, db.ForeignKey(
                          'role.id'), primary_key=True)
                      )


class Role(db.Model):
    __tablename__ = 'role'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)

    def __repr__(self):
        return f'<Role {self.name}>'


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(80), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False, index=True)
    password: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(
        timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    fs_uniquifier: Mapped[str] = mapped_column(
        String(64), unique=True, nullable=False)

    active: Mapped[bool] = mapped_column(default=True)

    roles = db.relationship('Role', secondary=user_roles, backref=('users'))

    watched_assets = db.relationship(
        'Asset', secondary='user_assets', backref='followers')

    def __repr__(self):
        return f'<User {self.username}>'
    # __repr__:
    #     return f'<User {self.username}>'


class Asset(db.Model):
    __tablename__ = 'assets'

    id: Mapped[int] = mapped_column(primary_key=True)
    coingecko_id: Mapped[str] = mapped_column(
        String(80), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    symbol: Mapped[str] = mapped_column(String(20), nullable=False)
    current_price: Mapped[float | None] = mapped_column(Float, nullable=True)
    last_updated: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc))

    price_history = db.relationship(
        'PriceHistory', backref='asset', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Asset {self.symbol}>'
    # __repr__:
    # - return f'<Asset {self.symbol}>'


class PriceHistory(db.Model):
    __tablename__ = 'price_history'

    id: Mapped[int] = mapped_column(primary_key=True)
    asset_id: Mapped[int] = mapped_column(
        ForeignKey('assets.id'), nullable=False, index=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    volume: Mapped[float | None] = mapped_column(Float, nullable=True)
    market_cap: Mapped[float | None] = mapped_column(Float, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    def __repr__(self):
        return f'<PriceHistory {self.asset_id} @ {self.timestamp}>'

    # __repr__:
    # - return f'<PriceHistory {self.asset_id} @ {self.timestamp}>'

# TODO 5: Skapa user_assets association table


user_assets = db.Table('user_assets',
                       db.Column('user_id', db.Integer, db.ForeignKey(
                           'users.id'), primary_key=True),
                       db.Column('asset_id', db.Integer, db.ForeignKey(
                           'assets.id'), primary_key=True),
                       db.Column('added_at', db.DateTime,
                                 default=lambda: datetime.now(timezone.utc))
                       )

"""
FÖRKLARING av mapped_column:
- Mapped[int] = typhin för Python (int, str, float, datetime, etc)
- mapped_column(...) = SQLAlchemy kolumndefinition
- String(80) = Max 80 tecken
- Float = Decimaltal
- DateTime = Datum och tid
- ForeignKey('assets.id') = Referens till annan tabell
- nullable=True/False = Kan värdet vara tomt?
- unique=True = Måste värdet vara unikt?
- index=True = Snabbar upp sökningar
- default=datetime.utcnow = Standardvärde

VALET | syntax:
- float | None = "float eller None" (nullable)
"""
