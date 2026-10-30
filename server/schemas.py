from marshmallow import Schema, fields
from marshmallow.validate import Length, Range
class ExerciseSchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True, validate=Length(min=2))
    category = fields.Str()
    equipment_needed = fields.Bool()

    workouts = fields.Nested(
        "WorkoutSchema",
        many=True,
        only=("id", "date", "duration_minutes", "notes"),
        dump_only=True
    )
class WorkoutSchema(Schema):
    id = fields.Int()
    date = fields.Date()
    duration_minutes = fields.Int(
        required=True,
        validate=Range(min=1)
    )
    notes = fields.Str()

    exercises = fields.Nested(
        "ExerciseSchema",
        many=True,
        only=("id", "name", "category", "equipment_needed"),
        dump_only=True
    )
class WorkoutExerciseSchema(Schema):
    id = fields.Int()
    reps = fields.Int(validate=Range(min=0))
    sets = fields.Int(validate=Range(min=0))
    duration_seconds = fields.Int()


