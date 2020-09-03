#nodeBot
#TOKEN = "NzUwNzcxMjYxODc3MjU2Mjg1.X0_YOQ._06jiG8andXDCn045HwVCMUSQhU"

#noobbot
TOKEN = "NzUxMTQzMzA4NjM3NzY1Njgy.X1EyuA.QhNotqE4RsKV05daOlPLHo7v5Gw"
#


import discord
from discord.ext import commands
import requests
client = discord.Client()

@client.event
async def on_message(message):

    if message.author==client.user:
        print('done')
        return
    if (message.content=="Hey" or message.content=="hey"):

        await message.channel.send("hi")

    elif message.content.startswith('!help'):
        embed = discord.Embed( colour=discord.Colour.green())
        embed.set_author(name='Help : list of commands available')
        embed.add_field(name='!google [Search Query]', value='Returns top 5 Google Search Results of given Query', inline=False)
        embed.add_field(name='!recent [Query]', value='Returns recent searched query using !google.', inline=False)
        await message.channel.send(embed=embed)
    elif message.content.startswith('!recent '):
        with open("C:\\Users\\ravi.rathore\\Desktop\\discord\\hist.txt") as f:
            content = f.readlines()
        content = [x.strip() for x in content]
        setContent=set(content)
        setContent1=list(setContent)
        print(setContent1)
        SQ = message.content.replace('!recent ', '')
        embed = discord.Embed(colour=discord.Colour.green())
        embed.set_author(name='Recent Search Results')
        c=0
        for i in range(len(setContent1)):
            if(KMPSearch(SQ,setContent1[i])):
                embed.add_field(name='' + str(c + 1) + ' Result', value=setContent1[i], inline=False)
                c=c+1
        if(c==0):
            embed.add_field(name='No recent history found ', value=SQ, inline=False)

        await message.channel.send(embed=embed)


    elif message.content.startswith('!google '):
        SQ=message.content.replace('!google ','')
        dd={}
        dd[message.author]=SQ
        file1 = open("C:\\Users\\ravi.rathore\\Desktop\\discord\\hist.txt", "a")
        kk=[str(SQ) + "\n"]
        file1.writelines(kk)
        file1.close()

        #with open("C:\\Users\\ravi.rathore\\Desktop\\discord\\history.json", "w") as fp:
         #   json.dump({str(message.author):SQ}, fp)

        API_KEY = "AIzaSyBL8STSFQVCpHUxSOkC8vhRsYGR0FXcV9Y"  # The API_KEY you acquired
        SEARCH_ENGINE_ID = "82caebc11378cedc4"  # The search-engine-ID you created

        query = SQ
        page = 1
        start = (page - 1) * 5 + 1

        url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}"
        data = requests.get(url).json()
        search_items = data.get("items")
        ll = []
        # iterate over 10 results found
        for i, search_item in enumerate(search_items, start=1):
            if (i > 5): break
            # get the page title
            title = search_item.get("title")
            # page snippet
            snippet = search_item.get("snippet")
            # alternatively, you can get the HTML snippet (bolded keywords)
            html_snippet = search_item.get("htmlSnippet")
            # extract the page url
            link = search_item.get("link")
            # print the results
            ll.append(link)

        embed = discord.Embed(colour=discord.Colour.green())
        embed.set_author(name='Top 5 google Search Results')
        for i in range(len(ll)):
            embed.add_field(name='' + str(i+1) + 'Result', value=ll[i], inline=False)


        await message.channel.send(embed=embed)
    else:
        embed = discord.Embed(colour=discord.Colour.green())
        embed.set_author(name='Invalid Query! here is the list of commands available')
        embed.add_field(name='!google [Search Query]', value='Returns top 5 Google Search Results of given Query',
                        inline=False)
        embed.add_field(name='!recent [Query]', value='Returns resent searched query using !google.', inline=False)
        await message.channel.send(embed=embed)


def KMPSearch(pat, txt):
    M = len(pat)
    N = len(txt)

    # create lps[] that will hold the longest prefix suffix
    # values for pattern
    lps = [0] * M
    j = 0  # index for pat[]

    # Preprocess the pattern (calculate lps[] array)
    computeLPSArray(pat, M, lps)

    i = 0  # index for txt[]
    while i < N:
        if pat[j] == txt[i]:
            i += 1
            j += 1

        if j == M:
            return 1
            j = lps[j - 1]

            # mismatch after j matches
        elif i < N and pat[j] != txt[i]:
            # Do not match lps[0..lps[j-1]] characters,
            # they will match anyway
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1


def computeLPSArray(pat, M, lps):
    len = 0  # length of the previous longest prefix suffix

    lps[0]  # lps[0] is always 0
    i = 1

    # the loop calculates lps[i] for i = 1 to M-1
    while i < M:
        if pat[i] == pat[len]:
            len += 1
            lps[i] = len
            i += 1
        else:
            # This is tricky. Consider the example.
            # AAACAAAA and i = 7. The idea is similar
            # to search step.
            if len != 0:
                len = lps[len - 1]

                # Also, note that we do not increment i here
            else:
                lps[i] = 0
                i += 1


client.run(TOKEN)

