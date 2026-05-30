from injector import Module, provider, singleton
from db.db import Database
from models.bookings_model import BookingModel
from models.event_model import EventModel


# AppModule — это инструкция для DI-контейнера 
# о том, как создавать зависимости.
class AppModule(Module):
    @provider
    @singleton
    def provide_database(self) -> Database:
        return Database()

    # @provider
    # @singleton
    # def provide_booking_model(self, db: Database) -> BookingModel:
    #     return BookingModel(db)

    @provider
    @singleton
    def provide_event_model(self, db: Database) -> EventModel:
        return EventModel(db)