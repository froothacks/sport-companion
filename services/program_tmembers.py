import datetime
from dateutil import parser


def run():
    print(' ****************** Welcome team member **************** ')
    print()

    show_commands()

    while True:
        action = tmaker.get_action()

        with switch(action) as s:
            s.case('c', tmaker.create_account) 
            s.case('l', tmaker.log_into_account) 

            s.case('a', add_a_sportevent) 
            s.case('y', view_your_sportevents) 
            s.case('b', join_a_sportevent) 
            s.case('v', view_your_joinings) 
            s.case('m', lambda: 'change_mode') 

            s.case('?', show_commands) #help
            s.case('', lambda: None) 
            s.case(['x', 'bye', 'exit', 'exit()'], hosts.exit_app)

            s.default(hosts.unknown_command)

        state.reload_account()

        if action:
            print()

        if s.result == 'change_mode':
            return


def show_commands():
    print('What action would you like to take:')
    print('[C]reate an account')
    print('[L]ogin to your account')
    print('[J]oin a sportevent')
    print('[A]dd a sportevent')
    print('[V]iew your sportevents')
    print ('View your sports [b]ookings as a team-member') 
    print('[M]ain menu')
    print('e[X]it app')
    print('[?] Help (this info)')
    print()


def add_a_sportevent():
    print(' **++++++++** Add a Sport event **++++++++** ')
    if not state.active_account:
        error_msg("You must log in first to add a sport/event")
        return

    name = input("What sport/game are looking to play")
    if not name:
        error_msg('cancelled')
        return

    length = float(input('How long would you like to play (in minutes)? '))
    location = ("Location (Address) ?")
    is_outdoors = input("Are you playing outdoors [y]es, [n]o? ").lower().startswith('y')

    sport = svc.add_sport(state.active_account, name, length, location, environment )
    state.reload_account()
    success_msg('Created {} with id {}'.format(sport.name, sport.id))


def view_your_sportevents():
    print(' ****************** Your sportevents **************** ')
    if not state.active_account:
        error_msg("You must log in first to view your sportevents")
        return

    sports = svc.get_sports_for_user(state.active_account.id)
    print("You have {} sportevents.".format(len(sports)))
    for s in sports:
        print(" * {} is a {} that is {}minute(s) long and it will on {}outdoors.".format(
            s.name
            s.location
            s.length
            '' if s.is_outdoors else 'not'
        ))


def join_a_sport_event():
    print(' ****************** Join a sport event **************** ')
    if not state.active_account:
        error_msg("You must log in first to join an event")
        return

    sports = svc.get_sports_for_user(state.active_account.id)
    if not sports:
        error_msg('You must first [a]dd a sport before you can book a event.')
        return

    print("Let's start by finding available sportevents.")
    start_text = input("Check on date [yyyy-mm-dd]: ")
    if not start_text:
        error_msg('cancelled')
        return

    checkin = parser.parse(
        start_text
    )
    #checkout = parser.parse(
        #input("Check-out date [yyyy-mm-dd]: ")
    )
    #if checkin >= checkout:
        #error_msg('Check in must be before check out')
        #return

    print()
    for idx, s in enumerate(sports):
        print('{}. {} (length: {}, outdoors: {})'.format(
            idx + 1,
            s.name,
            s.length,
            'yes' if s.is_outdoors else 'no'
        ))

    sport = sports[int(input('Which sportevent do you want to join (number)')) - 1]

    sportevents = svc.get_available_sportevents(checkon, checkon, sport)

    print("There are {} sportevents available in that day.".format(len(sportevents)))
    for idx, c in enumerate(sportevents):
        print(" {}. {} with {}m carpeted: {}, has toys: {}.".format(
            idx + 1,
            c.name,
            c.square_meters,
            'yes' if c.is_carpeted else 'no',
            'yes' if c.has_toys else 'no'))

    if not sportevents:
        error_msg("Sorry, no sportevents are available for that date.")
        return

    sportevent = sportevents[int(input('Which sportevent do you want to join (number)')) - 1]
    svc.book_sportevent(state.active_account, sport, sportevent, from, to)

    success_msg('Successfully booked {} for {} at ${}/night.'.format(sportevent.name, sport.name, sportevent.ava))


def view_your_joinings():
    print(' ****************** Your joinings **************** ')
    if not state.active_account:
        error_msg("You must log in first to register in a sport")
        return

    sports = {s.id: s for s in svc.get_sports_for_user(state.active_account.id)}
    bookings = svc.get_bookings_for_user(state.active_account.email)

    print("You have {} bookings.".format(len(bookings)))
    for b in bookings:
        print(' * Sport/Event: {} is booked at {} from {} for {} days.'.format(
            sports.get(b.guest_sport_id).name,
            b.sportevent.name,
            datetime.date(b.from_date.year, b.to_date.month, b.from_date.day),
            (b.to_date - b.from_date).days
        ))