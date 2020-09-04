import discord
import pyodbc
import pandas as pd

def CheckTableExistance(conn,cursor):
    query = """
        IF not EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES   WHERE TABLE_TYPE='BASE TABLE' AND TABLE_NAME='DiscordHistory') 
    	Begin
    	create table DiscordHistory(
    	[pk_id] [int] IDENTITY(1,1) NOT NULL,

    	[Query] [varchar](200) NULL,

    	[CreationDate] [datetime] NULL
    	)
    	End"""
    cursor.execute(query)
    conn.commit()

def SaveQueryInDataBase(conn,Substr):

    cursor = conn.cursor()
    #check if table exist else create the table in database
    CheckTableExistance(conn,cursor)

    query="insert into DiscordHistory(Query,CreationDate) select '" + str(Substr) + "',getdate()"
    cursor.execute(query)
    conn.commit()


def CreateMSSQLConnection(Connection_string):
    conn= pyodbc.connect(Connection_string)
    return conn

def GetSearchHistory(conn):
    cursor = conn.cursor()
    # check if table exist else create the table in database
    CheckTableExistance(conn,cursor)
    query="select distinct Query Query,convert(datetime, CreationDate, 103) Cdate from DiscordHistory order by convert(datetime, CreationDate, 103) desc"
    conn.commit()
    df = pd.read_sql_query(query, conn)
    return list(df['Query'])

def GetQuerySubString(msg,flag):
    if(flag==1):
        return msg.replace('!recent ', '')
    else:
        return msg.replace('!google ', '')


def PrintResults(Hist,Substr):
    embed = discord.Embed(colour=discord.Colour.green())
    embed.set_author(name='Recent Search Results')
    c = 0
    for i in range(len(Hist)):
        if (KMPSearchForPatternMatching(Substr, Hist[i])):
            embed.add_field(name='' + str(c + 1) + ' Result', value=Hist[i], inline=False)
            c = c + 1
    if (c == 0):
        embed.add_field(name='No recent history found ', value=Substr, inline=False)

    return embed

def GetTop5Links(search_items):
    arr = []
    for i, search_item in enumerate(search_items, start=1):
        if (i > 5): break
        link = search_item.get("link")
        arr.append(link)
    return arr

def PrintResult(ll):
    embed = discord.Embed(colour=discord.Colour.green())
    embed.set_author(name='Top 5 google Search Results')
    for i in range(len(ll)):
        embed.add_field(name='' + str(i + 1) + 'Result', value=ll[i], inline=False)
    return embed


def GetAllValidCommands():
    discord.Embed(colour=discord.Colour.green())
    embed.set_author(name='Help : list of commands available')
    embed.add_field(name='!google [Search Query]', value='Returns top 5 Google Search Results of given Query',
                    inline=False)
    embed.add_field(name='!recent [Query]', value='Returns recent searched query using !google.', inline=False)
    return embed


def KMPSearchForPatternMatching(pat, txt):
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

