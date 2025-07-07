"""Generate 3 new bookings --> Log below scenarios to a log file
 All available booking ID's
Above added 3 new booking details
Modify total price for test1 to 1000 and test2 to 1500. Log this data to same log file.
Delete one of the booking --> Log return status to same file
Present the data in log file as html report.
Test1 with total price 500 who deposit is paid with random check in and checkout dates and having preference of lunch as additional need.
Test2 with total price of 1000 whose deposit is not paid yet with random check in and checkout dates having no preference for additional needs"""

import logging
import random
import string
from datetime import datetime, timedelta
import json
from utils.api_utils import create_booking, get_all_booking_ids, get_booking, update_booking, delete_booking, create_token
from utils.report_generator import generate_html_report

# Configure Logging
logging.basicConfig(filename='execution_log.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def generate_random_dates():
    checkin = datetime.today() + timedelta(days=random.randint(1, 10))
    checkout = checkin + timedelta(days=random.randint(1, 5))
    return checkin.strftime('%Y-%m-%d'), checkout.strftime('%Y-%m-%d')

def main():
    token = create_token("admin", "password123")
    
    test_data = [
        {
            "firstname": "Test",
            "lastname": "One",
            "totalprice": 500,
            "depositpaid": True,
            "additionalneeds": "Lunch"
        },
        {
            "firstname": "Test",
            "lastname": "Two",
            "totalprice": 1000,
            "depositpaid": False,
            "additionalneeds": ""
        },
        {
            "firstname": "Random",
            "lastname": "User",
            "totalprice": random.randint(200, 1000),
            "depositpaid": random.choice([True, False]),
            "additionalneeds": random.choice(["Breakfast", "", "Late checkout"])
        }
    ]

    booking_ids = []
    booking_details = []

    # Create Bookings
    for data in test_data:
        checkin, checkout = generate_random_dates()
        data["bookingdates"] = {"checkin": checkin, "checkout": checkout}
        response = create_booking(data)
        booking_id = response.get("bookingid")
        booking_ids.append(booking_id)
        booking_details.append(response)
        logging.info(f"Created Booking: {json.dumps(response)}")

    # Log all booking IDs here in the below
    all_ids = get_all_booking_ids()
    logging.info(f"All Booking IDs: {all_ids}")

    # Update Test1 and Test2 prices
    test1_id = booking_ids[0]
    test2_id = booking_ids[1]

    test1 = booking_details[0]['booking']
    test2 = booking_details[1]['booking']

    test1['totalprice'] = 1000
    test2['totalprice'] = 1500

    update_booking1 = update_booking(test1_id, test1, token)
    update_booking2 = update_booking(test2_id, test2, token)

    logging.info(f"Updated Booking Test1: {json.dumps(update_booking1)}")
    logging.info(f"Updated Booking Test2: {json.dumps(update_booking2)}")

    # Delete 3rd booking in the below code
    delete_id = booking_ids[2]
    delete_status = delete_booking(delete_id, token)
    logging.info(f"Deleted Booking ID {delete_id}: Status Code {delete_status}")

    # Generate HTML report from log
    generate_html_report('execution_log.log', 'report.html')

if __name__ == '__main__':
    main()
