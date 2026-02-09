from peewee import PostgresqlDatabase

db = PostgresqlDatabase(
    "my_local_db",  # Database name
    user="postgres",  # Default user is usually 'postgres'
    password="password",  # Your password
    host="localhost",  # Local machine
    port=5432,  # Default Postgres port
)


def initialize_db():
    from models import Team, Player, Match, MatchReport, MatchPrediction

    with db:
        db.create_tables([Team, Player, Match, MatchReport, MatchPrediction], safe=True)
