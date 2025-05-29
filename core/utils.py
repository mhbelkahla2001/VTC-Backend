from django.core.mail import send_mail
import os
from twilio.rest import Client
import requests
from dotenv import load_dotenv
load_dotenv()

def send_reservation_email(to_email, username, pickup, destination, date, time):
    subject = "Confirmation de votre réservation VTC"
    message = (
        f"Bonjour {username},\n\n"
        f"Votre réservation a bien été enregistrée :\n"
        f"🛫 Départ : {pickup}\n"
        f"🛬 Destination : {destination}\n"
        f"📅 Date : {date} à {time}\n\n"
        f"Merci pour votre confiance.\n"
        f"— Équipe VTC App"
    )
    send_mail(subject, message, None, [to_email])

def send_sms(to_number, message_body):
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    twilio_phone_number = os.environ.get('TWILIO_PHONE_NUMBER')

    if not all([account_sid, auth_token, twilio_phone_number]):
        print("Twilio credentials not found in environment variables.")
        return None

    client = Client(account_sid, auth_token)
    try:
        message = client.messages.create(
            body=message_body,
            from_=twilio_phone_number,
            to=to_number
        )
        return message.sid
    except Exception as e:
        print(f"Error sending SMS: {e}")
        return None

def get_coordinates(address):
    mapbox_token = os.environ.get('MAPBOX_ACCESS_TOKEN')

    if not mapbox_token:
        print("Mapbox access token not found in environment variables.")
        return None, None

    url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{address}.json?access_token={mapbox_token}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data['features']:
            coords = data['features'][0]['center']
            return coords[1], coords[0]  # lat, lng
        else:
            return None, None

    except requests.exceptions.RequestException as e:
        print(f"Error during Mapbox API request: {e}")
        return None, None
    except (KeyError, IndexError, ValueError) as e:
        print(f"Error processing Mapbox API response: {e}")
        return None, None