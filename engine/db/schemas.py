from marshmallow import Schema, fields

from db.models import Currency, Industry, Vote

class InterviewVoteSchema(Schema):
    id = fields.Int()
    account_id = fields.Int()
    interview_id = fields.Int()
    vote = fields.Enum(Vote)
    created_at = fields.Int()
    updated_at = fields.Int(exclude=True)

class ReviewVoteSchema(Schema):
    id = fields.Int()
    account_id = fields.Int()
    review_id = fields.Int()
    vote = fields.Enum(Vote)
    created_at = fields.Int()
    updated_at = fields.Int(exclude=True)

class ReviewSchema(Schema):
    id = fields.Int()
    position = fields.Str()
    salary = fields.Int()
    currency = fields.Enum(Currency)
    location = fields.Str()
    duration_years = fields.Float()
    review = fields.Str()
    account_id = fields.Int()
    org_id = fields.Int()
    created_at = fields.Int()
    updated_at = fields.Int(exclude=True)
    review_votes = fields.Nested(ReviewVoteSchema, many=True, dump_only=True, exclude=('created_at', 'updated_at'))
    upvotes = fields.List(fields.Int())
    downvotes = fields.List(fields.Int())

class InterviewSchema(Schema):
    id = fields.Int()
    position = fields.Str()
    location = fields.Str()
    interview = fields.Str()
    account_id = fields.Int()
    org_id = fields.Int()
    created_at = fields.Int()
    updated_at = fields.Int(exclude=True)
    interview_votes = fields.Nested(InterviewVoteSchema, many=True, dump_only=True, exclude=('created_at', 'updated_at'))
    upvotes = fields.List(fields.Int())
    downvotes = fields.List(fields.Int())

class AccountSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    created_at = fields.Int()
    updated_at = fields.Int(exclude=True)
    reviews = fields.Nested(ReviewSchema, many=True, dump_only=True, exclude=['updated_at'])
    interviews = fields.Nested(InterviewSchema, many=True, dump_only=True, exclude=['updated_at'])
    interview_votes = fields.Nested(InterviewVoteSchema, many=True, dump_only=True, exclude=('created_at', 'updated_at'))
    review_votes = fields.Nested(ReviewVoteSchema, many=True, dump_only=True, exclude=('created_at', 'updated_at'))

class OrganisationSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    url = fields.Str()
    size = fields.Int()
    industry = fields.Enum(Industry)
    created_at = fields.Int()
    updated_at = fields.Int(exclude=True)
    reviews = fields.Nested(ReviewSchema, many=True, dump_only=True, exclude=['updated_at'])
    interviews = fields.Nested(InterviewSchema, many=True, dump_only=True, exclude=['updated_at'])
