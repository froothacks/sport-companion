import program_tmembers
import program_tmakers
import data.mongo_setup as mongo_setup


def main():
    mongo_setup.global_init()

    print_header()

    try:
        while True:
            if find_user_intent() == 'book': #if the user wants to find an event 
                program_tmembers.run()
            else:
                program_tmakers.run()  #if the user wants to create an event.
    except KeyboardInterrupt:
        return


def print_header():
    sport = \
        """
            ~ SPORT COMPANION  ~
      Find a sportive person near you """

    print(Fore.WHITE + '****************  SPORT COMPANION  ****************')
    print(Fore.GREEN + sport)
    print(Fore.WHITE + '*********************************************')
    print()
    print("Welcome to Sport Companion!")
    print("What would you like to do?")
    print()


def find_user_intent():
    print("[m] Create a sport event at a place")
    print("[mem] Look for a sport events near your place")
    print()
    choice = input("Are you a team[m]aker or team [mem]ber ? ")
    if choice == 'm':
        return 'offer'

    return 'book'


if __name__ == '__main__':
    main()
