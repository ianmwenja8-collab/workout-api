from flask import Flask, jsonify, request
from flask_migrate import Migrate
from marshmallow import ValidationError
from pathlib import Path

from server.models import db, Exercise, Workout, WorkoutExercise
from server.schemas import (
    ExerciseSchema,
    WorkoutSchema,
    WorkoutExerciseSchema
)


def create_app(test_config=None):
    app = Flask(__name__)

    BASE_DIR = Path(__file__).resolve().parent

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"sqlite:///{BASE_DIR / 'app.db'}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    Migrate(app, db)

    exercise_schema = ExerciseSchema()
    exercises_schema = ExerciseSchema(many=True)

    workout_schema = WorkoutSchema()
    workouts_schema = WorkoutSchema(many=True)

    workout_exercise_schema = WorkoutExerciseSchema()

    @app.route("/")
    def home():
        return jsonify({
            "message": "Workout API is running!"
        }), 200
    @app.route("/workouts", methods=["GET"])
    def get_workouts():
        workouts = Workout.query.all()
        return jsonify(workouts_schema.dump(workouts)), 200
    @app.route("/workouts/<int:id>", methods=["GET"])
    def get_workout(id):
        workout = db.session.get(Workout, id)

        if not workout:
            return jsonify({"error": "Workout not found"}), 404

        return jsonify(workout_schema.dump(workout)), 200
    @app.route("/workouts", methods=["POST"])
    def create_workout():
        try:
            validated_data = workout_schema.load(request.get_json())

            workout = Workout(**validated_data)

            db.session.add(workout)
            db.session.commit()

            return jsonify(workout_schema.dump(workout)), 201

        except ValidationError as error:
            return jsonify(error.messages), 400

    @app.route("/workouts/<int:id>", methods=["DELETE"])
    def delete_workout(id):
        workout = db.session.get(Workout, id)

        if not workout:
            return jsonify({"error": "Workout not found"}), 404

        db.session.delete(workout)
        db.session.commit()

        return jsonify({
            "message": "Workout deleted successfully"
        }), 200

    @app.route("/exercises", methods=["GET"])
    def get_exercises():
        exercises = Exercise.query.all()
        return jsonify(exercises_schema.dump(exercises)), 200

    @app.route("/exercises/<int:id>", methods=["GET"])
    def get_exercise(id):
        exercise = db.session.get(Exercise, id)

        if not exercise:
            return jsonify({"error": "Exercise not found"}), 404

        return jsonify(exercise_schema.dump(exercise)), 200

    @app.route("/exercises", methods=["POST"])
    def create_exercise():
        try:
            validated_data = exercise_schema.load(request.get_json())

            exercise = Exercise(**validated_data)

            db.session.add(exercise)
            db.session.commit()

            return jsonify(exercise_schema.dump(exercise)), 201

        except ValidationError as error:
            return jsonify(error.messages), 400
    @app.route("/exercises/<int:id>", methods=["DELETE"])
    def delete_exercise(id):
        exercise = db.session.get(Exercise, id)

        if not exercise:
            return jsonify({"error": "Exercise not found"}), 404

        db.session.delete(exercise)
        db.session.commit()

        return jsonify({
            "message": "Exercise deleted successfully"
        }), 200
    @app.route(
        "/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises",
        methods=["POST"]
    )
    def add_exercise_to_workout(workout_id, exercise_id):
        workout = db.session.get(Workout, workout_id)
        exercise = db.session.get(Exercise, exercise_id)

        if not workout:
            return jsonify({"error": "Workout not found"}), 404

        if not exercise:
            return jsonify({"error": "Exercise not found"}), 404

        try:
            validated_data = workout_exercise_schema.load(
                request.get_json()
            )

            workout_exercise = WorkoutExercise(
                workout_id=workout_id,
                exercise_id=exercise_id,
                **validated_data
            )

            db.session.add(workout_exercise)
            db.session.commit()

            return jsonify(
                workout_exercise_schema.dump(workout_exercise)
            ), 201

        except ValidationError as error:
            return jsonify(error.messages), 400

    return app
app = create_app()
