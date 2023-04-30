## Script to delete events from google calendar

from cal_setup import get_calendar_service
import googleapiclient


def main():
    # Delete the event
    service = get_calendar_service()
    try:
        service.events().delete(
            calendarId='primary',
            eventId='o8rdb29a8qnij9nrhu8u2c4e9g',
        ).execute()
    except googleapiclient.errors.HttpError:
        print("Failed to delete event")

    print("Event deleted")


if __name__ == '__main__':
    main()
