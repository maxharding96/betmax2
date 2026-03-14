from services.stats import get_dispersion_by_league
from database import get_session
from schemas import League, Field
from pprint import pprint


def main():
    with get_session() as session:
        mean, variance, dispersion = get_dispersion_by_league(
            session, League.PREMIER_LEAGUE, Field.SH
        )
        pprint({"mean": mean, "variance": variance, "dispersion": dispersion})


if __name__ == "__main__":
    main()
