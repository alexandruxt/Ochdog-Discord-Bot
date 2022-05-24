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

![image](https://user-images.githubusercontent.com/44554446/170082660-adce5180-fb6c-4e4e-8fcf-db33188d7b94.png)
![image](https://user-images.githubusercontent.com/44554446/170083198-b84203a1-968f-4c98-a8d9-61c1000d9346.png)
