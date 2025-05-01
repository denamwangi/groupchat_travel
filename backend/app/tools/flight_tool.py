import os
import csv
from amadeus import Client, ResponseError
from app.agents.mock_flights import mock_flights


# print('.'*50)
# print(mock_flights)

amadeus = Client(
    client_id=os.environ['AMADEUS_KEY'],
    client_secret=os.environ['AMADEUS_SECRET']
) 

def _load_iata_codes(filepath='airports.dat'):
    iata_lookup = {}
    with open(filepath, encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            city = row[2].lower()
            iata = row[4]
            if iata:  # avoid blank codes
                iata_lookup[city] = iata
    return iata_lookup

def _get_iata_code_for_city(city: str, codes):
    return codes.get(city)


def get_hotels(city: str):
    try:
        response = amadeus.reference_data.locations.hotels.by_city.get(cityCode='NBO')
    except ResponseError as e:
        print(f"error fetching hotel: {e}")
        return e
    
def _extract_flight_summary(flights: object):
    processed_flights = []
    for flight in flights:
        itinerary = flight['itineraries'][0]
        segment = itinerary['segments'][0]
        pricing = flight['travelerPricings'][0]

        flight_info = {
            "airline": segment["carrierCode"],
            "flight_number": segment["number"],
            "departure_airport": segment["departure"]["iataCode"],
            "departure_time": segment["departure"]["at"],
            "arrival_airport": segment["arrival"]["iataCode"],
            "arrival_time": segment["arrival"]["at"],
            "duration": itinerary["duration"],
            "cabin_class": pricing["fareDetailsBySegment"][0]["cabin"],
            "price_total": flight["price"]["total"],
            "currency": flight["price"]["currency"],
        }

        processed_flights.append(flight_info)

    print(f"Processing {len(flights)} flights data")
    return processed_flights

def get_flights(origin_city: str, destination_city: str, departure_date: str):
    """ Retrieves flight options for a particular origin location, destination and date

    Args:
        origin_city (str): The name of the city (e.g. "New York")
        destination_city (str): The name of the destination city (e.g. "Nairobi")
        departure_date (str): The date the user wants to depart
    Returns:
        dict: A dictionary containing the weather info
        Includes a 'status' key ('success' or 'error')
        If 'success', it will include a list of flight option objects
        If 'error', it will include an 'error_message'
    """
    
    return _extract_flight_summary(mock_flights)
    try:
        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode=origin_airport,
            destinationLocationCode=destination_airport,
            departureDate=departure_date,
            adults=1,
            currencyCode="USD",
            nonStop="true",
        )
        flight_summary = _extract_flight_summary(response.data)
        return flight_summary
    except ResponseError as e:
        print(f"error fetching flight options: {e}")
        return e


if __name__ == "__main__":
    print(_extract_flight_summary(mock_flights))