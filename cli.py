import typer
from datetime import datetime
from typing_extensions import Annotated

from services import event_service
from services import recurring_event_service
from models.event import Event

app = typer.Typer(no_args_is_help=True)


@app.command()
def add_event(summary: Annotated[str, typer.Option(prompt=True)],
              start_time: Annotated[
                  datetime, typer.Option(prompt="\nTime formats: YYYY-MM-DD, YYYY-MM-DD HH:MM:SS\n"
                                                "Start time")],
              end_time: Annotated[datetime, typer.Option(prompt=True)]) -> None:
    """Add a single event to the primary calendar."""

    attendees = event_service.add_attendee()

    event = Event(summary=summary, start_time=start_time, end_time=end_time, attendees=attendees)
    event_service.create_event(event)


@app.command()
def add_recurring_event(summary: Annotated[str, typer.Option(prompt=True)],
                        start_time: Annotated[
                            datetime, typer.Option(prompt="\nTime formats: YYYY-MM-DD, YYYY-MM-DD HH:MM:SS\n"
                                                          "Start time")],
                        end_time: Annotated[datetime, typer.Option(prompt=True)]) -> None:
    """Add a recurring event to the primary calendar."""

    attendees = event_service.add_attendee()
    recurrence_rule = recurring_event_service.add_recurrence_rule()

    event = Event(summary=summary, start_time=start_time, end_time=end_time,
                  attendees=attendees, recurrence=recurrence_rule)
    event_service.create_event(event)


@app.command()
def delete_event(event_id: Annotated[str, typer.Option(prompt=True)]):
    """Delete an event from the primary calendar by its ID."""
    event_service.delete_event(event_id)


@app.command()
def list_upcoming_events(max_results: Annotated[int, typer.Option(prompt=True)]):
    """List upcoming events in the primary calendar."""
    event_service.get_upcoming_events(max_results)


@app.command()
def get_event_by_id(event_id: Annotated[str, typer.Option(prompt=True)]):
    event_service.get_event_by_id(event_id)


if __name__ == "__main__":
    app()
