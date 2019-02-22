import sys

if __name__ == "__main__":
    try:
        bot = sys.argv[1]
        if bot == '1':
            from bot import launch as bot_launch
            bot_launch
        elif bot == '2':
            from bot import launch2 as bot_launch
            bot_launch
        elif bot == '3':
            from bot import launch3 as bot_launch
            bot_launch
        elif bot == '4':
            from bot import launch4 as bot_launch
            bot_launch
        elif bot == '5':
            from bot import launch5 as bot_launch
            bot_launch
        else:
            print('Specify a bot to run (1/2)')
    except IndexError:
        print('Specify a bot to run (1/2)')
