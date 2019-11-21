What is cuabot?
===============

It's a Telegram bot to handle questions from assistants to speakers in conferences.

.. image:: media/cuabot.png

The dynamics to use the bot is:

- any person may speak to the bot, anytime, it only has commands to send questions

- when a user connects to it inform the commands; there's one command per conference room (e.g. ``/roomA``, ``/room8``, ``/plenary``); this is obviously configured per conference/bot instance.

- people in the conference, assisting to a talk, may send a question to the bot at any time (during the talk, or when the talk finishes); as the person uses a specific command, that question will be sent by the bot to a specific Telegram private group.

- there is one Telegram private group per conference room, supervised by the conference collaborators, specially by the person assigned to that conference room

- when each talk finishes, the room supervisor will have in the group those questions sent by the people during the talk (and more may come at that moment)

- the room supervisor can select from the received messages those that are *really questions* and read them to the speaker

This solve several common conference problems regarding Q&A:

- it's much easier to take courage to ask questions writing them than talking in a room full of people, specially if you are not a white middle-aged man, or the conference is not in your native language, for example

- the room supervisors select which questions to transmit, so they can avoid "non-questions" messages, or select the better questions if the time is short, etc

- the room supervisors would speak through the microphone, so the mic doesn't need to be carried away through all the room, and there's no risk of people not hearing the question or it not be recorded


How to use it?
==============

The idea is to start an instance of this bot during a conference. The steps to do this are:

- create a bot in Telegram

- configure credentials and other service particularities

- start cuabot and enjoy


Create the bot
--------------

FIXME: improve these steps docs

- Go to Telegram
- Start talking to BotFather
- /newbot
- insert username for the bot
- insert handler for the bot


Configure it all
----------------

Copy the `example.yaml` config file to something for you and change the parameters:

- `bot_token`: the token from bot father obtained above

- `welcome_message`: the message to show to the user when it starts interacting with the bot

- `question_handler`: the command string (`/something`) to send questions to the bot

- `question_message`: the message for the user to select the room

- `rooms`: the list of rooms handled by the bot, each one is a dict holding:

  - `name`: the human friendly name for the room, to show to the user

  - `chat_id`: the Telegram id for the room; one nice way to see it is to invite the bot to the specific room and call its `/get_chat_id` command


Start a cuabot instance
-----------------------

Run `python -m cuabot run <config_file>`
