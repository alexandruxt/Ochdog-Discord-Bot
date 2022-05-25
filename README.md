<h1>
  <br>
  Ochdog 🤖
  <br>
</h1>

<h3>Discord bot built with <a href=https://github.com/Rapptz/discord.py>discord.py</a></h3>

## 📖 About

Ochbot is a discord application that manages message history data, giving out various statistics such as the most active users, as well as fun commands like posting random anonymous messages, which can be turned into a fun guessing game for the server members.

Right now the bot is private for use as it is a work in progress, it's being tested in smaller servers as I try to implement new ideas almost every week.
The bot uses MySQL to store the message history data from every server and Python to manipulate the data.

## 🐕 Commands

*   `update`: the most complex command, it validates and uploads the messsage history into the MySQL data base, so that it can be manipulated more easily
*   `random`: gives one anonymous random message from the channel history, the users can guess who might've sent the said message (examples with screenshots below)
*   `reveal`: reveals the author, link, date and time of the previously posted anonymous message
*   `info`: gives personalised information about the user (number of messages sent, number of active days in the server, number of interactions with other members, etc.)
*   and others...


## 📈 How does the Data Storage happen?

I mentioned the command `update` being pretty complex for the reason that it creates new tables with every new channel that's being updated.
Everytime the command is executed the bot creates a table for the specific channel in which it stores all the messages (or maximum 100k), including the author of the message, the date, time, content and attachments.
The bot also creates a table for each user where it keeps data such as the number of messages the user sent.


## Examples of `info`, `random`, `reveal`

![image](https://user-images.githubusercontent.com/44554446/170286503-b7dd9b07-d074-4be0-85a3-64e40df201bb.png)
![image](https://user-images.githubusercontent.com/44554446/170286425-08e9f250-6434-4176-a476-9b4ebbaff62e.png)
