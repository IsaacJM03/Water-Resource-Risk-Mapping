# Backend

Scaffold for the Water Resource Risk Mapping service. Contains FastAPI app, database layer, services, and tests.

## Configuration
- Create a `.env` file in this folder using `.env.example` as a template.
- Key settings:
	- `DATABASE_URL`: SQLAlchemy URL (e.g., `mysql+pymysql://user:password@localhost:3306/water_risk`).
	- `SECRET_KEY`: secret used for tokens.
	- `ACCESS_TOKEN_EXPIRE_MINUTES`: token lifetime.
