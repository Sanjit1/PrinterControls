import discord
import os
from dotenv import load_dotenv
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
load_dotenv()

# * Google Drive stuff

gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)


def getPrintableFiles():
    # Get the files in the folder
    print_files = drive.ListFile(
        {'q': f"'{os.getenv('DRIVE_FOLDER')}' in parents and trashed=false"}).GetList()
    # Filter by type: # TODO: figure out what type, PDF is a placeholder
    # print_files = [f for f in print_files if (f['mimeType'] == 'application/pdf')]
    return print_files


print_files = getPrintableFiles()


# * Discord stuff

client = discord.Client(intents=discord.Intents.all())


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!fishnets'):
        await message.channel.send('netsfish!')
    # - `!pic` - Get a picture of the printer bed
    # - `!status` - Get the status of the printer
    # - `!pause` - Pause the current print
    # - `!resume` - Resume the current print
    # - `!cancel` - Cancel the current print
    # - `!print <filename>` - Print the file with the given filename
    # - `!list` - Get a list of all the files in the folder
    # - `!help` - Get a list of all the commands
    # - `!ping` - Get a response from the bot
    elif message.content.startswith('!pic'):
        # TODO: Get a picture of the printer bed
        await message.channel.send('pic')
    elif message.content.startswith('!status'):
        # TODO: Get the status of the printer
        await message.channel.send('status')
    elif message.content.startswith('!pause'):
        # TODO: Pause the current print
        await message.channel.send('pause')
    elif message.content.startswith('!resume'):
        # TODO: Resume the current print
        await message.channel.send('resume')
    elif message.content.startswith('!cancel'):
        # TODO: Cancel the current print
        await message.channel.send('cancel')
    elif message.content.startswith('!print'):
        # TODO: Print the file with the given filename
        printing = False  # TODO: figure out how to check if the printer is printing
        if printing:
            await message.channel.send('The printer is already printing something m8.')
        else:
            print_files = getPrintableFiles()
            if(len(message.content.split()) == 1):
                await message.channel.send('Try again with a file')
                return
            elif(len(message.content.split()) == 2):
                filename = message.content.split()[1]
                file = [f for f in print_files if filename in f['title']][0]
                if(file == None):
                    await message.channel.send('Could not find' + filename)
                    return
            elif(len(message.content.split()) == 3 and message.content.split()[1] == '-n'):
                filenumber = message.content.split()[2]
                # if it doesnt exist, return
                try:
                    int(filenumber)
                except ValueError:
                    await message.channel.send('Use a valid number!')
                    return
                if(int(filenumber) >= len(print_files)):
                    await message.channel.send('That number is too big!')
                    return
                file = print_files[int(filenumber)]
            else:
                await message.channel.send('Try again with a file')
                return
            # We now have the filename, now lets download it to the queue folder
            file.GetContentFile(os.getcwd() + '/queue/' + file['title'])
            # Now we can print it

        await message.channel.send('print')
    elif message.content.startswith('!list'):
        print_files = getPrintableFiles()
        # make a rich embed
        embed = discord.Embed(title="Stuff you can print",
                              description="Here ye go", color=0x00ff00)
        for i, f in enumerate(print_files):
            embed.add_field(
                name=(str(i) + ". " + f['title']), value=f['owners'][0]['displayName'], inline=False)
        await message.channel.send(embed=embed)
    elif message.content.startswith('!help'):
        # make a rich embed
        embed = discord.Embed(
            title="Help", description="List of commands", color=0x00ff00)
        # embed.add_field(name="!fishnets", value="netsfish!", inline=False) # skip this because it's an easter egg
        embed.add_field(
            name="!pic", value="Get a picture of the printer bed", inline=False)
        embed.add_field(
            name="!status", value="Get the status of the printer", inline=False)
        embed.add_field(
            name="!pause", value="Pause the current print", inline=False)
        embed.add_field(
            name="!resume", value="Resume the current print", inline=False)
        embed.add_field(
            name="!cancel", value="Cancel the current print", inline=False)
        embed.add_field(name="!print <filename>",
                        value="Print the file with the given filename", inline=False)
        embed.add_field(
            name="!list", value="Get a list of all the files in the folder", inline=False)
        embed.add_field(
            name="!help", value="Get a list of all the commands", inline=False)
        embed.add_field(
            name="!ping", value="Get a response from the bot", inline=False)
        await message.channel.send(embed=embed)
    elif message.content.startswith('!ping'):
        await message.channel.send('pong')
    elif message.content.startswith('!'):
        await message.channel.send('What? What do you want? Go away')


client.run(os.getenv('DISCORD_TOKEN'))
