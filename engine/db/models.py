import enum

from sqlalchemy import (
        Column, Integer, Float, String, Enum, Index, ForeignKey, text, Boolean)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from werkzeug.security import generate_password_hash, check_password_hash

from . import database as db


class Industry(enum.Enum):
    TRANSPORT_AND_LOGISTICS = 'Transport and Logistics'
    EDUCATION = 'Education'
    SALES = 'Sales'
    SCIENCE_AND_PHARMACEUTICALS = 'Science and Pharmaceuticals'
    SOCIAL_CARE = 'Social care'
    RETAIL = 'Retail'
    RECRUITMENT_AND_HR = 'Recruitment and HR'
    PUBLIC_SERVICES = 'Public services'
    PROPERTY_AND_CONSTRUCTION = 'Property and Construction'
    MEDIA_AND_INTERNET = 'Media and Internet'
    MARKETING_ADVERTISING_AND_PR = 'Marketing, Advertising and PR'
    LEISURE_SPORTS_AND_TOURISM = 'Leisure, Sports and Tourism'
    LAW_ENFORCEMENT_AND_SECURITY = 'Law Enforcement and Security'
    LAW = 'Law'
    INFORMATION_TECHONOLOGY = 'I.T'
    HOSPITALITY = 'Hospitality'
    ENGINEERING_AND_MANUFACTURING = 'Engineering and Manufacturing'
    ENERGY_AND_UTILITIES = 'Energy and Utilities'
    CREATIVE_ARTS_AND_DESIGN = 'Creative Arts and Design'
    CHARITY_AND_VOLUNTARY_WORK = 'Charity and Voluntary Work'
    BUSINESS_CONSULTING_MANAGEMENT = 'Business, Consulting and Management'
    ACCOUNTANCY_BANKING_FINANCE = 'Accountancy, Banking and Finance'

class Currency(enum.Enum):
    GBP = 'gbp'
    USD = 'usd'
    EUR = 'eur'
    JPY = 'jpy'
    CNY = 'cny'

class Vote(enum.Enum):
    UPVOTE = 1
    DOWNVOTE = -1

class ReviewTag(enum.Enum):
    GOOD = 'good'
    AVERAGE = 'average'
    BAD = 'bad'

class AccountStatus(enum.Enum):
    ACTIVE = 'active'
    SUSPENDED = 'suspended'
    INACTIVE = 'inactive'

class AccountType(enum.Enum):
    USER = 'user'
    ADMIN = 'admin'


EPOCH_QUERY = "(select strftime('%s', 'now'))"

class Account(db.Base):
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(32), unique=True, nullable=False)
    created_at = Column(Integer, default=text(EPOCH_QUERY), nullable=False)
    updated_at = Column(Integer, default=text(EPOCH_QUERY), onupdate=text(EPOCH_QUERY))
    status = Column(Enum(AccountStatus), default=AccountStatus.ACTIVE, nullable=False)
    type = Column(Enum(AccountType), default=AccountType.USER, nullable=False)
    anonymous = Column(Boolean, default=False)
    dark_mode = Column(Boolean, default=False)
    password = Column(String(64), nullable=False)
    reviews = relationship('Review', backref='account', lazy=True)
    interviews = relationship('Interview', backref='account', lazy=True)
    interview_votes = relationship('InterviewVote', backref='account', lazy=True)
    review_votes = relationship('ReviewVote', backref='account', lazy=True)

    def __repr__(self):
        return (f"<Account({self.id})>")

    @hybrid_property
    def is_active(self):
        return self.status == AccountStatus.ACTIVE

    @hybrid_method
    def check_password(self, password):
        return check_password_hash(str(self.password), password)

    @hybrid_method
    def add_password(self, password):
        self.password = generate_password_hash(password, method='sha256')


account_username_idx = Index('account_username_idx', Account.username)


class Organisation(db.Base):
    __tablename__ = 'organisation'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(32), nullable=False)
    url = Column(String, unique=True)
    size = Column(Integer, default=1, nullable=False)
    headquarters = Column(String(32), nullable=False)
    industry = Column(Enum(Industry), nullable=False)
    created_at = Column(Integer, default=text(EPOCH_QUERY), nullable=False)
    updated_at = Column(Integer, default=text(EPOCH_QUERY), onupdate=text(EPOCH_QUERY))
    reviews = relationship('Review', backref='organisation', lazy=True)
    interviews = relationship('Interview', backref='organisation', lazy=True)
    positions = relationship('Position', backref='organisation', lazy=True)
    page_visits = Column(Integer, default=1)

    def __repr__(self):
        return (f"<Organisation({self.id})>")

    @hybrid_property
    def total_reviews(self):
        return len(self.reviews)

    @hybrid_property
    def total_interviews(self):
        return len(self.interviews)

organisation_size_idx = Index('organisation_size_idx', Organisation.size)
organisation_industry_idx = Index('organisation_industry_idx', Organisation.industry)


class Position(db.Base):
    __tablename__ = 'position'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(32), nullable=False)
    created_at = Column(Integer, default=text(EPOCH_QUERY), nullable=False)
    updated_at = Column(Integer, default=text(EPOCH_QUERY), onupdate=text(EPOCH_QUERY))
    org_id = Column(Integer, ForeignKey('organisation.id'), nullable=False)
    reviews = relationship('Review', backref='position', lazy=True)
    interviews = relationship('Interview', backref='position', lazy=True)

    def __repr__(self):
        return (f"<Position({self.id})>")

    @hybrid_property
    def total_reviews(self):
        return len(self.reviews)

    @hybrid_property
    def total_interviews(self):
        return len(self.interviews)

position_org_idx = Index('position_org_idx', Position.org_id)


class Review(db.Base):
    __tablename__ = 'review'

    id = Column(Integer, primary_key=True, nullable=False)
    salary = Column(Integer, default=0, nullable=False)
    currency = Column(Enum(Currency), default=Currency.USD, nullable=False)
    location = Column(String, nullable=False)
    duration_years = Column(Float, default=1, nullable=False)
    review = Column(String, nullable=False)
    account_id = Column(Integer, ForeignKey('account.id'), nullable=False)
    org_id = Column(Integer, ForeignKey('organisation.id'), nullable=False)
    position_id = Column(Integer, ForeignKey('position.id'), nullable=False)
    created_at = Column(Integer, default=text(EPOCH_QUERY), nullable=False)
    updated_at = Column(Integer, default=text(EPOCH_QUERY), onupdate=text(EPOCH_QUERY))
    votes = relationship('ReviewVote', backref='review', lazy=True)
    tag = Column(Enum(ReviewTag), default=ReviewTag.AVERAGE)

    def __repr__(self):
        return (f"<Review({self.id})>")

    @hybrid_property
    def upvotes(self):
        return [i.account_id for i in self.votes if i.vote == Vote.UPVOTE.value]

    @hybrid_property
    def downvotes(self):
        return [i.account_id for i in self.votes if i.vote == Vote.DOWNVOTE.value]

review_account_idx = Index('review_account_idx', Review.account_id)
review_org_idx = Index('review_org_idx', Review.org_id)
review_salary_idx = Index('review_salary_idx', Review.salary)
review_position_idx = Index('review_position_idx', Review.position_id)


class Interview(db.Base):
    __tablename__ = 'interview'

    id = Column(Integer, primary_key=True, nullable=False)
    location = Column(String, nullable=False)
    offer = Column(Integer, default=0)
    currency = Column(Enum(Currency), default=Currency.USD, nullable=False)
    interview = Column(String, nullable=False)
    account_id = Column(Integer, ForeignKey('account.id'), nullable=False)
    org_id = Column(Integer, ForeignKey('organisation.id'), nullable=False)
    position_id = Column(Integer, ForeignKey('position.id'), nullable=False)
    created_at = Column(Integer, default=text(EPOCH_QUERY), nullable=False)
    updated_at = Column(Integer, default=text(EPOCH_QUERY), onupdate=text(EPOCH_QUERY))
    votes = relationship('InterviewVote', backref='interview', lazy=True)
    tag = Column(Enum(ReviewTag), default=ReviewTag.AVERAGE)

    def __repr__(self):
        return (f"<Interview({self.id})>")

    @hybrid_property
    def upvotes(self):
        return [i.account_id for i in self.votes if i.vote == Vote.UPVOTE.value]

    @hybrid_property
    def downvotes(self):
        return [i.account_id for i in self.votes if i.vote == Vote.DOWNVOTE.value]

interview_account_idx = Index('interview_account_idx', Interview.account_id)
interview_org_idx = Index('interview_org_idx', Interview.org_id)
interview_offer_idx = Index('interview_offer_idx', Interview.offer)
interview_position_idx = Index('interview_position_idx', Interview.position_id)


class InterviewVote(db.Base):
    __tablename__ = 'interview_vote'

    id = Column(Integer, primary_key=True, nullable=False)
    account_id = Column(Integer, ForeignKey('account.id'), nullable=False)
    interview_id = Column(Integer, ForeignKey('interview.id'), nullable=False)
    vote = Column(Integer, default=0, nullable=False)
    created_at = Column(Integer, default=text(EPOCH_QUERY), nullable=False)
    updated_at = Column(Integer, default=text(EPOCH_QUERY), onupdate=text(EPOCH_QUERY))

    def __repr__(self):
        return (f"<InterviewVote({self.id})>")

interview_vote_account_idx = Index('interview_vote_account_idx', InterviewVote.account_id)
interview_vote_interview_idx = Index('interview_vote_interview_idx', InterviewVote.interview_id)


class ReviewVote(db.Base):
    __tablename__ = 'review_vote'

    id = Column(Integer, primary_key=True, nullable=False)
    account_id = Column(Integer, ForeignKey('account.id'), nullable=False)
    review_id = Column(Integer, ForeignKey('review.id'), nullable=False)
    vote = Column(Integer, default=0, nullable=False)
    created_at = Column(Integer, default=text(EPOCH_QUERY), nullable=False)
    updated_at = Column(Integer, default=text(EPOCH_QUERY), onupdate=text(EPOCH_QUERY))

    def __repr__(self):
        return (f"<ReviewVote({self.id})>")

review_vote_account_idx = Index('review_vote_account_idx', ReviewVote.account_id)
review_vote_review_idx = Index('review_vote_review_idx', ReviewVote.review_id)
