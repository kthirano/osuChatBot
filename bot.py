import os
from dotenv import load_dotenv
from twitchio.ext import commands
import osu_helper as osu



load_dotenv()
bot = commands.Bot(
    irc_token = os.getenv('TMI_TOKEN'),
    client_id = os.getenv('CLIENT_ID'),
    nick = os.getenv('BOT_NICK'),
    prefix = os.getenv('BOT_PREFIX'),
    initial_channels = [os.getenv('CHANNEL')]
    )
requestQueue = []

@bot.command(name="test")
async def test(ctx, addon):
    await(ctx.send('you wrote after test: ' + addon))

@bot.command(name="request")
async def request(ctx, link):
    mapId = osu.verifyLink(link)
    if (mapId == -1):
        await(ctx.send(osu.getInvaliLinkErrorMessage()))
    else:
        mapinfo = osu.getBeatMap(mapId)
        if ('error' in mapinfo):
            await(ctx.send("Something went wrong on my side. @ me"))
        else:
            if (mapinfo['ranked'] != 1 or mapinfo['mode'] != 'osu'):
                await(ctx.send("Please make sure the map is ranked in osu standard!"))
            else:
                file = open("q.txt", "w")
                titleInfo = mapinfo['beatmapset']
                songtitle = titleInfo['title'] + " - " + titleInfo['artist']
                requestQueue.append((mapinfo['url'],songtitle))
                file.write(songtitle)
                file.close()
                await(ctx.send("Added " + songtitle + " to queue!"))


@bot.command(name="rank")
async def request(ctx):
    userinfo = getUserRank()
    if ('error' in mapinfo):
        await(ctx.send("Something went wrong on my side. @ me"))
    else:
        username = userinfo['username']
        countrycode = userinfo['country_code']
        statistics = userinfo['statistics']
        globalrank = statistics['global_rank']
        countryrank = statistics['country_rank']
        sendString = username + "'s rank: " + str(globalrank) + " (" + countrycode + ": " + str(countryrank) + " )"
        await(ctx.send(sendString))
            
    

@bot.command(name="next")
async def next(ctx):
    if (ctx.author.name == os.getenv('BOT_NICK')):
        songTuple = requestQueue.pop(0)
        with open('q.txt', 'w') as fout:
            fout.writelines(songTuple[1] + " ")
        if (len(requestQueue) == 0):
            with open('q.txt', 'w') as fout:
                fout.writelines("")
        await(ctx.send(songTuple[0]))
    else:
        await(ctx.send("You're not me!"))


@bot.command(name="queue")
async def showQueue(ctx):
    totalString = ""
    if (len(requestQueue) == 0):
        totalString = "No songs in queue!"
    else:
        for songTuple in requestQueue:
            totalString = totalString + songTuple[1] + ", "
    await(ctx.send(totalString))
        

if __name__ == "__main__":
    bot.run()
    
