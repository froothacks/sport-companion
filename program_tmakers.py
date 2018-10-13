import datetime
from colorama import Fore
from dateutil import parser

from infrastructure.switchlang import switch
import infrastructure.state as state
import services.data_service as svc


def run():
    print(' ****************** Welcome Team maker **************** ')
    print()

    show_commands()

    while True:
        action = get_action()

        with switch(action) as s:
            s.case('c', create_account)
            s.case('a', create_account)
            s.case('l', log_into_account)
            s.case('y', list_events)
            s.case('r', register_event) 
            s.case('u', update_availability) #update if still available
            s.case('v', view_bookings) #see who joined
            s.case('m', lambda: 'change_mode')
            s.case(['x', 'bye', 'exit', 'exit()'], exit_app)
            s.case('?', show_commands)
            s.case('', lambda: None)
            s.default(unknown_command)

        if action:
            print()

        if s.result == 'change_mode':
            return


def show_commands():
    print('What action would you like to take:')
    print('[C]reate an [a]ccount')
    print('[L]ogin to your account')
    print('List [y]our event(s)')
    print('[R]egister an event')
    print('[U]pdate event availability')
    print('[V]iew your bookings')
    print('Change [M]ode (Team member or Team maker)')
    print('e[X]it app')
    print('[?] Help (this info)')
    print()


def create_account():
    print(' ****************** REGISTER **************** ')

    name = input('What is your name? ')
    email = input('What is your email? ').strip().lower()

    old_account = svc.find_account_by_email(email)
    if old_account:
        error_msg(f"ERROR: Account with email {email} already exists.")
        return

    state.active_account = svc.create_account(name, email)
    success_msg(f"Created new account with id {state.active_account.id}.")


def log_into_account():
    print(' ****************** LOGIN **************** ')

    email = input('What is your email? ').strip().lower()
    account = svc.find_account_by_email(email)

    if not account:
        error_msg(f'Could not find account with email {email}.')
        return

    state.active_account = account
    success_msg('Logged in successfully.')


def register_event():
    print(' ****************** REGISTER EVENT **************** ')

    if not state.active_account:
        error_msg('You must login first to register a cage.')
        return

    minutes = input('How long is the duration for the event? ')
    if not minutes:
        error_msg('Cancelled')
        return

    minutes = float(minutes)
    in_public_place = input("Is it in a public space [y, n]? ").lower().startswith('y')
    in_outdoors = input("Is it outdoors [y, n]? ").lower().startswith('y')
    allow_non_friends = input("Do you allow strangers (non-friends) to join your event [y, n]? ").lower().startswith('y')
    name = input("Give your sportevent a name: ")
    rating_price = float(input("How much rating are you expecting for the players to have?  "))

    cage = svc.register_event(
        state.active_account, name,
        allow_non_friends, in_outdoors, in_public_place, minutes, rating_price
    )

    state.reload_account()
    success_msg(f'Register new sportevent with id {cage.id}.')


def list_events(suppress_header=False):
    if not suppress_header:
        print(' ******************     Your events     **************** ')

    if not state.active_account:
        error_msg('You must login first to register an event.')
        return

    cages = svc.find_event_for_user(state.active_account)
    print(f"You have {len(events)} events.")
    for idx, c in enumerate(events):
        print(f' {idx+1}. {c.name} for {c.square_meters} minutes.')
        for b in c.bookings:
            print('      * Booking: {}, {} days, booked? {}'.format(
                b.check_in_date,
                (b.check_out_date - b.check_in_date).days,
                'YES' if b.booked_date is not None else 'no'
            ))


def update_availability():
    print(' ****************** Add available date **************** ')

    if not state.active_account:
        error_msg("You must log in first to register a cage")
        return

    list_cages(suppress_header=True)

    cage_number = input("Enter event number: ")
    if not cage_number.strip():
        error_msg('Cancelled')
        print()
        return

    event_number = int(event_number)

    events = svc.find_events_for_user(state.active_account)
    selected_event = events[event_number - 1]

    success_msg("Selected event {}".format(selected_event.name))

    start_date = parser.parse(
        input("Enter available date [yyyy-mm-dd]: ")
    )
    days = int(input("How many days is this block of time? "))

    svc.add_available_date(
        selected_cage,
        start_date,
        days
    )

    success_msg(f'Date added to cage {selected_cage.name}.')


def view_bookings():
    print(' ****************** Your bookings **************** ')

    if not state.active_account:
        error_msg("You must log in first to register an event")
        return

    event = svc.find_events_for_user(state.active_account)

    bookings = [
        (c, b)
        for c in events
        for b in c.bookings
        if b.booked_date is not None
    ]

    print("You have {} bookings.".format(len(bookings)))
    for c, b in bookings:
        print(' * Event: {}, booked date: {}, from {} for {} days.'.format(
            c.name,
            datetime.date(b.booked_date.year, b.booked_date.month, b.booked_date.day),
            datetime.date(b.check_in_date.year, b.check_in_date.month, b.check_in_date.day),
            b.duration_in_days
        ))


def exit_app():
    print()
    print('bye')
    raise KeyboardInterrupt()


def get_action():
    text = '> '
    if state.active_account:
        text = f'{state.active_account.name}> '

    action = input(Fore.YELLOW + text + Fore.WHITE)
    return action.strip().lower()


def unknown_command():
    print("Sorry we didn't understand that command.")


def success_msg(text):
    print(Fore.LIGHTGREEN_EX + text + Fore.WHITE)


def error_msg(text):
    print(Fore.LIGHTRED_EX + text + Fore.WHITE)
