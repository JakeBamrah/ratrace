import enum
from collections import Counter

from sqlalchemy import Column, Integer, Float, String, Enum, Index, ForeignKey, text
from sqlalchemy.orm import relationship, validates
from sqlalchemy.ext.hybrid import hybrid_property

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
    BUSINSS_CONSULTING_MANAGEMENT = 'Business, Consulting and Management'
    ACCOUNTANCY_BANKING_FINANCE = 'Accountancy, Banking and Finance'

class Currency(enum.Enum):
    GBP = 'gbp'
    USD = 'usd'
    EUR = 'eur'
    JPY = 'jpy'
    CNY = 'cny'

class Vote(enum.Enum):
    DOWNVOTE = 'downvote'
    UPVOTE = 'upvote'


EPOCH_QUERY = "(select strftime('%s', 'now'))"

class User(db.Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(32), unique=True, nullable=False)
    password = Column(String(64), nullable=False)
    created_at = Column(Integer, default=text(EPOCH_QUERY), nullable=False)
    updated_at = Column(Integer, default=text(EPOCH_QUERY), onupdate=text(EPOCH_QUERY))
    reviews = relationship('Review', backref='user', lazy=True)
    interviews = relationship('Interview', backref='user', lazy=True)
    interview_votes = relationship('InterviewVote', backref='user', lazy=True)
    review_votes = relationship('ReviewVote', backref='user', lazy=True)

    def __repr__(self):
        return (f"<User({self.id})>")

user_username_idx = Index('user_username_idx', User.username)


class Organisation(db.Base):
    __tablename__ = 'organisation'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(32), nullable=False)
    url = Column(String, unique=True)
    size = Column(Integer, default=1, nullable=False)
    industry = Column(Enum(Industry), nullable=False)
    created_at = Column(Integer, default=text(EPOCH_QUERY), nullable=False)
    updated_at = Column(Integer, default=text(EPOCH_QUERY), onupdate=text(EPOCH_QUERY))
    reviews = relationship('Review', backref='organisation', lazy=True)
    interviews = relationship('Interview', backref='organisation', lazy=True)

    def __repr__(self):
        return (f"<Organisation({self.id})>")

organisation_size_idx = Index('organisation_size_idx', Organisation.size)
organisation_industry_idx = Index('organisation_industry_idx', Organisation.industry)


class Review(db.Base):
    __tablename__ = 'review'

    id = Column(Integer, primary_key=True, nullable=False)
    position = Column(String(32), nullable=False)
    salary = Column(Integer, default=0, nullable=False)
    currency = Column(Enum(Currency), default=Currency.USD, nullable=False)
    location = Column(String, nullable=False)
    duration_years = Column(Float, default=1, nullable=False)
    review = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    org_id = Column(Integer, ForeignKey('organisation.id'), nullable=False)
    created_at = Column(Integer, default=text(EPOCH_QUERY), nullable=False)
    updated_at = Column(Integer, default=text(EPOCH_QUERY), onupdate=text(EPOCH_QUERY))
    review_votes = relationship('ReviewVote', backref='review', lazy=True)

    def __repr__(self):
        return (f"<Review({self.id})>")

    @hybrid_property
    def vote_count(self):
        return Counter(i.vote.value for i in self.review_votes)

review_user_idx = Index('review_user_idx', Review.user_id)
review_org_idx = Index('review_org_idx', Review.org_id)
review_salary_idx = Index('review_salary_idx', Review.salary)


class Interview(db.Base):
    __tablename__ = 'interview'

    id = Column(Integer, primary_key=True, nullable=False)
    position = Column(String(32), nullable=False)
    location = Column(String, nullable=False)
    interview = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    org_id = Column(Integer, ForeignKey('organisation.id'), nullable=False)
    created_at = Column(Integer, default=text(EPOCH_QUERY), nullable=False)
    updated_at = Column(Integer, default=text(EPOCH_QUERY), onupdate=text(EPOCH_QUERY))
    interview_votes = relationship('InterviewVote', backref='interview', lazy=True)

    def __repr__(self):
        return (f"<Interview({self.id})>")

    @hybrid_property
    def vote_count(self):
        return Counter(i.vote.value for i in self.interview_votes)

interview_user_idx = Index('interview_user_idx', Interview.user_id)
interview_org_idx = Index('interview_org_idx', Interview.org_id)


class InterviewVote(db.Base):
    __tablename__ = 'interview_vote'

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    interview_id = Column(Integer, ForeignKey('interview.id'), nullable=False)
    vote = Column(Enum(Vote), nullable=False)
    created_at = Column(Integer, default=text(EPOCH_QUERY), nullable=False)
    updated_at = Column(Integer, default=text(EPOCH_QUERY), onupdate=text(EPOCH_QUERY))

    def __repr__(self):
        return (f"<InterviewVote({self.id})>")

interview_vote_user_idx = Index('interview_vote_user_idx', InterviewVote.user_id)
interview_vote_interview_idx = Index('interview_vote_interview_idx', InterviewVote.interview_id)


class ReviewVote(db.Base):
    __tablename__ = 'review_vote'

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    review_id = Column(Integer, ForeignKey('review.id'), nullable=False)
    vote = Column(Enum(Vote), nullable=False)
    created_at = Column(Integer, default=text(EPOCH_QUERY), nullable=False)
    updated_at = Column(Integer, default=text(EPOCH_QUERY), onupdate=text(EPOCH_QUERY))

    def __repr__(self):
        return (f"<ReviewVote({self.id})>")

review_vote_user_idx = Index('review_vote_user_idx', ReviewVote.user_id)
review_vote_review_idx = Index('review_vote_review_idx', ReviewVote.review_id)
