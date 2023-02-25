from flask import (
    Blueprint, g, request, url_for
)

import json

from db.models import Organisation, Account, Review, Interview, ReviewVote, InterviewVote
import db.schemas as schemas


orgs = Blueprint('orgs', __name__, url_prefix='/orgs')

@orgs.route('/', methods=['GET'])
def get_orgs():
    org_names = [{'id': o.id, 'name': o.name} for o in g.session.query(Organisation).all()]
    response = dict(response=200, data=org_names)
    return json.dumps(response)

@orgs.route('/search', methods=['GET'])
def search_orgs():
    org_name = request.args.get('org_name', type=str, default='')
    # TODO: setup similarity funcion to find positions like given org name
    find_org_q = (g.session
             .query(Organisation)
             .filter(Organisation.name.contains(org_name))
             .limit(20)
    )
    orgs = [{'id': o.id, 'name': o.name} for o in find_org_q.all()]
    response = dict(response=200, data=orgs)
    return json.dumps(response)

@orgs.route('/<int:org_id>', methods=['GET'])
def get_org(org_id):
    org = g.session.query(Organisation).filter(Organisation.id == org_id).scalar()
    limit = request.args.get('limit', type=int, default=50)
    review_sorted_q = (g.session
                .query(Review)
                .filter(Review.org_id == org_id)
                .order_by(Review.created_at.desc())
                .limit(limit))

    data = dict(
            org = schemas.OrganisationSchema(exclude=('interviews', 'reviews')).dump(org),
            reviews = schemas.ReviewSchema().dump(review_sorted_q, many=True)
        )
    return json.dumps(dict(response=200, data=data))

@orgs.route('/<int:org_id>/reviews', methods=['GET'])
def get_org_reviews(org_id):
    limit = request.args.get('limit', type=int, default=50)
    review_sorted_q = (g.session
                .query(Review)
                .filter(Review.org_id == org_id)
                .order_by(Review.created_at.desc())
                .limit(limit))

    data = dict(reviews = schemas.ReviewSchema().dump(review_sorted_q, many=True))
    return json.dumps(dict(response=200, data=data))

@orgs.route('/<int:org_id>/interviews', methods=['GET'])
def get_org_interviews(org_id):
    limit = request.args.get('limit', type=int, default=50)
    interview_sorted_q = (g.session
                   .query(Interview)
                   .filter(Interview.org_id == org_id)
                   .order_by(Interview.created_at.desc())
                   .limit(limit))

    data = dict(interviews = schemas.InterviewSchema().dump(interview_sorted_q, many=True))
    return json.dumps(dict(response=200, data=data))

@orgs.route('/<int:org_id>/reviews_for_position', methods=['GET'])
def get_org_reviews_for_position(org_id):
    position = request.args.get('position', type=str, default='')
    limit = request.args.get('limit', type=int, default=50)
    # TODO: setup similarity funcion to find positions like given position
    review_sorted_q = (g.session
                .query(Review)
                .filter(
                    (Review.org_id == org_id) &
                    (Review.position.contains(position.lower()))
                )
                .order_by(Review.created_at.desc())
                .limit(limit))
    data = dict(reviews = schemas.ReviewSchema().dump(review_sorted_q, many=True))
    return json.dumps(dict(response=200, data=data))

@orgs.route('/<int:org_id>/interviews_for_position', methods=['GET'])
def get_org_interviews_for_position(org_id):
    position = request.args.get('position', type=str, default='')
    limit = request.args.get('limit', type=int, default=50)
    # TODO: setup similarity funcion to find positions like given position
    interview_sorted_q = (g.session
                .query(Interview)
                .filter(
                    (Interview.org_id == org_id) &
                    (Interview.position.contains(position.lower()))
                )
                .order_by(Interview.created_at.desc())
                .limit(limit))
    data = dict(interviews = schemas.InterviewSchema().dump(interview_sorted_q, many=True))
    return json.dumps(dict(response=200, data=data))

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
    review_sorted_q = (g.session
                .query(Review)
                .filter(Review.account_id == account_id)
                .order_by(Review.created_at.desc())
                .limit(5))
    data = dict(
            account = schemas.AccountSchema(exclude=('reviews', 'interviews')).dump(account),
            reviews = schemas.ReviewSchema().dump(review_sorted_q, many=True)
        )
    return json.dumps(dict(response=200, data=data))

@account.route('/<int:account_id>/reviews', methods=['GET'])
def get_account_reviews(account_id):
    limit = request.args.get('limit', type=int, default=50)
    review_sorted_q = (g.session
                .query(Review)
                .filter(Review.account_id == account_id)
                .order_by(Review.created_at.desc())
                .limit(limit))
    data = dict(reviews = schemas.ReviewSchema().dump(review_sorted_q, many=True))
    return json.dumps(dict(response=200, data=data))

@account.route('/<int:account_id>/interviews', methods=['GET'])
def get_account_interviews(account_id):
    limit = request.args.get('limit', type=int, default=50)
    interview_sorted_q = (g.session
                .query(Interview)
                .filter(Interview.account_id == account_id)
                .order_by(Interview.created_at.desc())
                .limit(limit))
    data = dict(interviews = schemas.InterviewSchema().dump(interview_sorted_q, many=True))
    return json.dumps(dict(response=200, data=data))

@account.route('/<int:account_id>/review_votes', methods=['GET'])
def get_account_review_votes(account_id):
    review_votes_sorted_q = (g.session
                .query(ReviewVote)
                .filter(ReviewVote.account_id == account_id)
                .order_by(ReviewVote.created_at.desc()))

    data = dict(review_votes = schemas.ReviewVoteSchema(
        exclude=['updated_at']).dump(review_votes_sorted_q, many=True))
    return json.dumps(dict(response=200, data=data))

@account.route('/<int:account_id>/interview_votes', methods=['GET'])
def get_account_interview_votes(account_id):
    review_votes_sorted_q = (g.session
                .query(InterviewVote)
                .filter(InterviewVote.account_id == account_id)
                .order_by(InterviewVote.created_at.desc()))

    data = dict(interview_votes = schemas.InterviewVoteSchema(
                exclude=['updated_at']).dump(review_votes_sorted_q, many=True))
    return json.dumps(dict(response=200, data=data))
