from app.database.connection import AsyncSessionLocal
import app.database.models_registry
import asyncio
import typer
from app.users.services import create_user_service
from app.users.schemas import UserCreateSchema

app = typer.Typer()


async def _create_superuser(name: str, surname: str, email: str, password: str) -> None:
    async with AsyncSessionLocal() as session:
        await create_user_service(
            UserCreateSchema(name=name, surname=surname, email=email, password=password),
            db=session,
            is_admin=True,
        )


@app.command()
def create_superuser(
    name: str = typer.Option(..., "--name"),
    surname: str = typer.Option(..., "--surname"),
    email: str = typer.Option(..., "--email"),
    password: str = typer.Option(..., "--pwd"),
) -> None:
    print("Creating superuser...")
    asyncio.run(_create_superuser(name, surname, email, password))
    print("Superuser created successfully!")


if __name__ == "__main__":
    app()