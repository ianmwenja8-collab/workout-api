from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint, UniqueConstraint

db = SQLAlchemy()


class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String,
        nullable=False
    )

    category = db.Column(
        db.String,
        nullable=False
    )

    equipment_needed = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="exercise",
        cascade="all, delete-orphan"
    )

    workouts = db.relationship(
        "Workout",
        secondary="workout_exercises",
        viewonly=True
    )

    @validates("name")
    def validate_name(self, key, value):
        if len(value) < 2:
            raise ValueError(
                "Name must be at least 2 characters"
            )
        return value


class Workout(db.Model):
    __tablename__ = "workouts"

    __table_args__ = (
        CheckConstraint(
            "duration_minutes > 0",
            name="check_positive_duration"
        ),
    )

    id = db.Column(db.Integer, primary_key=True)

    date = db.Column(
        db.Date,
        nullable=False
    )

    duration_minutes = db.Column(
        db.Integer,
        nullable=False
    )

    notes = db.Column(db.Text)

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="workout",
        cascade="all, delete-orphan"
    )

    exercises = db.relationship(
        "Exercise",
        secondary="workout_exercises",
        viewonly=True
    )

    @validates("duration_minutes")
    def validate_duration(self, key, value):
        if value <= 0:
            raise ValueError(
                "Duration must be greater than 0"
            )
        return value


class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"

    __table_args__ = (
        UniqueConstraint(
            "workout_id",
            "exercise_id",
            name="unique_workout_exercise"
        ),
        CheckConstraint(
            "sets IS NULL OR sets >= 0",
            name="check_nonnegative_sets"
        ),
        CheckConstraint(
            "reps IS NULL OR reps >= 0",
            name="check_nonnegative_reps"
        ),
    )

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    workout_id = db.Column(
        db.Integer,
        db.ForeignKey("workouts.id"),
        nullable=False
    )

    exercise_id = db.Column(
        db.Integer,
        db.ForeignKey("exercises.id"),
        nullable=False
    )

    reps = db.Column(db.Integer)

    sets = db.Column(db.Integer)

    duration_seconds = db.Column(db.Integer)

    workout = db.relationship(
        "Workout",
        back_populates="workout_exercises"
    )

    exercise = db.relationship(
        "Exercise",
        back_populates="workout_exercises"
    )

    @validates("sets", "reps")
    def validate_numbers(self, key, value):
        if value is not None and value < 0:
            raise ValueError(
                f"{key} cannot be negative"
            )
        return value