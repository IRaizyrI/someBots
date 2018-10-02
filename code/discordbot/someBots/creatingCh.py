import discord
import asyncio

client = discord.Client()

VATNIK_SERVER_ID = '361563400427274240'
CONTROL_REACTION_ID = '422780652769771520'
ACCESS_ROLE_1_ID = '493741393567547393'
ACCESS_ROLE_2_ID = '496364196536123396'

CH_FILE = 'channellist.txt'

# reading contributors whitelist
with open('whitelist.txt') as f:
    ctb_whitelist = f.read().splitlines()

# reading author-channel dictionary
channels = dict()
with open(CH_FILE) as f:
    for line in f:
        (author, nazich) = line.split()
        channels[author] = nazich


# print channels dictionary
def print_dict(title):
    print(title)
    for k in channels:
        print(client.get_channel(channels[k]).name + '\t\tuid: ' + k + ' ch: ' + channels[k])
    print()


@client.event
async def on_ready():
    print('Connected!')
    print('Username: ' + client.user.name)
    print('ID: ' + client.user.id)
    print_dict('\nchannels:\n')


# remove channel from dict and file, if it has been deleted
@client.event
async def on_channel_delete(channel):
    if channel.id in channels.values():
        for k in channels:
            if channels[k] == channel.id:
                # rewrite file to delete specific line
                cf = open(CH_FILE, "r")
                lines = cf.readlines()  # read file to list
                cf.close()  # reopen file in write mode
                cf = open(CH_FILE, "w")
                for line in lines:
                    if line != (k + ' ' + channels[k] + "\n"):
                        cf.write(line)
                    else:
                        print('\ndeleted', k + ' ' + channels[k])
                cf.close()
                delete_item = k

        del channels[delete_item]  # delete dict instance

        # print new dict
        print_dict('updated channels:\n')


@client.event
async def on_reaction_add(reaction, user):
    if(user.id in ctb_whitelist) and (reaction.emoji.id == CONTROL_REACTION_ID):

        print_dict('\nchannels:\n')

        myserver = client.get_server(VATNIK_SERVER_ID)
        if reaction.message.author.id not in channels:

            # creating channel with name:author.name and premission read for two roles defined
            everyone = discord.PermissionOverwrite(read_messages=False)
            access = discord.PermissionOverwrite(read_messages=True)
            rolea = discord.utils.get(myserver.roles, id=ACCESS_ROLE_1_ID)
            roleb = discord.utils.get(myserver.roles, id=ACCESS_ROLE_2_ID)
            newchannel = await client.create_channel(myserver, reaction.message.author.name,
                                                     (myserver.default_role, everyone), (rolea, access), (roleb, access))
            await asyncio.sleep(1)  # pizdec a ne kostyl
            # add a dictionary item of new user+channel
            channels[reaction.message.author.id] = newchannel.id

            # print new dict
            print_dict('\nupdated channels:\n')

            # add a line with user+channel to txt file
            file = open(CH_FILE, 'a')
            file.write(reaction.message.author.id + ' ' + newchannel.id + '\n')
            file.close()

        print('post to ch', client.get_channel(str(channels[reaction.message.author.id])), 'id: ', channels[reaction.message.author.id])

        embed = discord.Embed(description=reaction.message.content, timestamp=reaction.message.timestamp)
        embed.set_author(name=reaction.message.author.name, icon_url=reaction.message.author.avatar_url)
        await client.send_message(client.get_channel(str(channels[reaction.message.author.id])), embed=embed)


client.run('NDg5ODExOTI1OTQ2MDczMTE5.DnwrNQ.HggsgJ-XpsL6yG_vNK-S0G1arMs')
