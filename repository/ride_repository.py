from telebot import types

from components.paginate_buttons_component import generate
from db.models.ride_model import RideModel


class RideRepository:

    def __init__(self, bot):
        self.ride = RideModel()
        self.bot = bot

    def show_ride(self, message, id):
        ride = self.ride.find_matching_ride(id)
        if ride is None:
            return self.bot.send_message(message.chat.id, "Ride not found.")

        rides_text = (f"From - {ride['from_city']}\n"
                      f"To - {ride['to_city']}\n"
                      f"Date - {ride['ride_date']}\n"
                      f"Places - {ride['free_places']} / {ride['places']}\n"
                      f"Price - {ride['price']}֏\n"
                      f"🚙 - {ride['car_color']} {ride['car_mark']} "
                      f"{str(ride['car_number']).upper().replace(" ", "")}\n\n"
                      )

        markup = types.InlineKeyboardMarkup()
        if ride['user_id'] != message.chat.id:
            rides_text += f"Select places count for BOOKING"
            places_count = []
            for i in range(1, int(ride['free_places']) + 1):
                btn = types.InlineKeyboardButton(str(i),
                                                 callback_data="bookRide_" + str(ride['id']) + "_" + str(i))
                places_count.append(btn)

            markup.row(*places_count)
        back = types.InlineKeyboardButton("Back to list", callback_data="firstRides_first")
        markup.add(back)
        self.bot.send_message(message.chat.id, rides_text, reply_markup=markup)

    def find_ride(self, data):
        rides = self.ride.get_matching_rides(data['from_city'], data['to_city'], data['date'],
                                             data['free_places'])
        if len(rides) == 0:
            return self.bot.send_message(data['id'], "No rides found.")

        rides_text = ("OK, this is a list of rides. \n\n"
                      f"From - {data['from_city']}\n"
                      f"To - {data['to_city']}\n"
                      f"Date - {data['date']}\n"
                      f"Free places - {data['free_places']}")

        markup = types.InlineKeyboardMarkup()

        for ride in rides:
            ride_button_text = ''
            if ride['user_id'] == data['id']:
                ride_button_text += "🔴 "
            else:
                ride_button_text += "🟢 "

            ride_button_text += (f"Price - {str(ride['price'])}֏ "
                                 f" 🚙 {ride['car_color']} {ride['car_mark']} "
                                 f"{str(ride['car_number']).upper().replace(" ", "")} ")
            btn = types.InlineKeyboardButton(ride_button_text, callback_data="showRide_" + str(ride['id']))
            markup.add(btn)

        markup.row(*generate(len(rides)))

        self.bot.send_message(data['id'], rides_text, reply_markup=markup)