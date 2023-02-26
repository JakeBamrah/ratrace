from flask import (
    Blueprint, g, request, url_for, jsonify
)

from db.models import Organisation, Account, Review, Interview, ReviewVote, InterviewVote
import db.schemas as schemas


orgs = Blueprint('orgs', __name__, url_prefix='/orgs')

@orgs.route('/', methods=['GET'])
def get_orgs():
    org_names = [{'id': o.id, 'name': o.name} for o in g.session.query(Organisation).all()]
    return jsonify(response=200, data=org_names)


@orgs.route('/search', methods=['GET'])
def search_orgs():
    org_name = request.args.get('org_name', type=str, default='')
    # TODO: setup similarity funcion to find positions like given org name
    find_org_q = (g.session
             .query(Organisation)
             .filter(Organisation.name.contains(org_name))
             .limit(20)
    )
    data = [{'id': o.id, 'name': o.name} for o in find_org_q.all()]
    return jsonify(response=200, data=data)


@orgs.route('/<int:org_id>', methods=['GET'])
def get_org(org_id):
    """Get overview, reviews and interviews for organisation."""
    org = g.session.query(Organisation).filter(Organisation.id == org_id).scalar()
    limit = request.args.get('limit', type=int, default=50)
    position = request.args.get('position', type=str, default='')
    review_sorted_q = (g.session
                .query(Review)
                .filter(
                    (Review.org_id == org_id) &
                    (Review.position.contains(position.lower()))
                )
                .order_by(Review.created_at.desc())
                .limit(limit))
    interview_sorted_q = (g.session
                .query(Interview)
                .filter(
                    (Interview.org_id == org_id) &
                    (Interview.position.contains(position.lower()))
                )
                .order_by(Interview.created_at.desc())
                .limit(limit))
    data = dict(
            org = schemas.OrganisationSchema(exclude=('interviews', 'reviews')).dump(org),
            reviews = schemas.ReviewSchema().dump(review_sorted_q, many=True),
            interviews = schemas.InterviewSchema().dump(interview_sorted_q, many=True),
        )
    return jsonify(response=200, data=data)


@orgs.route('/<int:org_id>/reviews', methods=['GET'])
def get_org_reviews(org_id):
    schema = schemas.ReviewSchema()

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
    data = dict(reviews = schema.dump(review_sorted_q, many=True))
    return jsonify(response=200, data=data)


@orgs.route('/<int:org_id>/interviews', methods=['GET'])
def get_org_interviews(org_id):
    schema = schemas.InterviewSchema()

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
    data = dict(interviews = schema.dump(interview_sorted_q, many=True))
    return jsonify(response=200, data=data)


@orgs.route('/<int:org_id>/salary_info', methods=['GET'])
def get_org_salary_info(org_id):
    # TODO: build a nice query that aggregates salary info for us for a given
    # company and position
    org = g.session.query(Organisation).filter(Organisation.id == org_id).all()
    return str(org.interviews)


account = Blueprint('account', __name__, url_prefix='/account')

@account.route('/<int:account_id>', methods=['GET'])
def get_account(account_id):
    account_schema = schemas.AccountSchema(exclude=('reviews', 'interviews'))
    review_schema = schemas.ReviewSchema()

    limit = request.args.get('limit', type=int, default=5)
    account = g.session.query(Account).filter(Account.id == account_id).scalar()
    review_sorted_q = (g.session
                .query(Review)
                .filter(Review.account_id == account_id)
                .order_by(Review.created_at.desc())
                .limit(limit))
    data = dict(
            account = account_schema.dump(account),
            reviews = review_schema.dump(review_sorted_q, many=True)
        )
    return jsonify(response=200, data=data)


@account.route('/<int:account_id>/reviews', methods=['GET'])
def get_account_reviews(account_id):
    review_schema = schemas.ReviewSchema()

    limit = request.args.get('limit', type=int, default=50)
    review_sorted_q = (g.session
                .query(Review)
                .filter(Review.account_id == account_id)
                .order_by(Review.created_at.desc())
                .limit(limit))
    data = dict(reviews = review_schema.dump(review_sorted_q, many=True))
    return jsonify(response=200, data=data)


@account.route('/<int:account_id>/interviews', methods=['GET'])
def get_account_interviews(account_id):
    interview_schema = schemas.InterviewSchema()

    limit = request.args.get('limit', type=int, default=50)
    interview_sorted_q = (g.session
                .query(Interview)
                .filter(Interview.account_id == account_id)
                .order_by(Interview.created_at.desc())
                .limit(limit))
    data = dict(interviews = interview_schema.dump(interview_sorted_q, many=True))
    return jsonify(response=200, data=data)


@account.route('/<int:account_id>/review_votes', methods=['GET'])
def get_account_review_votes(account_id):
    vote_schema = schemas.ReviewVoteSchema( exclude=['updated_at'])
    review_votes_sorted_q = (g.session
                .query(ReviewVote)
                .filter(ReviewVote.account_id == account_id)
                .order_by(ReviewVote.created_at.desc()))

    data = dict(review_votes = vote_schema.dump(review_votes_sorted_q, many=True))
    return jsonify(response=200, data=data)


@account.route('/<int:account_id>/interview_votes', methods=['GET'])
def get_account_interview_votes(account_id):
    vote_schema = schemas.InterviewVoteSchema( exclude=['updated_at'])
    interview_votes_sorted_q = (g.session
                .query(InterviewVote)
                .filter(InterviewVote.account_id == account_id)
                .order_by(InterviewVote.created_at.desc()))

    data = dict(vote_schema.dump(interview_votes_sorted_q, many=True))
    return jsonify(response=200, data=data)
