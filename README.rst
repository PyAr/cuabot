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

FIXME: write this


Configure it all
----------------

FIXME: write this


Start a cuabot instance
-----------------------

FIXME: write this
