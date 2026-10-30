from datetime import date

from app import create_app
from models import db, Exercise, Workout, WorkoutExercise


app = create_app()

with app.app_context():

    push_up = Exercise(
        name="Push Up",
        category="Strength",
        equipment_needed=False
    )

    squat = Exercise(
        name="Squat",
        category="Strength",
        equipment_needed=False
    )

    jump_rope = Exercise(
        name="Jump Rope",
        category="Cardio",
        equipment_needed=True
    )

    exercises = [push_up, squat, jump_rope]

    for exercise in exercises:
        existing = Exercise.query.filter_by(
            name=exercise.name
        ).first()

        if not existing:
            db.session.add(exercise)

    db.session.commit()

    push_up = Exercise.query.filter_by(
        name="Push Up"
    ).first()

    squat = Exercise.query.filter_by(
        name="Squat"
    ).first()

    jump_rope = Exercise.query.filter_by(
        name="Jump Rope"
    ).first()

    leg_day = Workout(
        date=date.today(),
        duration_minutes=45,
        notes="Leg strength training"
    )

    upper_body = Workout(
        date=date.today(),
        duration_minutes=40,
        notes="Upper body training"
    )

    workouts = [leg_day, upper_body]

    for workout in workouts:
        existing = Workout.query.filter_by(
            notes=workout.notes
        ).first()

        if not existing:
            db.session.add(workout)

    db.session.commit()

    leg_day = Workout.query.filter_by(
        notes="Leg strength training"
    ).first()

    upper_body = Workout.query.filter_by(
        notes="Upper body training"
    ).first()

    workout_exercises = [
        (leg_day, squat, 3, 12),
        (leg_day, jump_rope, 3, 30),
        (upper_body, push_up, 3, 15)
    ]

    for workout, exercise, sets, reps in workout_exercises:

        existing = WorkoutExercise.query.filter_by(
            workout_id=workout.id,
            exercise_id=exercise.id
        ).first()

        if not existing:
            db.session.add(
                WorkoutExercise(
                    workout=workout,
                    exercise=exercise,
                    sets=sets,
                    reps=reps
                )
            )

    db.session.commit()

    print("Database seeded successfully!")