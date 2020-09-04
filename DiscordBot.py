
import discord.config as Config
import discord.NoobBot_Utilities as Utils
import discord
import requests
import pyodbc

client = discord.Client()

@client.event
async def on_message(message):
    #base case
    if message.author==client.user:
        return


    if (message.content=="Hey" or message.content=="hey"):
        await message.channel.send("hi")

    elif message.content.startswith('!help'):
        #get all valid commands for this bot
        embed = Utils.GetAllValidCommands()
        await message.channel.send(embed=embed)

    elif message.content.startswith('!recent '):
        #get substring to search in database
        Substr = Utils.GetQuerySubString(message.content,1)
        # create Sql server connection hosted on google cloud
        conn=Config.CreateMSSQLConnection( Config.GetConnectionString() )
        #get all matched results in a list using substring search algorithms
        Hist=Utils.GetSearchHistory(conn)
        #print the searched data into a format
        embed=Utils.PrintResults(Hist,Substr)
        await message.channel.send(embed=embed)


    elif message.content.startswith('!google '):
        #get substring to search on google
        Substr = Utils.GetQuerySubString(message.content,2)

        #storing query: create Sql server connection hosted on google cloud
        conn = Config.CreateMSSQLConnection(Config.GetConnectionString())
        #save Query in database using stored procedure
        Utils.SaveQueryInDataBase(conn,Substr)

        #search Engine using custom google  search API
        #step 1 : set starting page of search
        start = 1

        #Step 2: call Google coustum search API
        url = f"https://www.googleapis.com/customsearch/v1?key={Config.API_KEY}&cx={Config.SEARCH_ENGINE_ID}&q={Substr}&start={start}"
        data = requests.get(url).json()
        search_items = data.get("items")
        
        #Step 3: Extract top 5 links from the output data of API
        Links=Utils.GetTop5Links(search_items)
        #print data found

        embed=Utils.PrintResult(Links)
        await message.channel.send(embed=embed)

    else:
        embed = discord.Embed(colour=discord.Colour.green())
        embed.set_author(name='Invalid Query! here is the list of commands available')
        embed.add_field(name='!google [Search Query]', value='Returns top 5 Google Search Results of given Query',
                        inline=False)
        embed.add_field(name='!recent [Query]', value='Returns resent searched query using !google.', inline=False)
        await message.channel.send(embed=embed)



client.run(Config.TOKEN)

