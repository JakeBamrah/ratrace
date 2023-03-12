import gzip

from flask import Blueprint, g, request, jsonify, json, make_response, session
import pandas as pd
from sqlalchemy import func, desc

from db.models import (
        Organisation, Account, Review, Vote,
        Interview, ReviewVote, InterviewVote,
        VoteTypeModel
)
import db.schemas as schemas


orgs = Blueprint('orgs', __name__, url_prefix='/orgs')

def min_max_scale(df, col):
    """Normalize column values between [0, 1]"""
    return (df[col] - df[col].min()) / (df[col].max() - df[col].min())

def gzippify(data):
    """Compress data and create gzip response"""
    content = gzip.compress(json.dumps(data).encode('utf8'))
    response = make_response(content)
    response.headers['Content-length'] = len(content)
    response.headers['Content-Encoding'] = 'gzip'
    return response

@orgs.route('/get_names', methods=['GET'])
def get_names():
    limit = request.args.get('limit', type=int, default=50)
    offset = request.args.get('offset', type=int, default=0)
    industry = request.args.get('industry', type=str, default=None)
    filter_queries = []
    if industry:
        filter_queries.append(Organisation.industry == industry)

    find_orgs_q = (g.session
                   .query(Organisation.id, Organisation.name,
                        Organisation.page_visits, Organisation.size)
                   .filter(*filter_queries)
                   .offset(offset)
                   .limit(limit))

    # create weight for sorting orgs (w = min_max(size) * min_max(page_visits))
    df = pd.DataFrame(data=find_orgs_q.all(), columns=['id', 'label', 'page_visits', 'size'])
    df['weight'] = round(min_max_scale(df, 'size') * min_max_scale(df, 'page_visits'), 3)
    df = df.sort_values('weight', ascending=False)

    org_names = df[['id', 'label']].to_dict('records')
    return gzippify(org_names)


@orgs.route('/search', methods=['GET'])
def search_orgs():
    # TODO: setup similarity funcion to find positions like given org name
    limit = request.args.get('limit', type=int, default=50)
    offset = request.args.get('offset', type=int, default=0)
    org_name = request.args.get('org_name', type=str, default='')
    industry = request.args.get('industry', type=str, default='')
    queries = [Organisation.name.contains(org_name)]
    if industry and industry != 'ALL':
        queries.append(Organisation.industry == industry)

    find_orgs_q = (g.session
            .query(Organisation)
            .filter(*queries)
            .offset(offset)
            .limit(limit))

    schema = schemas.OrganisationSchema(exclude=('interviews', 'reviews'), many=True)
    orgs = schema.dump(find_orgs_q)
    return jsonify(orgs=orgs)


@orgs.route('/<int:org_id>', methods=['GET'])
def get_org(org_id):
    """Get overview, reviews and interviews for organisation."""
    review_limit = request.args.get('review_limit', type=int, default=50)
    interview_limit = request.args.get('interview_limit', type=int, default=50)
    org = g.session.query(Organisation).filter(Organisation.id == org_id).scalar()

    # increment page_visits for org when selected
    org.page_visits += 1
    g.db_commit(g.session, [org])

    review_sorted_q = (g.session
            .query(Review)
            .filter(Review.org_id == org_id)
            .order_by(Review.created_at.desc())
            .limit(review_limit))
    interview_sorted_q = (g.session
            .query(Interview)
            .filter(Interview.org_id == org_id)
            .order_by(Interview.created_at.desc())
            .limit(interview_limit))

    data = dict(
            org = schemas.OrganisationSchema(exclude=('interviews', 'reviews')).dump(org),
            reviews = schemas.ReviewSchema().dump(review_sorted_q, many=True),
            interviews = schemas.InterviewSchema().dump(interview_sorted_q, many=True),
        )
    return jsonify(org=data)


@orgs.route('/<int:org_id>/reviews_and_interviews', methods=['GET'])
def get_org_reviews_and_interviews(org_id):
    # TODO: setup similarity funcion to find positions like given position
    position_id = request.args.get('position_id', type=int, default=None)
    tag = request.args.get('tag', type=str, default=None)
    sort_order = request.args.get('sort_order', type=str, default=None)
    limit = request.args.get('limit', type=int, default=50)
    offset = request.args.get('offset', type=int, default=0)

    review = g.session.query(Review)
    interview = g.session.query(Interview)

    review_filter_queries = [(Review.org_id == org_id)]
    interview_filter_queries = [(Interview.org_id == org_id)]
    if position_id:
        review_filter_queries.append(Review.position_id == position_id)
        interview_filter_queries.append(Interview.position_id == position_id)
    if tag:
        review_filter_queries.append(Review.tag == tag)
        interview_filter_queries.append(Interview.tag == tag)

    review_order = Review.created_at.desc()
    interview_order = Interview.created_at.desc()
    if sort_order == 'TENURE':
        review_order = Review.duration_years.desc()
    if sort_order == 'COMPENSATION':
        review_order = Review.compensation.desc()
        interview_order = Interview.compensation.desc()

    if sort_order in {'DOWNVOTES', 'UPVOTES'}:
        # upvotes downvotes is a bit special
        # we need to find the vote score for each review in an org and (cte)
        # join this cte vote score table to actual review objects
        review_vote_score_q = (g.session
            .query(
                ReviewVote.review_id.label('review_id'),
                func.sum(ReviewVote.vote).label('vote_count')
            )
            .join( Review, isouter=True)
            .filter(Review.org_id == org_id)
            .group_by(ReviewVote.review_id)).cte('review_vote_count')
        review = g.session.query(Review).join(review_vote_score_q, review_vote_score_q.c.review_id == Review.id, isouter=True)
        review_order = desc(func.coalesce(review_vote_score_q.c.vote_count, 0))

        inter_vote_score_q = (g.session
            .query(
                InterviewVote.interview_id.label('interview_id'),
                func.sum(InterviewVote.vote).label('vote_count')
            )
            .join( Interview, isouter=True)
            .filter(Interview.org_id == org_id)
            .group_by(InterviewVote.interview_id)).cte('interview_vote_count')
        interview = g.session.query(Interview).join(inter_vote_score_q, inter_vote_score_q.c.interview_id == Interview.id, isouter=True)

        if sort_order == 'DOWNVOTES':
            review_order = func.coalesce(review_vote_score_q.c.vote_count, 0)
            interview_order = func.coalesce(inter_vote_score_q.c.vote_count, 0)
        else:
            review_order = desc(func.coalesce(review_vote_score_q.c.vote_count, 0))
            interview_order = desc(func.coalesce(inter_vote_score_q.c.vote_count, 0))


    # for disabling load more reviews button
    max_reviews_for_filter = review.filter(*review_filter_queries).count()
    max_interviews_for_filter = interview.filter(*interview_filter_queries).count()
    review_sorted_q = (review
            .filter(*review_filter_queries)
            .order_by(review_order)
            .offset(offset)
            .limit(limit))
    interview_sorted_q = (interview
            .filter(*interview_filter_queries)
            .order_by(interview_order)
            .offset(offset)
            .limit(limit))

    data = dict(
            reviews = schemas.ReviewSchema().dump(review_sorted_q, many=True),
            no_more_reviews = max_reviews_for_filter <= offset + limit,
            interviews = schemas.InterviewSchema().dump(interview_sorted_q, many=True),
            no_more_interviews = max_interviews_for_filter <= offset + limit
        )
    return jsonify(reviews_and_interviews=data)


@orgs.route('/<int:org_id>/compensation_summary', methods=['GET'])
def get_org_comp_info(org_id):
    # TODO: build a nice query that aggregates comp info for us for a given
    # company and position
    org = g.session.query(Organisation).filter(Organisation.id == org_id).all()
    return str(org.interviews)


auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/login', methods=['POST'])
def login():
    r = request.get_json()
    username = r.get('username', '').lower()
    password = r.get('password', '')

    if not username or not password:
        return jsonify(authenticated=False)

    # check if user actually exists
    account = (g.session
            .query(Account)
            .filter(Account.username == username)
            .scalar())
    if not account or not account.check_password(password):
        return jsonify(authenticated=False)

    session['account_id'] = account.id

    schema = schemas.AccountSchema(only=(['id', 'username', 'anonymous', 'dark_mode']))
    return jsonify(authenticated=True, account=schema.dump(account))


@auth.route('/check_session', methods=['GET'])
def check_session():
    account_id = session.get('account_id')
    schema = schemas.AccountSchema(only=(['id', 'username', 'anonymous', 'dark_mode']))

    data = None
    if account_id:
        account = (g.session
                .query(Account)
                .filter(Account.id == account_id)
                .scalar())
        data = schema.dump(account)
        session.clear()
        session['account_id'] = account_id

    return jsonify(authenticated=bool(account_id), account=data)


@auth.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return jsonify(authenticated=False)


@auth.route('/signup', methods=['POST'])
def signup():
    r = request.get_json()
    username = r.get('username', '').lower()
    password = r.get('password', '')

    error_message = None
    if not username or not password or len(password) < 8:
        error_message = "Username or password not given"
        return jsonify(error=error_message)

    # check if user actually exists
    account = (g.session
            .query(Account)
            .filter(Account.username == username)
            .scalar())
    if account:
        error_message = "Account already exists"
        return jsonify(error=error_message)

    # create user and attempt to commit user
    new_account = Account(username=username)
    new_account.add_password(password)

    account_created = g.db_commit(g.session, [new_account])
    if not account_created:
        error_message = "Failed to create account"

    # add account id to the session so session can be checked on re-direct
    session['account_id'] = new_account.id
    schema = schemas.AccountSchema(only=(['id', 'username', 'anonymous', 'dark_mode']))

    return jsonify(error=error_message, account=schema.dump(new_account))


account = Blueprint('account', __name__, url_prefix='/account')

@account.route('/reviews', methods=['POST'])
def get_account_reviews():
    r = request.get_json()
    limit = r.get('limit', 10)
    account_id = r.get('account_id')
    review_sorted_q = (g.session
            .query(Review)
            .filter(Review.account_id == account_id)
            .order_by(Review.created_at.desc())
            .limit(limit))

    schema = schemas.ReviewSchema()
    data = dict(reviews = schema.dump(review_sorted_q, many=True))
    return jsonify(data=data)


@account.route('/interviews', methods=['POST'])
def get_account_interviews():
    r = request.get_json()
    limit = r.get('limit', 10)
    account_id = r.get('account_id')
    interview_sorted_q = (g.session
            .query(Interview)
            .filter(Interview.account_id == account_id)
            .order_by(Interview.created_at.desc())
            .limit(limit))

    schema = schemas.InterviewSchema()
    data = dict(interviews = schema.dump(interview_sorted_q, many=True))
    return jsonify(data=data)


@account.route('/vote', methods=['PUT'])
def review_vote():
    """Handles creating new upvotes and downvotes for ReviewVote and
    InterviewVote objects. Existing votes are updated if a user changes it from
    a positive to a negative vote."""
    r = request.get_json()
    post_id = r.get('post_id', None)
    raw_vote = r.get('vote', None)
    already_upvoted = r.get('already_upvoted', False)
    already_downvoted = r.get('already_downvoted', False)
    vote_model_type = r.get('vote_model_type', VoteTypeModel.REVIEW)

    account_id = session.get('account_id')

    error_message=None
    if not account_id:
        error_message = "Not authenticated"
    if not raw_vote:
        error_message = "Invalid vote"

    # figure out which model we are dealing with and update filters from there
    VoteModel = ReviewVote
    filters = [(VoteModel.review_id == post_id)]
    id_key = 'review_id'
    vote = Vote.DOWNVOTE.value if raw_vote < 0 else Vote.UPVOTE.value
    if vote_model_type == VoteTypeModel.INTERVIEW.value:
        VoteModel = InterviewVote
        filters = [(VoteModel.interview_id == post_id)]
        id_key = 'interview_id'

    vote_created = False
    filters.append(VoteModel.account_id == account_id)
    if already_upvoted or already_downvoted:
        # find existing vote and update it
        vote_obj = g.session.query(VoteModel).filter(*filters).scalar()
        vote_obj.vote = vote
        vote_created = g.db_commit(g.session, [vote_obj])
    else:
        # no previous votes for this review, create a new vote object
        params = {'account_id': account_id, 'vote': vote}
        params[id_key] = post_id
        vote_obj = VoteModel(**params)
        vote_created = g.db_commit(g.session, [vote_obj])

    if not vote_created:
        error_message = "Failed to create vote"

    return jsonify(vote_created=vote_created, error=error_message)
