import functools

from flask import (
    Blueprint, g, redirect, request, session, url_for
)

from db.models import Organisation, Account, Review, Interview


orgs = Blueprint('orgs', __name__, url_prefix='/orgs')

@orgs.route('/', methods=['GET'])
def get_orgs():
    org_names = g.session.query(Organisation.name).all()
    return str(org_names)

@orgs.route('/<int:org_id>', methods=['GET'])
def get_org(org_id):
    org = g.session.query(Organisation).filter(Organisation.id == org_id).scalar()
    return str(org)

@orgs.route('/<int:org_id>/reviews', methods=['GET'])
def get_org_reviews(org_id):
    org = g.session.query(Organisation).filter(Organisation.id == org_id).all()
    return str(org.reviews)

@orgs.route('/<int:org_id>/interviews', methods=['GET'])
def get_org_interviews(org_id):
    org = g.session.query(Organisation).filter(Organisation.id == org_id).all()
    return str(org.interviews)

@orgs.route('/<int:org_id>/reviews_for_position', methods=['GET'])
def get_org_reviews_for_position(org_id):
    position = request.args.get('position', type=str)
    # TODO: filter for position and reviews at company
    reviews = g.session.query(Review).filter(Review.org_id == org_id).all()
    return str(reviews) + position

@orgs.route('/<int:org_id>/interviews_for_position', methods=['GET'])
def get_org_interviews_for_position(org_id):
    position = request.args.get('position', type=str)
    # TODO: filter for position and interview at company
    interviews = g.session.query(Interview).filter(Interview.org_id == org_id).all()
    return str(interviews) + position

@orgs.route('/<int:org_id>/salary_info', methods=['GET'])
def get_org_salary_info(org_id):
    # TODO: build a nice query that aggregates salary info for us for a given
    # company and position
    org = g.session.query(Organisation).filter(Organisation.id == org_id).all()
    return str(org.interviews)


account = Blueprint('account', __name__, url_prefix='/account')

@account.route('/<int:account_id>', methods=['GET'])
def get_account(account_id):
    account = g.session.query(Account).filter(Account.id == account_id).scalar()
    return str(account)

@account.route('/<int:account_id>/reviews', methods=['GET'])
def get_account_reviews(account_id):
    account = g.session.query(Account).filter(Account.id == account_id).scalar()
    return str(account.reviews)

@account.route('/<int:account_id>/interviews', methods=['GET'])
def get_account_interviews(account_id):
    account = g.session.query(Account).filter(Account.id == account_id).scalar()
    return str(account.interviews)

@account.route('/<int:account_id>/review_votes', methods=['GET'])
def get_account_review_votes(account_id):
    account = g.session.query(Account).filter(Account.id == account_id).scalar()
    return str(account.review_votes)

@account.route('/<int:account_id>/interview_votes', methods=['GET'])
def get_account_interview_votes(account_id):
    account = g.session.query(Account).filter(Account.id == account_id).scalar()
    return str(account.interview_votes)
