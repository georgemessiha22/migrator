import datetime
import click
import logging
from jinja2 import Environment, FileSystemLoader

from yoyo import read_migrations, get_backend
import os

LOGGING_LEVEL = os.environ.get("LEVEL", "DEBUG")

logger = logging.getLogger("migrator")

logging.basicConfig(
    format="[%(asctime)s] [%(levelname)s] [%(filename)s:L%(lineno)d] %(message)s",
    level=logging.getLevelNamesMapping()[LOGGING_LEVEL],
)

MIGRATION_FOLDER: str = os.environ.get("MIGRATION_FOLDER", "/migrations/")
MIGRATION_TABLE: str = os.environ.get("MIGRATION_TABLE", "migrator")

def database_url() -> str:
    """
    Generate the database url from environment variables, that can be replaced
    available options and default values:
    - DATABASE_USER=root
    - DATABASE_PASSWORD=root
    - DATABASE_NAME=main
    - DATABASE_DOMAIN
    - DATABASE_PORT=5432
    - DATABASE_TYPE=postgresql
    """
    user = os.environ.get("DATABASE_USER", "root")
    password = os.environ.get("DATABASE_PASSWORD", "root")
    database_name = os.environ.get("DATABASE_NAME")
    domain = os.environ.get("DATABASE_DOMAIN")
    port = os.environ.get("DATABASE_PORT")
    database_type = os.environ.get("DATABASE_TYPE", "postgresql")

    return f"{database_type}://{user}:{password}@{domain}:{port}/{database_name}"


@click.command(help="Create Migration file from template, providing the service name.")
@click.argument("service_name", required=True)
def create(service_name: str) -> None:
    """
    Create Migration file from template, providing the service name
    """
    env = Environment(loader=FileSystemLoader("migrator/templates"))
    template = env.get_template("create_service.py.jinja")
    filename = str(datetime.date.today()).replace("-", "") + f"_{service_name}.py"
    with open(MIGRATION_FOLDER + filename, "w") as f:
        f.write(template.render(service_name=service_name))
    logger.info(f"Migration file (migrations/{filename}) craeted")


@click.command(help="migrate all migration files.")
def migrate():
    """Apply all migration files presented in the migration folder."""
    logger.info("Migrating")
    backend = get_backend(database_url(), migration_table=MIGRATION_TABLE)
    migrations = read_migrations(MIGRATION_FOLDER)
    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))


@click.group()
def cli(service_name: str = None):
    """Microservices sidecar migrations"""
    pass


cli.add_command(migrate)
cli.add_command(create)

if __name__ == "__main__":
    cli()
