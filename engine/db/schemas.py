from marshmallow import Schema, fields

from db.models import Currency, Industry, Vote, ReviewTag

class InterviewVoteSchema(Schema):
    id = fields.Int()
    account_id = fields.Int()
    interview_id = fields.Int()
    vote = fields.Enum(Vote)
    created_at = fields.Int()
    updated_at = fields.Int(load_only=True)

class ReviewVoteSchema(Schema):
    id = fields.Int()
    account_id = fields.Int()
    review_id = fields.Int()
    vote = fields.Enum(Vote)
    created_at = fields.Int()
    updated_at = fields.Int(load_only=True)

class ReviewSchema(Schema):
    id = fields.Int()
    position = fields.Str()
    compensation = fields.Int()
    currency = fields.Enum(Currency)
    location = fields.Str()
    duration_years = fields.Float()
    post = fields.Str()
    account = fields.Nested('AccountSchema', only=('username', 'id', 'anonymous'), dump_only=True)
    account_id = fields.Int(load_only=True)
    org_id = fields.Int()
    position = fields.Nested('PositionSchema', only=('name', 'id', 'org_id'), dump_only=True)
    position_id = fields.Int(load_only=True)
    created_at = fields.Int(dump_only=True)
    updated_at = fields.Int(dump_only=True)
    # review_votes = fields.Nested(ReviewVoteSchema, many=True, dump_only=True, exclude=('created_at', 'updated_at'))
    upvotes = fields.List(fields.Int(), dump_only=True)
    downvotes = fields.List(fields.Int(), dump_only=True)
    tag = fields.Enum(ReviewTag)
    reported = fields.Bool()

class InterviewSchema(Schema):
    id = fields.Int()
    position = fields.Str()
    location = fields.Str()
    compensation = fields.Int()
    stages = fields.Int()
    currency = fields.Enum(Currency)
    post = fields.Str()
    account = fields.Nested('AccountSchema', only=('username', 'id', 'anonymous'), dump_only=True)
    account_id = fields.Int(load_only=True)
    org_id = fields.Int()
    position = fields.Nested('PositionSchema', only=('name', 'id', 'org_id'), dump_only=True)
    position_id = fields.Int(load_only=True)
    created_at = fields.Int(dump_only=True)
    updated_at = fields.Int(dump_only=True)
    # interview_votes = fields.Nested(InterviewVoteSchema, many=True, dump_only=True, exclude=('created_at', 'updated_at'))
    upvotes = fields.List(fields.Int(), dump_only=True)
    downvotes = fields.List(fields.Int(), dump_only=True)
    tag = fields.Enum(ReviewTag)
    reported = fields.Bool()

class AccountSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(dump_only=True)
    created_at = fields.Int()
    updated_at = fields.Int(load_only=True)
    anonymous = fields.Bool()
    dark_mode = fields.Bool()
    reviews = fields.Nested(ReviewSchema, many=True, dump_only=True, exclude=['updated_at', 'account'])
    interviews = fields.Nested(InterviewSchema, many=True, dump_only=True, exclude=['updated_at', 'account'])
    interview_votes = fields.Nested(InterviewVoteSchema, many=True, dump_only=True, exclude=('created_at', 'updated_at'))
    review_votes = fields.Nested(ReviewVoteSchema, many=True, dump_only=True, exclude=('created_at', 'updated_at'))

class PositionSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    org_id = fields.Int()
    created_at = fields.Int()
    updated_at = fields.Int(load_only=True)
    total_reviews = fields.Int()
    total_interviews = fields.Int()

class OrganisationSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    url = fields.Str()
    size = fields.Int()
    headquarters = fields.Str()
    industry = fields.Enum(Industry)
    created_at = fields.Int()
    updated_at = fields.Int(load_only=True)
    reviews = fields.Nested(ReviewSchema, many=True, dump_only=True, exclude=['updated_at'])
    interviews = fields.Nested(InterviewSchema, many=True, dump_only=True, exclude=['updated_at'])
    positions = fields.Nested(PositionSchema, many=True, dump_only=True, exclude=['updated_at'])
    total_reviews = fields.Int()
    total_interviews = fields.Int()
    page_visits = fields.Str(load_only=True)
    verified = fields.Bool()
