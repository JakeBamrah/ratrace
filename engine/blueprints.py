import gzip

from flask import Blueprint, g, request, jsonify, json, make_response, session
import pandas as pd
from sqlalchemy import func, desc

from db.models import (
        Organisation, Account, Review, Vote,
        Interview, ReviewVote, InterviewVote,
        PostTypeModel, Position
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

@orgs.route('/get-names', methods=['GET'])
def get_names():
    limit = request.args.get('limit', type=int, default=50)
    offset = request.args.get('offset', type=int, default=0)
    industry = request.args.get('industry', type=str, default=None)
    filter_queries = [Organisation.verified == True]
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
    return jsonify(orgs)


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
    return jsonify(data)


@orgs.route('/<int:org_id>/reviews', methods=['GET'])
def get_org_reviews(org_id):
    position_id = request.args.get('position_id', type=int, default=None)
    tag = request.args.get('tag', type=str, default=None)
    sort_order = request.args.get('sort_order', type=str, default=None)
    limit = request.args.get('limit', type=int, default=50)
    offset = request.args.get('offset', type=int, default=0)

    review = g.session.query(Review)
    filter_queries = [(Review.org_id == org_id)]
    if position_id:
        filter_queries.append(Review.position_id == position_id)
    if tag:
        filter_queries.append(Review.tag == tag)

    order_by = Review.created_at.desc()
    if sort_order == 'TENURE':
        order_by = Review.duration_years.desc()
    if sort_order == 'COMPENSATION':
        order_by = Review.compensation.desc()

    if sort_order in {'DOWNVOTES', 'UPVOTES'}:
        # upvotes downvotes is a bit special
        # we need to find the vote score for each review in an org via (cte)
        # join this cte vote score table to actual review objects
        review_vote_score_q = (g.session
            .query(
                ReviewVote.review_id.label('review_id'),
                func.sum(ReviewVote.vote).label('vote_count')
            )
            .join( Review, isouter=True)
            .filter(Review.org_id == org_id)
            .group_by(ReviewVote.review_id)).cte('review_vote_count')
        review = (g.session
            .query(Review)
            .join(
                review_vote_score_q,
                review_vote_score_q.c.review_id == Review.id, isouter=True
            ))
        order_by = desc(func.coalesce(review_vote_score_q.c.vote_count, 0))
        if sort_order == 'DOWNVOTES':
            order_by = func.coalesce(review_vote_score_q.c.vote_count, 0)
        else:
            order_by = desc(func.coalesce(review_vote_score_q.c.vote_count, 0))


    # for disabling load more reviews button
    max_reviews_for_filter = review.filter(*filter_queries).count()
    review_sorted_q = (review
            .filter(*filter_queries)
            .order_by(order_by)
            .offset(offset)
            .limit(limit))

    data = dict(
            posts = schemas.ReviewSchema().dump(review_sorted_q, many=True),
            max_reached = max_reviews_for_filter <= offset + limit,
        )
    return jsonify(data)


@orgs.route('/<int:org_id>/interviews', methods=['GET'])
def get_org_interviews(org_id):
    position_id = request.args.get('position_id', type=int, default=None)
    tag = request.args.get('tag', type=str, default=None)
    sort_order = request.args.get('sort_order', type=str, default=None)
    limit = request.args.get('limit', type=int, default=50)
    offset = request.args.get('offset', type=int, default=0)

    interview = g.session.query(Interview)

    filter_queries = [(Interview.org_id == org_id)]
    if position_id:
        filter_queries.append(Interview.position_id == position_id)
    if tag:
        filter_queries.append(Interview.tag == tag)

    order_by = Interview.created_at.desc()
    if sort_order == 'STAGES':
        order_by = Interview.stages.desc()
    if sort_order == 'COMPENSATION':
        order_by = Interview.compensation.desc()

    if sort_order in {'DOWNVOTES', 'UPVOTES'}:
        # upvotes downvotes is a bit special
        # we need to find the vote score for each review in an org via (cte)
        # join this cte vote score table to actual review objects
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
            order_by = func.coalesce(inter_vote_score_q.c.vote_count, 0)
        else:
            order_by = desc(func.coalesce(inter_vote_score_q.c.vote_count, 0))

    # for disabling load more reviews button
    max_interviews_for_filter = interview.filter(*filter_queries).count()
    interview_sorted_q = (interview
            .filter(*filter_queries)
            .order_by(order_by)
            .offset(offset)
            .limit(limit))

    data = dict(
            posts = schemas.InterviewSchema().dump(interview_sorted_q, many=True),
            max_reached = max_interviews_for_filter <= offset + limit
        )
    return jsonify(data)


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
        return jsonify(authenticated=False, error="Details not given")

    # check if user actually exists
    account = (g.session
            .query(Account)
            .filter(Account.username == username)
            .scalar())
    if not account or not account.check_password(password):
        return jsonify(authenticated=False, error="Incorrect log in details")

    session['account_id'] = account.id

    schema = schemas.AccountSchema(only=(['id', 'username', 'anonymous', 'dark_mode']))
    return jsonify(authenticated=True, account=schema.dump(account))


@auth.route('/check-session', methods=['GET'])
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
        return jsonify(error="Signup details missing")

    # check if user actually exists
    account = (g.session
            .query(Account)
            .filter(Account.username == username)
            .scalar())
    if account:
        error_message = "Username taken"
        return jsonify(error=error_message)

    # create user and attempt to commit user
    new_account = Account(username=username)
    new_account.add_password(password)

    account_created = g.db_commit(g.session, [new_account])
    if not account_created:
        return jsonify(error="Failed to create account")

    # add account id to the session so session can be checked on re-direct
    session['account_id'] = new_account.id
    schema = schemas.AccountSchema(only=(['id', 'username', 'anonymous', 'dark_mode']))

    return jsonify(error=error_message, account=schema.dump(new_account))


account = Blueprint('account', __name__, url_prefix='/account')

@account.route('/update', methods=['POST'])
def account_update():
    r = request.get_json()
    anonymous = r.get('anonymous')
    dark_mode = r.get('dark_mode')

    account_id = session.get('account_id')
    error_message=None
    if not account_id:
        return jsonify(error="Not logged in")

    account = g.session.query(Account).filter(Account.id == account_id).scalar()
    if anonymous is not None:
        account.anonymous = anonymous
    if dark_mode is not None:
        account.dark_mode = dark_mode

    g.db_commit(g.session, [account])

    return jsonify(error=error_message)

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


@account.route('/post-review', methods=['POST'])
def post_review():
    r = request.get_json()
    post = r.get('post')
    position = r.get('position')
    position_id = r.get('position_id')
    org_id = r.get('org_id')

    r['account_id'] = session.get('account_id')

    error_message = None
    if not r['account_id']:
        return jsonify(post_created=False, error="Not logged in")
    if not position and not position_id:
        return jsonify(post_created=False, error="Position not given")
    if not post:
        return jsonify(post_created=False, error="Post not given")

    objs = []
    schema = schemas.ReviewSchema()
    if not position_id:
        new_position = Position(name=position, org_id=org_id)
        g.session.add(new_position)
        g.session.flush()

        r['position_id'] = new_position.id

    # we've used position by this point, remove so schema can load successfully
    r.pop('position', None)
    review = schema.load(r)
    objs.append(Review(**review))
    review_created = g.db_commit(g.session, objs)
    if not review_created:
        return jsonify(post_created=False, error="Failed to create post")

    return jsonify(post_created=review_created, error=error_message)


@account.route('/post-interview', methods=['POST'])
def post_interview():
    r = request.get_json()
    post = r.get('post')
    position = r.get('position')
    position_id = r.get('position_id')
    org_id = r.get('org_id')

    r['account_id'] = session.get('account_id')

    error_message = None
    if not r['account_id']:
        return jsonify(post_created=False, error="Not logged in")
    if not position and not position_id:
        return jsonify(post_created=False, error="Position not given")
    if not post:
        return jsonify(post_created=False, error="Post not given")

    objs = []
    schema = schemas.InterviewSchema()
    if not position_id:
        new_position = Position(name=position, org_id=org_id)
        g.session.add(new_position)
        g.session.flush()

        r['position_id'] = new_position.id

    # we've used position by this point, remove so schema can load successfully
    r.pop('position', None)
    interview = schema.load(r)
    objs.append(Interview(**interview))
    interview_created = g.db_commit(g.session, objs)
    if not interview_created:
        return jsonify(post_created=False, error="Failed to create post")

    return jsonify(post_created=interview_created, error=error_message)


@account.route('/delete-post', methods=['POST'])
def delete_post():
    r = request.get_json()
    post_id = r.get('post_id')
    post_model_type = r.get('post_type')

    account_id = session.get('account_id')

    error_message = None
    if not account_id:
        return jsonify(post_deleted=False, error="Not logged in")
    if not post_id or not post_model_type:
        return jsonify(post_deleted=False, error="Post not given")

    PModel = Review
    if post_model_type.lower() == PostTypeModel.INTERVIEW.value:
        PModel = Interview

    filters =[PModel.id == post_id, PModel.account_id == account_id]
    post = g.session.query(PModel).filter(*filters).scalar()
    g.session.delete(post)
    g.session.commit()

    return jsonify(post_deleted=True, error=error_message)


@account.route('/vote', methods=['PUT'])
def post_vote():
    """Handles creating new upvotes and downvotes for ReviewVote and
    InterviewVote objects. Existing votes are updated if a user changes it from
    a positive to a negative vote."""
    r = request.get_json()
    post_id = r.get('post_id', None)
    raw_vote = r.get('vote', None)
    already_upvoted = r.get('already_upvoted', False)
    already_downvoted = r.get('already_downvoted', False)
    vote_model_type = r.get('vote_model_type', PostTypeModel.REVIEW)

    account_id = session.get('account_id')

    error_message=None
    if not account_id:
        return jsonify(vote_created=False, error="Not authenticated")
    if not raw_vote:
        error_message = "Invalid vote"
        return jsonify(vote_created=False, error="Invalid vote")

    # figure out which model we are dealing with and update filters from there
    VoteModel = ReviewVote
    filters = [(VoteModel.review_id == post_id)]
    id_key = 'review_id'
    vote = Vote.DOWNVOTE.value if raw_vote < 0 else Vote.UPVOTE.value
    if vote_model_type.lower() == PostTypeModel.INTERVIEW.value:
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
