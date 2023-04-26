import discord
import datetime
from discord import Option
from discord.ext import commands
from discord.ext.tasks import loop
from discord.ext.commands import MissingPermissions , Bot
import os # default module
from dotenv import load_dotenv
from discord.ui import *
from datetime import datetime
import asyncio
import sys
from discord.utils import get
from config import activitytype, botstatusmessage, embedcolor, developerid, statscooldownamount, guildID, IDofChannelForServerMembers, NameofStatsChannel1, Role1CountCheckEnabled, IDofChannelForRole1Check, NameofRole1Channel, ServerMembersCheckEnabled, IDofRole1, BotCountCheckEnabled, IDofChannelForBotCheck, NameofBotChannel, BansCountCheckEnabled, IDofChannelForBansCheck, NameofBansChannel, Role2CountCheckEnabled, IDofChannelForRole2Check, IDofRole2, NameofRole2Channel , TICKET_CHANNEL , CATEGORY_ID1 , CATEGORY_ID2 , TEAM_ROLE1 , TEAM_ROLE2 , LOG_CHANNEL , SAY_TITLE , ON_DUTY_ROLE , servers


intents = discord.Intents.default()

load_dotenv() # load all the variables from the env file
intents.members = True #enable in the Developer Portal
intents.messages = True
bot = discord.Bot(intents = intents)
client = bot = commands.Bot(command_prefix='!', intents=intents)

###############################################################ON-OFF DUTY

bot.duties = {}
@bot.slash_command(guild_ids =servers ,name = "dutymenu", description = "Duty menu")
async def hello(ctx):
    onduty = Button(label= "OnDuty", style=discord.ButtonStyle.green,emoji="🟢" , custom_id = "onduty")
    offduty = Button(label= "OnDuty", style=discord.ButtonStyle.red,emoji="🔴" , custom_id = "offduty")
    async def onduty_callback(interaction):
        bot.duties[interaction.user.id] = datetime.now()
        await interaction.user.add_roles(interaction.guild.get_role(ON_DUTY_ROLE))
        await interaction.response.edit_message(content=f"<@{interaction.user.id}> You are on duty" , view=None ) 
    async def offduty_callback(interaction):
            prev_date = bot.duties.get(interaction.user.id, None)
            if bot.duties is not None:
                date = datetime.now()
                diff = (date - prev_date)
            await interaction.user.remove_roles(interaction.guild.get_role(ON_DUTY_ROLE))
            await interaction.response.edit_message(content= f"{round(diff.total_seconds(), 1)} secconds" , view=None )
    onduty.callback = onduty_callback
    offduty.callback = offduty_callback
    view = View()
    view.add_item(onduty)
    view.add_item(offduty)
    await ctx.respond("`Duty menu`" , view=view , ephemeral=True)
############################################################SAY

@bot.slash_command(guild_ids =servers , name = "say", escription = "embeded creator")
async def say(ctx, emb: Option(str, required = True , description = "enter message")):
    embed=discord.Embed(title = f"{SAY_TITLE}", description=f"{emb}", color=0x000000)
    await ctx.send(embed=embed)
    await ctx.respond("`Success`" , ephemeral=True)
######################################################################################################## timeoute mute     
@bot.slash_command(guild_ids =servers , name = 'timeout', description = "mutes/timeouts a member")
@commands.has_permissions(moderate_members = True)
async def timeout(ctx, member: Option(discord.Member, required = True), reason: Option(str, required = False), days: Option(int, max_value = 27, default = 0, required = False), hours: Option(int, default = 0, required = False), minutes: Option(int, default = 0, required = False), seconds: Option(int, default = 0, required = False)): #setting each value with a default value of 0 reduces a lot of the code
    if member.id == ctx.author.id:
        await ctx.respond("You can't timeout yourself!")
        return
    if member.guild_permissions.moderate_members:
        await ctx.respond("You can't do this, this person is a moderator!")
        return
    duration = timedelta(days = days, hours = hours, minutes = minutes, seconds = seconds)
    if duration >= timedelta(days = 28): #added to check if time exceeds 28 days
        await ctx.respond("I can't mute someone for more than 28 days!", ephemeral = True) #responds, but only the author can see the response
        return
    if reason == None:
        await member.timeout_for(duration)
        await ctx.respond(f"<@{member.id}> has been timed out for {days} days, {hours} hours, {minutes} minutes, and {seconds} seconds by <@{ctx.author.id}>.")
    else:
        await member.timeout_for(duration, reason = reason)
        await ctx.respond(f"<@{member.id}> has been timed out for {days} days, {hours} hours, {minutes} minutes, and {seconds} seconds by <@{ctx.author.id}> for '{reason}'.")

@timeout.error
async def timeouterror(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.respond("You can't do this! You need to have moderate members permissions!")
    else:
        raise error

@bot.slash_command(guild_ids =servers, name = 'unmute', description = "unmutes/untimeouts a member")
@commands.has_permissions(moderate_members = True)
async def unmute(ctx, member: Option(discord.Member, required = True), reason: Option(str, required = False)):
    if reason == None:
        await member.remove_timeout()
        await ctx.respond(f"<@{member.id}> has been untimed out by <@{ctx.author.id}>.")
    else:
        await member.remove_timeout(reason = reason)
        await ctx.respond(f"<@{member.id}> has been untimed out by <@{ctx.author.id}> for '{reason}'.")

@unmute.error
async def unmuteerror(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.respond("You can't do this! You need to have moderate members permissions!")
    else:
        raise error    
#====================================================unban=========================================================================    
@bot.slash_command(guild_ids =servers, name = "unban", description = "Unbans a member")
@commands.has_permissions(ban_members = True)
async def unban(ctx, id: Option(discord.Member, description = "The User ID of the person you want to unban.", required = True)):
    await ctx.defer()
    member = await bot.get_or_fetch_user(id)
    await ctx.guild.unban(member)
    await ctx.respond(f"I have unbanned {member.mention}.")

@unban.error
async def unbanerror(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.respond("You need ban members permissions to do this!")
    else: 
        await ctx.respond(f"Something went wrong, I couldn't unban this member or this member isn't banned.")
        raise error
    
    
    
    #==========================================================ban/kick===================================================================================
@bot.slash_command(guild_ids =servers, name = "ban", description = "Bans a member")
@commands.has_permissions(ban_members = True, administrator = True)
async def ban(ctx, member: Option(discord.Member, description = "Who do you want to ban?"), reason: Option(str, description = "Why?", required = False)):
    if member.id == ctx.author.id: #checks to see if they're the same
        await ctx.respond("BRUH! You can't ban yourself!")
    elif member.guild_permissions.administrator:
        await ctx.respond("Stop trying to ban an admin! :rolling_eyes:")
    else:
        if reason == None:
            reason = f"None provided by {ctx.author}"
        await member.ban(reason = reason)
        await ctx.respond(f"<@{ctx.author.id}>, <@{member.id}> has been banned successfully from this server!\n\nReason: {reason}")
    
@ban.error
async def banerror(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.respond("You need Ban Members and Administrator permissions to do this!")
    else:
        await ctx.respond("Something went wrong...") #most likely due to missing permissions
        raise error

@bot.slash_command(guild_ids =servers, name = "kick", description = "Kicks a member")
@commands.has_permissions(kick_members = True, administrator = True)
async def kick(ctx, member: Option(discord.Member, description = "Who do you want to kick?"), reason: Option(str, description = "Why?", required = False)):
    if member.id == ctx.author.id: #checks to see if they're the same
        await ctx.respond("BRUH! You can't kick yourself!")
    elif member.guild_permissions.administrator:
        await ctx.respond("Stop trying to kick an admin! :rolling_eyes:")
    else:
        if reason == None:
            reason = f"None provided by {ctx.author}"
        await member.kick(reason = reason)
        await ctx.respond(f"<@{ctx.author.id}>, <@{member.id}> has been kicked from this server!\n\nReason: {reason}")

@kick.error
async def kickerror(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.respond("You need Kick Members and Administrator permissions to do this!")
    else:
        await ctx.respond("Something went wrong...") #most likely due to missing permissions 
        raise error  
           #==============================================================================logs=============================================================================

#############################################################ANTISPAM
class Client(discord.Client):
    def __init__(self):
        intents = discord.Intents.default() #antispam doesn't need message content intent
        super().__init__(intents = intents)
        self.anti_spam = commands.CooldownMapping.from_cooldown(5, 15, commands.BucketType.member)
        self.too_many_violations = commands.CooldownMapping.from_cooldown(4, 60, commands.BucketType.member)

    async def on_ready(self):
        print(f'We have logged in as {self.user}.')
    
    async def on_message(self, message):
        if type(message.channel) is not discord.TextChannel or message.author.bot: return
        bucket = self.anti_spam.get_bucket(message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            await message.delete()
            await message.channel.send(f"{message.author.mention}, don't spam!", delete_after = 10)
            violations = self.too_many_violations.get_bucket(message)
            check = violations.update_rate_limit()
            if check:
                await message.author.timeout(timedelta(minutes = 10), reason = "Spamming")
                try: await message.author.send("You have been muted for spamming!")
                except: pass
    
    
    
    
    
#serverstats
#Defs:#
def filterOnlyBots(member):
    return member.bot

#Loops:#
@loop(seconds=statscooldownamount)
async def checkallmembers():
    try:
        guild = bot.get_guild(guildID)
        MembersInServerCount = len(guild.members)
        tchannel1 = get(guild.channels, id=IDofChannelForServerMembers)
        amount1 = (MembersInServerCount)
        prevtname = str(f'{NameofStatsChannel1}{amount1}')
        tname = tchannel1.name
        if prevtname == tname:
            pass
        elif prevtname != tname:
            await tchannel1.edit(name=f'{NameofStatsChannel1}{amount1}')
    except Exception as e:
        developer = get(guild.members, id=developerid)
        text = str('''Error on line {}'''.format(sys.exc_info()[-1].tb_lineno))
        embed = discord.Embed(title='checkallmembers function fail', description=f'{text}, {str(e)}', color=embedcolor)
        try:
            await developer.send(embed=embed)
        except discord.HTTPException:
            await developer.send("checkallmembers loop fail\n" + str(e))
        print('[ERROR][Line {}]:'.format(sys.exc_info()[-1].tb_lineno) + f'{str(e)}')
        print("----------------------------------------")

@loop(seconds=statscooldownamount)
async def checkrole1():
    try:
        guild = bot.get_guild(guildID)
        tchannel2 = get(guild.channels, id=IDofChannelForRole1Check)
        Role = get(guild.roles, id=IDofRole1)  
        Rolecount = len(Role.members)
        tname2 = tchannel2.name
        prevtname2 = str(f'{NameofRole1Channel}{Rolecount}')
        if prevtname2 == tname2:
            pass
        elif prevtname2 != tname2:
            await tchannel2.edit(name=f'{NameofRole1Channel}{Rolecount}')
    except Exception as e:
        developer = get(guild.members, id=developerid)
        text = str('''Error on line {}'''.format(sys.exc_info()[-1].tb_lineno))
        embed = discord.Embed(title='checkrole1 function fail', description=f'{text}, {str(e)}', color=embedcolor)
        try:
            await developer.send(embed=embed)
        except discord.HTTPException:
            await developer.send("checkrole1 loop fail\n" + str(e))
        print('[ERROR][Line {}]:'.format(sys.exc_info()[-1].tb_lineno) + f'{str(e)}')
        print("----------------------------------------")

@loop(seconds=statscooldownamount)
async def checkrole2():
    try:
        guild = bot.get_guild(guildID)
        tchannel6 = get(guild.channels, id=IDofChannelForRole2Check)
        Role = get(guild.roles, id=IDofRole2)  
        Rolecount = len(Role.members)
        tname6 = tchannel6.name
        prevtname6 = str(f'{NameofRole2Channel}{Rolecount}')
        if prevtname6 == tname6:
            pass
        elif prevtname6 != tname6:
            await tchannel6.edit(name=f'{NameofRole2Channel}{Rolecount}')
    except Exception as e:
        developer = get(guild.members, id=developerid)
        text = str('''Error on line {}'''.format(sys.exc_info()[-1].tb_lineno))
        embed = discord.Embed(title='checkrole2 function fail', description=f'{text}, {str(e)}', color=embedcolor)
        try:
            await developer.send(embed=embed)
        except discord.HTTPException:
            await developer.send("checkrole2 loop fail\n" + str(e))
        print('[ERROR][Line {}]:'.format(sys.exc_info()[-1].tb_lineno) + f'{str(e)}')
        print("----------------------------------------")

@loop(seconds=statscooldownamount)
async def checkbots():
    try:
        guild = bot.get_guild(guildID)
        tchannel4 = bot.get_channel(IDofChannelForBotCheck)
        MembersInServer = guild.members
        Bots = list(filter(filterOnlyBots, MembersInServer))
        botcount = len(Bots)
        prevtname4 = str(f'{NameofBotChannel}{botcount}')
        tname4 = tchannel4.name
        if prevtname4 == tname4:
            pass
        elif prevtname4 != tname4:
            await tchannel4.edit(name=f'{NameofBotChannel}{botcount}')
    except Exception as e:
        developer = get(guild.members, id=developerid)
        text = str('''Error on line {}'''.format(sys.exc_info()[-1].tb_lineno))
        embed = discord.Embed(title='checkbots function fail', description=f'{text}, {str(e)}', color=embedcolor)
        try:
            await developer.send(embed=embed)
        except discord.HTTPException:
            await developer.send("checkbots loop fail\n" + str(e))
        print('[ERROR][Line {}]:'.format(sys.exc_info()[-1].tb_lineno) + f'{str(e)}')
        print("----------------------------------------")

@loop(seconds=statscooldownamount)
async def checkbans():
    try:
        guild = bot.get_guild(guildID)
        tchannel5 = get(guild.channels, id=IDofChannelForBansCheck)
        bans = await guild.bans()
        bans2 = (len(bans))
        prevtname5 = str(f'{NameofBansChannel}{bans2}')
        tname5 = tchannel5.name
        if prevtname5 == tname5:
            pass
        elif prevtname5 != tname5:
            await tchannel5.edit(name=f'{NameofBansChannel}{bans2}')
    except Exception as e:
        developer = get(guild.members, id=developerid)
        text = str('''Error on line {}'''.format(sys.exc_info()[-1].tb_lineno))
        embed = discord.Embed(title='checkbans function fail', description=f'{text}, {str(e)}', color=embedcolor)
        try:
            await developer.send(embed=embed)
        except discord.HTTPException:
            await developer.send("checkbans loop fail\n" + str(e))
        print('[ERROR][Line {}]:'.format(sys.exc_info()[-1].tb_lineno) + f'{str(e)}')
        print("----------------------------------------")




##################################################################TICKET TEST
class MyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.select(
        custom_id="support",
        placeholder="Choose a Ticket option",
        options=[
            discord.SelectOption(
                label="Donate",
                emoji="💸",
                value="support1"
            ),discord.SelectOption(
                label="Other",
                emoji="❓",
                value="support2"
            )
        ]
    )
    async def callback(self, select, interaction):
        if "support1" in interaction.data['values']:
            if interaction.channel.id == TICKET_CHANNEL:
                guild = bot.get_guild(guildID)
                for ticket in guild.channels:
                    if str(interaction.user.id) in ticket.name:
                        embed = discord.Embed(title=f"You can only open one Ticket!", description=f"Here is your opend Ticket --> {ticket.mention}", color=0xff0000)
                        await interaction.response.send_message(embed=embed, ephemeral=True)
                        return

                category = bot.get_channel(CATEGORY_ID1)
                ticket_channel = await guild.create_text_channel(f"t-💸Donate-{interaction.user.name}", category=category,
                                                                topic=f"Ticket from {interaction.user} \nUser-ID: {interaction.user.id}")

                await ticket_channel.set_permissions(guild.get_role(TEAM_ROLE1), send_messages=True, read_messages=True, add_reactions=False,
                                                    embed_links=True, attach_files=True, read_message_history=True,
                                                    external_emojis=True)
                await ticket_channel.set_permissions(interaction.user, send_messages=True, read_messages=True, add_reactions=False,
                                                    embed_links=True, attach_files=True, read_message_history=True,
                                                    external_emojis=True)
                await ticket_channel.set_permissions(guild.default_role, send_messages=False, read_messages=False, view_channel=False)
                embed = discord.Embed(description=f'Welcome {interaction.user.mention}!\n'
                                                   'Type your message for a <@&1073604128133099601> to see',
                                                color=discord.colour.Color.green())
                await ticket_channel.send(embed=embed)


                embed = discord.Embed(description=f'📬 Ticket was Created! Look here --> {ticket_channel.mention}',
                                        color=discord.colour.Color.green())

                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
        if "support2" in interaction.data['values']:
            if interaction.channel.id == TICKET_CHANNEL:
                guild = bot.get_guild(guildID)
                for ticket in guild.channels:
                    if str(interaction.user.id) in ticket.name:
                        embed = discord.Embed(title=f"You can only open one Ticket", description=f"Here is your opend Ticket --> {ticket.mention}", color=0xff0000)
                        await interaction.response.send_message(embed=embed, ephemeral=True)
                        return

                category = bot.get_channel(CATEGORY_ID2)
                ticket_channel = await guild.create_text_channel(f"t-❓Other-{interaction.user.name}", category=category,
                                                                    topic=f"Ticket from {interaction.user} \nUser-ID: {interaction.user.id}")
                await ticket_channel.set_permissions(guild.get_role(TEAM_ROLE2), send_messages=True, read_messages=True, add_reactions=False,
                                                        embed_links=True, attach_files=True, read_message_history=True,
                                                        external_emojis=True)
                await ticket_channel.set_permissions(interaction.user, send_messages=True, read_messages=True, add_reactions=False,
                                                        embed_links=True, attach_files=True, read_message_history=True,
                                                        external_emojis=True)
                await ticket_channel.set_permissions(guild.default_role, send_messages=False, read_messages=False, view_channel=False)
                embed = discord.Embed(description=f'Welcome {interaction.user.mention}!\n'
                                                   'Type something here for a <@&1073604128103743498> meber to see',
                                                    color=discord.colour.Color.gold())
                await ticket_channel.send(embed=embed)

                embed = discord.Embed(description=f'📬 Ticket was Created! Look here --> {ticket_channel.mention}',
                                        color=discord.colour.Color.green())
                await interaction.response.send_message(embed=embed, ephemeral=True)
        return

@commands.is_owner()
@bot.slash_command(guild_ids =servers, name = "ticketcreate", description = "creates ticket")
async def ticket(ctx):
    await ctx.respond("`Succsess`", ephemeral=True)
    channel = bot.get_channel(TICKET_CHANNEL)
    embed = discord.Embed(title="🎟Tickets", description="Για την άμεση εξυπηρέτηση σας μπορείτε να ανοίξετε ένα ticket ώστε να μιλήσετε με κάποιον ανώτερο και να λύσετε το πρόβλημα σας." , color=discord.colour.Color.gold())
    await channel.send(embed=embed, view=MyView())
   	

@bot.slash_command(guild_ids =servers, name = "tclose", description = "closes ticket")
async def close(ctx):
    if "t-" in ctx.channel.name:
        channel = bot.get_channel(LOG_CHANNEL)
        closed = ctx.channel.name

        fileName = f"{ctx.channel.name}.txt"
        with open(fileName, "w") as file:
            async for msg in ctx.channel.history(limit=None, oldest_first=True):
                file.write(f"{msg.author.display_name}: {msg.clean_content}\n")

        embed = discord.Embed(
                description=f'to ticket tha klisei akoma se 5 defterolepta!',
                color=0xff0000)
        embed2 = discord.Embed(title="Ticket Closed!", description=f"Ticket-Name: {closed}\n Closed-From: {ctx.author.display_name}\n Transcript: ", color=discord.colour.Color.orange())
        file = discord.File(fileName)
        await channel.send(embed=embed2)
        await asyncio.sleep(1)
        await channel.send(file=file)       
        await ctx.send(embed=embed)
        await asyncio.sleep(5)
        await ctx.channel.delete()













######################################################################################
#Events:#


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
        message1 = ctx.message
        await message1.delete()
        author = ctx.message.author
        message2 = await ctx.send(f'{author.mention}')
        await message2.delete()
        embed = discord.Embed(description=f'''{author.mention}, Huh? I don't know that command!''', color=embedcolor)
        embed.set_author(name=f'{author}', icon_url=f'{author.avatar_url}')
        embed.add_field(name='**__Debug Error:__**', value=f'```discord.ext.commands.errors.CommandNotFound: {error}```')
        embed.set_footer(text=f'{bot.user.name} | {bot.user.id}', icon_url=bot.user.avatar_url)
        try:
            message3 = await ctx.send(embed=embed)
        except discord.HTTPException:
            message3 = await ctx.send(f'''{author.mention}, I don't know that command!''')
        await asyncio.sleep(15)
        await message3.delete()


@bot.event
async def on_message(message):
    try:
        await bot.process_commands(message)
        if message.content.startswith(f"<@!{bot.user.id}>") or message.content.startswith(f"<@{bot.user.id}>"):
            latency = bot.latency * 1000
            embed = discord.Embed(description=f'Hi there! I see that you have mentioned me! My latency is **{latency:.2f}ms**.', color=embedcolor)
            embed.set_footer(text=f'{bot.user.name} | {bot.user.id}', icon_url=bot.user.avatar_url)
            try:
                try:
                    async with message.channel.typing():
                        await asyncio.sleep(1)
                    await message.reply(embed=embed, mention_author=True)
                except discord.HTTPException:
                    await message.reply(f'Hi there! I see that you have mentioned me! My latency is **{latency:.2f}ms**``.', mention_author=True)
            except Exception:
                pass
        else:
            pass
    except Exception as e:
        developer = bot.get_user(developerid)
        text = str('''Error on line {}'''.format(sys.exc_info()[-1].tb_lineno))
        embed = discord.Embed(title='on_message event fail', description=f'{text}, {str(e)}', color=embedcolor)
        try:
            await developer.send(embed=embed)
        except discord.HTTPException:
            await developer.send("on_message event fail" + str(e))
        print('[ERROR][Line {}]:'.format(sys.exc_info()[-1].tb_lineno) + f'{str(e)}')
        print("----------------------------------------")

#Commands:#
@bot.slash_command(guild_ids =servers, name = "logout", description = "logout function")
async def logout(ctx):
    try:
        message1 = ctx.message
        author = ctx.message.author
        if author.id == developerid:
            await message1.add_reaction('✅')
            await bot.logout()
        else:
            await message1.delete()
            message5 = await ctx.send(f'{author.mention}')
            await message5.delete()
            embed5 = discord.Embed(description=f'''{author.mention}, you can't use that command! ❌''', color=embedcolor)
            embed5.set_footer(text=f'{bot.user.name} | {bot.user.id}', icon_url=bot.user.avatar_url) 
            try:
                message6 = await ctx.send(embed=embed5)
            except discord.HTTPException:
                message6 = await ctx.send(f'''{author.mention}, **you can't use that command! ❌**''')
            await asyncio.sleep(20)
            await message6.delete()
    except Exception as e:
        message2 = await ctx.send(f'{author.mention} a unknown error has occurred, a copy of the error has been sent to the developer ❌')
        developer = bot.get_user(developerid)
        text = str('''Error on line {}'''.format(sys.exc_info()[-1].tb_lineno))
        embed = discord.Embed(title='commands.logout function fail', description=f'{text}, {str(e)}', color=embedcolor)
        try:
            await developer.send(embed=embed)
        except discord.HTTPException:
            await developer.send("commands.logout function fail" + str(e))
        print('[ERROR][Line {}]:'.format(sys.exc_info()[-1].tb_lineno) + f'{str(e)}')
        print("----------------------------------------") 
        await asyncio.sleep(10)
        await message2.delete()
        
        
@bot.event
async def on_ready():
    bot.add_view(MyView())
    await bot.wait_until_ready()
    activity2 = discord.Activity(type=discord.ActivityType.playing, name="booting...")
    await bot.change_presence(status=discord.Status.idle, activity=activity2)
    print("\n/////////////////////////////////")
    print("//                             //")
    print("//    Gvol ServerStatsBot      //")
    print("//         feature             //")
    print("/////////////////////////////////\n")
    print("Bot Infomation:")
    print ("------------------------------------")
    print (f"Bot Name: {bot.user.name}#{bot.user.discriminator}")
    print (f"Bot ID: {bot.user.id}")
    creator = bot.get_user(720218422222520410)
    print(f'Creator: {creator}')    #DO NOT CHANGE#
    print ("Discord Version: " + discord.__version__)
    guild = bot.get_guild(guildID)
    print(f'Operating Guild Name: {guild}')
    print ("-----------------------------------------")
    print("[MESSAGE]: Bot has logged into discord sucessfully.")
    print("----------------------------------------------------")
    await asyncio.sleep(2)
    print("Loops Enabled/Diabled Self Check:")
    if ServerMembersCheckEnabled == True:
        print(f'Checkallmembers: Enabled')
    else:
        print(f'Checkallmembers: Disabled')
    if Role1CountCheckEnabled == True:
        print(f'Checkrole1: Enabled')
    else:
        print(f'Checkrole1: Disabled')
    if Role2CountCheckEnabled == True:
        print(f'Checkrole2: Enabled')
    else:
        print(f'Checkrole2: Disabled')
    if BotCountCheckEnabled == True:
        print(f'Checkbots: Enabled')
    else:
        print(f'Checkbots: Disabled')
    if BansCountCheckEnabled == True:
        print(f'Checkbans: Enabled')
    else:
        print(f'Checkbans: Disabled')
    print("----------------------------------------------------")
    print(f'[MESSAGE]: Starting enabled loops')
    print("----------------------------------------------------")
    await asyncio.sleep(1)
    try:
        if ServerMembersCheckEnabled == True:
            checkallmembers.start()
            await asyncio.sleep(1)
        else:
            pass
        if Role1CountCheckEnabled == True:
            checkrole1.start()
            await asyncio.sleep(1)
        else:
            pass
        if Role2CountCheckEnabled == True:
            checkrole2.start()
            await asyncio.sleep(1)
        else:
            pass
        if BotCountCheckEnabled == True:
            checkbots.start()
            await asyncio.sleep(1)
        else:
            pass
        if BansCountCheckEnabled == True:
            checkbans.start()
            await asyncio.sleep(1)
        else:
            pass
        print("[MESSAGE:] All enabled loops started sucessfully")
        print("----------------------------------------------------")
    except Exception as r:
        developer = get(guild.members, id=developerid)
        embed = discord.Embed(title='`On_Ready Function Fail (Enabled Loops Start Fail)`', description=f'{str(r)}', color=embedcolor)
        try:
            await developer.send(embed=embed)
        except discord.HTTPException:
            await developer.send("On_Ready Function Fail (Enabled Loops Start Fail)\n" + str(r))
        print("[ERROR]: Enabled loops were attempted to start running but an error occurred, the loops are most likely already running, more details have been sent to the developer specified in the config")
        print('[ERROR][Line {}]:'.format(sys.exc_info()[-1].tb_lineno) + f'{str(e)}')
        print("------------------------------------")
    if f'{activitytype}' == 'Playing':
        activity1 = discord.Activity(type=discord.ActivityType.playing, name=f'{botstatusmessage}')
        await bot.change_presence(status=discord.Status.online, activity=activity1)
    elif f'{activitytype}' == 'Streaming':
        activity1 = discord.Activity(type=discord.ActivityType.streaming, name=f'{botstatusmessage}')
        await bot.change_presence(status=discord.Status.online, activity=activity1)
    elif f'{activitytype}' == 'Watching':
        activity1 = discord.Activity(type=discord.ActivityType.watching, name=f'{botstatusmessage}')
        await bot.change_presence(status=discord.Status.online, activity=activity1)
    elif f'{activitytype}' == 'Listening':
        activity1 = discord.Activity(type=discord.ActivityType.listening, name=f'{botstatusmessage}')
        await bot.change_presence(status=discord.Status.online, activity=activity1)
    else:
        activity1 = discord.Activity(type=discord.ActivityType.playing, name=f'{botstatusmessage}')
        await bot.change_presence(status=discord.Status.online, activity=activity1)
        print('''[WARN]: You have incorrectly specified the bot's activity type, the default has been selected. ''')
        print("----------------------------------------------------")
    print("[MESSAGE]: Bot is ready!")
    print("------------------------------------")        

    
    
    
    
    
    
    
    
    
    
    
    
    
    

    
    
    
    
    
    
    
    
    
#######################################login###########################################################################################
bot.run(os.getenv('TOKEN'))