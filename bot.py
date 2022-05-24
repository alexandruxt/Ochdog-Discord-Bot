import random
import warnings
import mysql.connector
import discord
from datetime import datetime
from mysql.connector import Error

warnings.simplefilter(action='ignore', category=FutureWarning)

guild = discord.Guild


def is_command(msg):
    """

    :param msg: message to be checked
    :return: whether or not its a balid command
    """
    if len(msg.content) == 0:
        return False
    elif msg.content.startswith('och!'):
        return True
    elif "\'" in str(msg.content):
        return True
    elif "\"" in str(msg.content):
        return True
    elif "\\" in str(msg.content):
        return True
    elif len(msg.content) > 999:
        return True
    else:
        return False


def sameDay(d1, d2):
    """

    :param d1: first date
    :param d2: second date
    :return: whether or not the 2 dates are in the same day (in the same year, same month)
    """
    if d1.day == d2.day:
        if d1.month == d2.month:
            if d1.year == d2.year:
                return True
    return False


def getDate(d1):
    """

    :param d1: raw date
    :return: returns in the most fitting format (there is a bug that the first format won't work if the microseconds
    are equal to 0.
    """
    try:
        return datetime.strptime(str(d1), "%Y-%m-%d %H:%M:%S.%f")
    except ValueError:
        return datetime.strptime(str(d1), "%Y-%m-%d %H:%M:%S")


def niceDay(d1):
    """

    :param d1: raw date
    :return: date in a nice format i. e. "Monday, Dec 20, 2020"
    """
    return d1.strftime('%A, ') + d1.strftime("%b") + " " + str(d1.day) + ", " + str(d1.year)


class Ochdog(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        super().__init__(intents=intents)
        try:
            self.connection = mysql.connector.connect(host='localhost',
                                                      database='OchData',
                                                      user='root',
                                                      password='test',
                                                      auth_plugin='mysql_native_password')
            self.connection.autocommit = True
            if self.connection.is_connected():
                db_Info = self.connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                self.cursor = self.connection.cursor(buffered=True)
                self.cursor.execute("select database();")
                record = self.cursor.fetchone()
                print("You're connected to database: ", record)
        except Error as e:
            print("Error while connecting to MySQL", e)
        self.rows = []
        self.bots_are_banned = ['TriviaBot#7948', 'NotSoBot#9555', 'Miso Bot#9991', 'KDBot#9735', 'Dyno#3861',
                                'Chuu#1850', 'UB3R-B0T#3802', 'Tatsu#8792', 'Rythm#3722', 'Groovy#7254', 'Dyno#3861']

    async def on_ready(self):
        await self.get_channel(633400171425824846).send("im on")
        activity = discord.Game(name="och!help", type=3)
        await self.change_presence(status=discord.Status.online, activity=activity)
        print("I'm ready")

    def update_last_post(self, data):
        """
        updates the last random post so that it could reveal details about it later
        :param data: data of the last post
        :return:
        """
        check_command = 'SELECT * FROM LastPost WHERE channel_link = \'' + data[4] + '\''
        self.cursor.execute(check_command)
        data_aha = self.cursor.fetchone()
        if data_aha is None:
            executed_command = "INSERT INTO LastPost VALUES(\'" + data[0] + \
                               "\',\'" + data[1] + "\',\'" + data[2] + "\',\'" + data[3] + "\',\'" + \
                               data[4] + "\');"
        else:
            executed_command = 'UPDATE LastPost SET content = \'' + data[0] + '\',time = \'' + data[
                1] + '\',author=\'' + \
                               data[2] + '\',link=\'' + data[3] + '\' WHERE channel_link = \'' + data[4] + "\' "
        self.cursor.execute(executed_command)

    def get_last_post(self, channel_id):
        """
        :param channel_id: int
        :return: the last random post details
        """
        check_command = 'SELECT * FROM LastPost WHERE channel_link = \'' + str(channel_id) + '\''
        self.cursor.execute(check_command)
        data = list(self.cursor.fetchone())
        data.pop()
        return data

    async def on_message(self, message, limit=200000):
        """
        where we manipulate all messages that are our commands (begin with !och)
        :param message: the message that triggered the method
        :param limit: limit for how many messages to read
        :return:
        """
        if message.author == self.user:
            return
        elif message.content.startswith('och!'):
            cmd = message.content.split()[0].replace("och!", "")

            if len(message.content.split()) > 1:
                params = message.content.split()[1:]
            else:
                params = []

            # help people identify the commands
            if cmd == 'help':
                content = discord.Embed(title="Getting started",
                                        description="`och!help` triggers this same message\n"
                                                    "`och!ping` checks the connection (replies with pong)\n"
                                                    "`och!update` loads or updates messages\n"
                                                    "`och!random` gives one anonymous random message\n "
                                                    "`och!reveal` reveals the details of the last random message\n"
                                                    "`och!randomuser` gives a random user from the server\n"
                                                    "`och!info` see your stats in the current server\n"
                                                    "`och!interactions` see who you interacted with the most\n"
                                                    "`och!top_active_days` see top users for most active days\n\n"
                                                    "**Creator**: @Montigo#5612",
                                        color=0xFF0000)
                content.set_thumbnail(url='https://cdn.discordapp.com/avatars/963027212360101918'
                                          '/ca98ea59911b747c453cd7688a6fe7e4.png?size=1024')
                await message.channel.send(embed=content)

            # returns a random user from the server
            if cmd == 'randomuser':
                members = list(message.guild.members)
                n = random.randint(0, len(members) - 1)
                random_user = members[n]
                content = discord.Embed(title="Random user",
                                        description=str(random_user),
                                        color=0xFF0000)
                content.set_thumbnail(url=random_user.avatar_url)
                await message.channel.send(embed=content)

            # sets the main channel of a server from where we can read the messages and upload them into the DB
            if cmd == 'main_channel':
                executed_command = "INSERT INTO servers values(" + str(message.guild.id) + ", " + \
                                   str(message.channel.id) + ",\'2017-02-27 22:22:49.606000\')"
                self.cursor.execute(executed_command)
                await message.channel.send("Successfully set the main channel! Now you can update your data")

            # the most complex function, we validate all messages and put them into our data base,
            # we have to add a lot of information into every table in order to retrieve stats later
            if cmd == 'update':

                # First we check to see if the current server has a main channel
                check_command = "SELECT * FROM servers WHERE id = \'" + str(message.guild.id) + '\''
                self.cursor.execute(check_command)
                server_data = self.cursor.fetchone()
                if server_data is None:
                    await message.channel.send("You haven't updated this server yet. Before you do, you have to set the"
                                               " main channel, (i.e. the place from where we will take "
                                               "all of your data)\n"
                                               "Please execute the command \"och!main_channel"
                                               "\" in the channel you wish to use for collecting your data")
                    return

                # if it has a main channel, we get the last date and change the date of the last update
                data = list(server_data)
                check_channel = self.get_channel(int(data[1]))
                check_date = getDate(data[2])
                update_command = "UPDATE servers SET last_update = \'" + str(message.created_at) + "\'"
                self.cursor.execute(update_command)

                # then we create the table with the data if it didn't exist before
                create_command = "CREATE TABLE IF NOT EXISTS C" + str(
                    check_channel.id) + "(content varchar(1000), " \
                                        "time varchar(1000), " \
                                        "author varchar(1000), " \
                                        "link varchar(1000));"
                self.cursor.execute(create_command)
                await message.channel.send("Started updating messages now...")

                # then we insert the data in the tables as we go through every message
                prev_user = ""
                c = 0
                async for msg in check_channel.history(limit=100000):
                    if msg.author != self.user and str(msg.author) not in self.bots_are_banned:
                        if not is_command(msg):
                            if msg.created_at <= check_date:
                                print(msg.created_at, check_date)
                                break
                            if msg.attachments:
                                content = msg.attachments[0].url
                            else:
                                content = str(msg.content).lower()

                            # first we insert the message in the channel's data table
                            insert_command = "INSERT INTO C" + str(check_channel.id) + " VALUES(\'" + content + \
                                             "\',\'" + str(msg.created_at) + "\',\'" + str(
                                msg.author.id) + "\',\'" + str(
                                msg.jump_url) + "\');"
                            c = c + 1
                            if c > limit:
                                break
                            print(c)
                            self.cursor.execute(insert_command)

                            # then we update the data of the message author
                            # first we make sure the table for the users in this server exists:
                            create_command = "CREATE TABLE IF NOT EXISTS USERS" + str(
                                check_channel.id) + "(author varchar(1000), " \
                                                    "last_updated varchar(1000), " \
                                                    "letters int, " \
                                                    "active_days int, " \
                                                    "last_active varchar(1000), " \
                                                    "first_active varchar(1000), " \
                                                    "messages int);"
                            self.cursor.execute(create_command)

                            # then we add the user if they weren't in the table, and update their info
                            check_command = 'SELECT last_active, first_active FROM USERS' + str(
                                check_channel.id) + ' WHERE author = \'' + \
                                            str(msg.author.id) + '\''
                            self.cursor.execute(check_command)
                            user_data = self.cursor.fetchone()
                            if user_data is None:
                                executed_command = "INSERT INTO USERS" + str(check_channel.id) + " VALUES(\'" + \
                                                   str(msg.author.id) + "\',\'0\',\'1\',\'1\',\'" + \
                                                   str(msg.created_at) + "\',\'" + \
                                                   str(msg.created_at) + "\', 1);"
                                self.cursor.execute(executed_command)
                            else:
                                last_active = user_data[0]
                                first_active = user_data[1]
                                executed_command = 'UPDATE USERS' + str(check_channel.id) + \
                                                   ' SET letters = letters +' + str(len(content)) + ' + 1 ' + \
                                                   ' WHERE author = \'' + str(msg.author.id) + "\' "
                                self.cursor.execute(executed_command)
                                executed_command = 'UPDATE USERS' + str(check_channel.id) + \
                                                   ' SET messages = messages + 1 ' + \
                                                   ' WHERE author = \'' + str(msg.author.id) + "\' "
                                self.cursor.execute(executed_command)

                                last_active_date = getDate(last_active)
                                first_active_date = getDate(first_active)
                                now_date = getDate(message.created_at)
                                if not sameDay(now_date, first_active_date):
                                    executed_command = 'UPDATE USERS' + str(check_channel.id) + \
                                                       ' SET active_days = active_days + 1 ' + \
                                                       ' WHERE author = \'' + str(msg.author.id) + "\' "
                                    self.cursor.execute(executed_command)
                                    executed_command = 'UPDATE USERS' + str(check_channel.id) + \
                                                       ' SET first_active = \'' + str(msg.created_at) + '\'' + \
                                                       ' WHERE author = \'' + str(msg.author.id) + "\' "
                                    self.cursor.execute(executed_command)
                                if now_date > last_active_date:
                                    executed_command = 'UPDATE USERS' + str(check_channel.id) + \
                                                       ' SET last_active = \'' + str(msg.created_at) + '\'' + \
                                                       ' WHERE author = \'' + str(msg.author.id) + "\' "
                                    self.cursor.execute(executed_command)

                            # next, we update the interactions of the user
                            create_command = "CREATE TABLE IF NOT EXISTS I" + str(msg.guild.id) + \
                                             str(msg.author.id) + \
                                             "(user_id varchar(1000), " \
                                             "interactions int);"
                            self.cursor.execute(create_command)

                            # next we add the previous user to the table
                            if prev_user != "" and prev_user != str(msg.author.id):
                                check_command = "SELECT * FROM I" + str(msg.guild.id) + \
                                                str(msg.author.id) + " WHERE user_id = \'" + \
                                                prev_user + "\'"
                                self.cursor.execute(check_command)
                                user_data = self.cursor.fetchone()
                                if user_data is None:
                                    executed_command = "INSERT INTO I" + str(msg.guild.id) + \
                                                       str(msg.author.id) + " VALUES(\'" + \
                                                       prev_user + "\',1);"
                                else:
                                    executed_command = 'UPDATE I' + str(msg.guild.id) + \
                                                       str(msg.author.id) + \
                                                       ' SET interactions = interactions + 1 ' + \
                                                       ' WHERE user_id = \'' + prev_user + "\' "
                                self.cursor.execute(executed_command)

                            prev_user = str(msg.author.id)

                print("finished scanning")
                await message.channel.send("Finished updating messages!")

            if cmd == 'interactions':
                # we get the data from our data base and reveal it after sorting it
                executed_command = 'SELECT * FROM I' + str(message.guild.id) + \
                                   str(message.author.id) + ' order by interactions desc limit 10'
                print(executed_command)
                self.cursor.execute(executed_command)
                thumbnail = ""
                interactions = ""
                for i in range(10):
                    data_n = self.cursor.fetchone()
                    if data_n is None:
                        break
                    data = list(data_n)
                    user = await self.fetch_user(data[0])
                    if i == 0:
                        thumbnail = user.avatar_url
                    interactions = interactions + "**" + str(i + 1) + "** " + user.mention + \
                                   " - " + str(data[1]) + " interactions\n"

                content = discord.Embed(title="Top 10 Interactions For " + str(message.author),
                                        description=interactions,
                                        color=0xFF0000)
                content.set_thumbnail(url=thumbnail)
                await message.channel.send(embed=content)

            if cmd == 'info':
                # get user data from the specific table and put it up on an embed message
                executed_command = 'SELECT main_channel, id from servers where id=' + str(message.guild.id)
                self.cursor.execute(executed_command)
                main_channel = self.cursor.fetchone()
                channel = list(main_channel)
                executed_command = 'SELECT * from USERS' + str(channel[0]) + \
                                   ' where author=' + str(message.author.id)
                self.cursor.execute(executed_command)
                record = self.cursor.fetchone()
                data = list(record)
                user = await self.fetch_user(data[0])
                executed_command = 'SELECT * FROM I' + str(message.guild.id) + \
                                   str(message.author.id) + ' order by interactions desc limit 1'
                self.cursor.execute(executed_command)
                record = self.cursor.fetchone()
                interaction = list(record)
                interaction_user = await self.fetch_user(interaction[0])
                first = data[5]
                first_active_date = getDate(first)
                text = "User: " + user.mention + "\n" + \
                       "-----------------------------------------------------\n**" + \
                       str(data[6]) + "**" + " Messages sent \n**" + \
                       str(data[2]) + "**" + " Letters sent \n**" + \
                       str(int(data[2] / data[6])) + "**" + " Letters per Message sent \n**" + \
                       str(data[3]) + "**" + " Active days \n**" + \
                       str(int(data[6] / data[3])) + "**" + " Messages sent per active day \n" + \
                       "-----------------------------------------------------\n" + \
                       "Most interacted with user: " + interaction_user.mention + " | **" + str(
                    interaction[1]) + "** interactions"
                content = discord.Embed(title="User Info since " +
                                              niceDay(first_active_date),
                                        description=text,
                                        color=0xFF0000)
                content.set_thumbnail(url=user.avatar_url)
                await message.channel.send(embed=content)

            if cmd == 'top_active_days':
                # sorts the data from the table that holds the information of most active days for each user
                executed_command = 'SELECT main_channel, id from servers where id=' + str(message.guild.id)
                self.cursor.execute(executed_command)
                main_channel = self.cursor.fetchone()
                channel = list(main_channel)
                executed_command = 'SELECT author, active_days, first_active from USERS' + str(channel[0]) + \
                                   ' order by active_days desc limit 10'
                self.cursor.execute(executed_command)
                thumbnail = ""
                interactions = ""
                first = 0
                for i in range(10):
                    data_n = self.cursor.fetchone()
                    if data_n is None:
                        break
                    data = list(data_n)
                    user = await self.fetch_user(data[0])
                    if i == 0:
                        first = data[2]
                        thumbnail = user.avatar_url
                    interactions = interactions + "**" + str(i + 1) + "** " + user.mention + \
                                   " - " + str(data[1]) + " active days\n"
                first_active_date = getDate(first)
                content = discord.Embed(title="Top users with the most active days since " +
                                              str(first_active_date.day) + "-" + str(first_active_date.month) + "-" + \
                                              str(first_active_date.year),
                                        description=interactions,
                                        color=0xFF0000)
                content.set_thumbnail(url=thumbnail)
                await message.channel.send(embed=content)

            if cmd == 'random':
                # reveal a random message from the data base, completely anonymous so that it's up for the
                # users to guess who it could have been sent by
                executed_command = 'SELECT main_channel, id from servers where id=' + str(message.guild.id)
                self.cursor.execute(executed_command)
                main_channel = self.cursor.fetchone()
                channel = list(main_channel)
                used_channel = channel[0]
                create_command = "CREATE TABLE IF NOT EXISTS C" + str(
                    used_channel) + "(content varchar(1000), " \
                                    "time varchar(1000), " \
                                    "author varchar(1000), " \
                                    "link varchar(1000));"
                self.cursor.execute(create_command)
                random_command = 'SELECT * FROM C' + str(used_channel) + ' ORDER BY RAND ( ) LIMIT 1 '
                self.cursor.execute(random_command)
                data_n = self.cursor.fetchone()
                if data_n is None:
                    await message.channel.send("You haven't updated this channel yet\n"
                                               "to do so, type 'och!update'")
                else:
                    data = list(data_n)
                    data.append(str(message.channel.id))
                    self.update_last_post(data)
                    await message.channel.send("> " + data[0])

            if cmd == 'ping':
                # ping pong connection tester!
                await message.channel.send("pong woof!")

            if cmd == 'reveal':
                # reveals the last posted random message
                data = self.get_last_post(message.channel.id)
                if data[1] == 'test':
                    await message.channel.send("do the random command first bitch")
                else:
                    user = await self.fetch_user(data[2])
                    print(user)
                    show_date = getDate(data[1])
                    content = discord.Embed(title="Revealing Message",
                                            description="[[Go To Message]](" + data[3] + "): " +
                                                        data[
                                                            0] + "\n"
                                                                 "**Sent by**: " + user.mention + "\n"
                                                                                                  "**At**: " +
                                                        niceDay(show_date),
                                            color=0xFF0000)
                    content.set_thumbnail(url=user.avatar_url)
                    await message.channel.send(embed=content)


ochdog = Ochdog()
ochdog.run("OTYzMDI3MjEyMzYwMTAxOTE4.YlQG-w.PWNQZF-2ydS1p-FtD09jg-xeFpA")
