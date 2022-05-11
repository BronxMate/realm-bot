import discord
from discord.ext import commands
import datetime
from datetime import datetime, timedelta
from discord.ext import tasks
import aiohttp
import asyncio
import json
import io
import chat_exporter
import random
import os
from discord import DMChannel, Guild, Interaction, Role
from random import choice
import discord.ui
from discord.ui import Select, View
import fivempy



intents = discord.Intents.default()
intents.members = True      
bot = commands.Bot(command_prefix='.', intents=intents)
bot.remove_command("help")



@bot.command()
async def Hello(ctx):
    await ctx.reply('Hello')

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    if reason == None:
        await ctx.send('Please write a reason!')
        return
    await member.ban(reason=reason)
    await ctx.send(f"{member} bannolva lett! Indok: {reason}")

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    if reason == None:
        await ctx.send('Please write a reason!')
        return
    await member.kick(reason=reason)
    await ctx.send(f"{member} kickelve lett! Indok: {reason}")

@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, user: discord.User):
    guild = ctx.guild
    await guild.unban(user=user)
    await ctx.send(f'{user} unbannolva lett!')


@bot.command(case_insensitive=True)
@commands.has_permissions(ban_members=True)
async def warn(ctx, member:discord.Member, *, reason=None):
    
    if reason == None:
        await ctx.send('Please write a reason!')
        return
    
    


    guild = ctx.guild
    warn1 = discord.utils.get(guild.roles, name = "Warn-1")
    warn2 = discord.utils.get(guild.roles, name = "Warn-2")
   
    
    await member.add_roles(warn1)
    await ctx.send(f"{member.mention} was warned. Reason: {reason}")

    if warn == True:
        await member.add_roles(warn2)





@bot.command(case_insensitive=True)
@commands.has_permissions(ban_members=True)
async def rewarn(ctx, member:discord.Member, *, reason=None):


    guild = ctx.guild
    role = discord.utils.get(member.roles, name = "Warn-1")

    if "Warn-1" == False:
        await ctx.send(f"{member.mention} is not")
        return
        
    
    
    await member.remove_roles(role)
    await ctx.send(f"You removed the warning from {member.mention}")

     


@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear (ctx, amount= 100):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f'{amount} messages were deleted', delete_after=1)
    


    

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('Realm Roleplay'))



@bot.command()
async def suggest(ctx, *, suggestion):
    await ctx.channel.purge(limit=1)

    suggestEmbed = discord.Embed(colour=0xfecb01)
    suggestEmbed.set_author(name =f'{ctx.message.author}', icon_url=f'{ctx.author.avatar.url}')
    suggestEmbed.add_field(name= 'Ötlet', value=f'{suggestion}')

    message = await ctx.send(embed=suggestEmbed)
    await message.add_reaction('\N{WHITE HEAVY CHECK MARK}')
    await message.add_reaction('\N{CROSS MARK}') 

@bot.listen()
async def on_message(message):
    if message.author == bot.user:
        return
    if message.channel.id == 970295286851305482:
        await message.delete()
    else:
        return

    suggestEmbed = discord.Embed(colour=0xfecb01)
    suggestEmbed.set_author(name =message.author, icon_url= message.author.avatar.url),
    suggestEmbed.add_field(name= 'Ötlet', value= message.content)

    message = await message.channel.send(embed=suggestEmbed)
    await message.add_reaction('\N{WHITE HEAVY CHECK MARK}')
    await message.add_reaction('\N{CROSS MARK}') 
        

    
    


 
@bot.command()    
@commands.has_permissions(manage_messages=True)
async def statuss (ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://mcapi.us/server/status?ip=server21.clans.hu&port=25644') as response:
          data = await response.json()
          data2 = (data ['players'] ['now'])
                 


    embed = discord.Embed(

        title= 'Szerver Státusz',
        description = f"Információk: Ha problémád adódik a csatlakozással, nyiss egy ticketet!" ,
        url= 'http://atroxminecraft.clans.hu/',
        timestamp=datetime.now(), 
        color= 0x206694
    )
    embed.add_field (name= "Szerver Státusz:", value = ('\N{WHITE HEAVY CHECK MARK}') , inline= True)
    embed.add_field (name= "Szerver Ip", value= "atroxmc.clan.hu", inline = True)
    embed.add_field (name= "Szerver verziója", value= "1.16.5-1.18.2", inline = True)
    embed.add_field (name= "Online Játékosok", value = "Hamarosan" , inline= True)
    

    msg= await ctx.send(embed=embed)


@bot.command()
@commands.has_permissions(ban_members=True)
async def poll(ctx, *, message):
    await ctx.channel.purge(limit=1)
    channel = bot.get_channel(959499680117559297)

    Embed = discord.Embed(colour=0x206694)
    Embed.add_field(name= 'Szavazás', value=f'{message}')

    message = await channel.send(embed=Embed)
    await message.add_reaction('\N{WHITE HEAVY CHECK MARK}')
    await message.add_reaction('\N{CROSS MARK}') 

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(964444958662725652)
    await channel.send(f'Üdvözlünk a szerveren {member.mention}!')
    await member.send(f'Olvasd el a szerver és a discord szabályzatot {member.mention}!')



        
#final options class
class final(discord.ui.View):
    def init(self):
        super().init(timeout=None)
    #re-open ticket button
    @discord.ui.button(label='🔓Újranyitás', style=discord.ButtonStyle.green, custom_id= 're-open ticket')
    async def Reopen_ticket_button(self, button, interaction):
        embed = discord.Embed(
            title = 'Újranyitva',
            description = f'A ticketed újra lett nyitva {interaction.user.mention} által.',
            color = (0x3D6EFF)
        )
        await interaction.response.send_message(embed=embed)
        await interaction.message.delete()
    #save transcript button
    @discord.ui.button(label='📄Transzkript mentése', style=discord.ButtonStyle.blurple, custom_id = 'save-ticket-transcript')
    async def Save_transcript_button(self, button, interaction):
        global logs
        with open('data.json', 'r') as f:
           data = json.load(f)
           global logging
           logging = data.get("logging")
        print(logging)
        logs = bot.get_channel(logging)
        channel = interaction.channel
        counter = 0
        counter += 1
        await interaction.response.send_message('A transzkript mentés alatt! Kérlek várj.', ephemeral=True)
        transcript = await chat_exporter.export(bot_set_timezone='Europe')
        transcript_file = discord.File(io.BytesIO(transcript.encode()),filename=f"{channel.name}.html")
        await logs.send(file=transcript_file)
        await interaction.response.send_message('Transzkript mentve!', ephemeral=True)
    #delete button
    @discord.ui.button(label='⛔Ticket bezárása', style=discord.ButtonStyle.red, custom_id = 'delete-ticket')
    async def Delete_button(self, button, interaction):
        channel = interaction.channel
        await channel.send('A ticketed 3 másodpercen belül be lesz zárva.')
        await channel.send('https://media.giphy.com/media/2kMEaQH2aPtUWbYyLV/giphy.gif%27)')
        await asyncio.sleep(3)
        await channel.delete()


bot.persistent_views_added = False
#confirmation class
class Confirm(discord.ui.View):
    def init(self):
        super().init(timeout=None)
    #no button
    @discord.ui.button(label='Mégse', style=discord.ButtonStyle.red, custom_id = 'no-button')
    async def no_button(self, button, interaction):
        channel = interaction.channel
        await interaction.response.send_message('A ticketed nem lett bezárva!', ephemeral=True)
        await interaction.message.delete()
    #yes button
    @discord.ui.button(label='Folytatás', style=discord.ButtonStyle.success, custom_id = 'yes-button')
    async def yes_button(self, button, interaction):
        channel = interaction.channel
        embed = discord.Embed(
            title = 'Bezárva',
            description = f'A ticketed be lett zárva {interaction.user.mention} által.',
            color = (0x3D6EFF))
        await channel.send(embed=embed, view =final())
        await interaction.message.delete()
@bot.command()
@commands.has_permissions(ban_members=True)
async def add(ctx, member: discord.Member=None):
    if ctx.message.channel.name.startswith('ticket'):
        await ctx.message.channel.set_permissions(member, view_channel=True)
        await ctx.send(f'{member} hozzá lett adva a tickethez')

@bot.command()
@commands.has_permissions(ban_members=True)
async def remove(ctx, member: discord.Member=None):
    if ctx.message.channel.name.startswith('ticket'):
        await ctx.message.channel.set_permissions(member, view_channel=False)
        await ctx.send(f'{member} el lett távolítva a ticketből')

class Close(discord.ui.View):
    def init(self):
        super().init(timeout=None)
    async def interaction_check(self, interaction):
        
        return interaction.user.guild_permissions.manage_roles
    #close ticket
    @discord.ui.button(label='🔒Ticket bezárása', style=discord.ButtonStyle.red, custom_id = 'close-ticket')
    async def Close_ticket_button(self, button, interaction):
        channel = interaction.channel
        embed = discord.Embed(
            title = 'Bizots vagy benne hogy bezárod a ticketet??',
            color = (0x3D6EFF))
        await channel.send(embed=embed, view = Confirm())
        #claim ticket
    @discord.ui.button(label='🙋‍♂️Ticket begyűjtése', style=discord.ButtonStyle.success, custom_id = 'claim-ticket')
    async def CLaim_ticket_button(self, button, interaction):
        channel = interaction.channel
        embed = discord.Embed(
            title = f'Ticket begyűjtve',
            description = f'A ticketedet kézbe vette {interaction.user.mention}.',
            color = (0x3D6EFF)
        )
        await channel.edit(topic = f"A ticketed be lett gyűjtve {interaction.user} által")
        await channel.send(embed=embed)
        button.disabled=True
        button.label = '✅Begyűjtve'
        await interaction.response.edit_message(view=self)
class Ticket(discord.ui.View):
    def init(self):
        super().init(timeout=None)
    @discord.ui.button(label='📩Ticket nyitása', style=discord.ButtonStyle.blurple, custom_id = 'open-ticket')
    async def button_callback(self, button, interaction):
        guild = interaction.guild
        category = discord.utils.get(guild.categories, name='Tickets')
        if category is None:
            category = await guild.create_category(name='Tickets')
            await category.edit(position=0)
        else:
            pass
        ticket = await guild.create_text_channel(name=f'ticket--{interaction.user.display_name}', category=category)
        await interaction.response.send_message(f'A ticketed sikeresen elkészült! {ticket.mention}', ephemeral=True)
        await ticket.set_permissions(guild.default_role, view_channel=False)
        await ticket.set_permissions(interaction.user, view_channel=True)
        await ticket.send(f'Szia! {interaction.user.mention}, hamarosan egy staff tag kézbeveszi a ticketed! ')
        embed = discord.Embed(
            title = 'Nyomd meg a piros gombot, hogy bezárd a ticketet.',
            color = (0x3D6EFF))
        await ticket.send(embed=embed, view=Close())

TicketEmbeds = []
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def ticket(ctx, channel: discord.TextChannel=None):
    await ctx.message.delete()
    if (channel == None):
        guild = ctx.guild
        embed = discord.Embed(
            title = 'Ticket',
            description = 'Nyomd meg ezt a gombot, hogy nyiss egy ticketet.',
            color = (0x3D6EFF)
            )
        await ctx.send(embed=embed, view=Ticket())
    else:
        guild = ctx.guild
        embed = discord.Embed(
            title = 'Ticket',
            description = 'Nyomd meg ezt a gombot, hogy nyiss egy ticketet.',
            color = (0x3D6EFF)
            )
        await channel.send(embed=embed, view=Ticket())
#bot.events

  

@bot.command()  
@commands.has_permissions(ban_members=True)
async def giveaway(ctx, mins : int, *, prize : str):
    
    await ctx.send('@everyone')
    
    embed = discord.Embed(title = 'Nyereményjáték!')    
    embed.add_field(name='Prize', value=f'{prize}')
    end =datetime.utcnow() +    timedelta(seconds = mins*60)
    embed.add_field(name = 'Véget ér ekkor:', value = f'{end}')
    embed.set_footer(text= f'Vége {mins} perc múlva.' )

    my_msg = await ctx.send(embed=embed)

    await my_msg.add_reaction("🎉")
    
    await asyncio.sleep(mins*3600)

    new_msg = await ctx.channel.fetch_message(my_msg.id)

    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(bot.user))

    winner = random.choice(users)
   
    await ctx.send(f'{winner.mention}')

    embed=discord.Embed(title = 'Győztes!', description = f'{winner.mention}' )
    embed.set_thumbnail(url=winner.avatar_url)
    embed.add_field(name = 'Nyeremény', value=f'{prize}')
    embed.set_footer(text = 'A sorsolás véget ért!')
    await ctx.send(embed = embed)

    server = ctx.message.guild

    await winner.send(f'Megnyerted a sorsolást {server.name}')

    
@bot.command()
@commands.has_permissions(ban_members=True)
async def list(ctx):
    await ctx.send("Szar szerverek listája: 1. 37.221.214.50:25597 BARCRAFT 1.18.1 ")
                                            

                 

@bot.command()
async def help(ctx):
    embed = discord.Embed(

        title= 'Help',
        description = "These are the commands that you can use." ,
        url= '',
        timestamp=datetime.now(), 
        color= 0x206694
    )
    embed.add_field (name= "Suggestion", value= "suggest (Usage: .suggest [message]", inline = True)
    #embed.add_field (name= " ", value= " ", inline = True)
    #embed.add_field (name= "yes", value = "Hamarosan" , inline= True)
    
    msg= await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(kick_members=True)
async def mhelp(ctx):
    embed = discord.Embed(
        
        title = 'Moderation Help',
        description = "These are the commands that you can use for moderating, if you don't know how to use them do .help [command]",
        url = '',
        timestamp=datetime.now(),
        color= 0x206694
    )
    embed.add_field (name= "Moderation", value = ('kick, ban, unban, mute, unmute, clear') , inline= True)
    msg = await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(kick_members=True)
async def helpkick(ctx):
    await ctx.send(".kick [@member] [reason]")

@bot.command()
@commands.has_permissions(kick_members=True)
async def helpban(ctx):
    await ctx.send(".ban [@member] [reason]")

@bot.command()
@commands.has_permissions(kick_members=True)
async def helpunban(ctx):
    await ctx.send(".unban [discordid]")

@bot.command()
@commands.has_permissions(kick_members=True)
async def helpmute(ctx):
    await ctx.send(".mute [@member] [reason]")

@bot.command()
@commands.has_permissions(kick_members=True)
async def helpunmute(ctx):
    await ctx.send(".unmute [@member]")



@bot.command(case_insensitive=True)
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    if reason == None:
        await ctx.send('Please write a reason!')
        return
    guild = ctx.guild
    muteRole = discord.utils.get(guild.roles, name = "Muted")
 
 
    for channel in guild.channels:
            await channel.set_permissions(muteRole, speak=False, send_messages=False, read_messages=True, read_message_history=True)
    await member.add_roles(muteRole, reason=reason)
    await ctx.send(f"{member.mention} was muted. Reason: {reason}")
    
 
@bot.command(case_insensitive=True)
async def unmute(ctx, member: discord.Member, *, reason=None):
 
    guild = ctx.guild
    muteRole = discord.utils.get(guild.roles, name = "Muted")
 
    await member.remove_roles(muteRole, reason=reason)
    await ctx.send(f"{member.mention} was unmuted.")
    

  


@bot.command()
async def rang(ctx, member: discord.Member, role: discord.Role, *, reason=None):
    if reason == None:
        await ctx.send('Kérlek írj indokot')
        return
    await ctx.message.delete()
    rangembed = discord.Embed(colour=0xfecb01)
    rangembed.set_author(name=f'{ctx.message.author} rang kérelme')
    rangembed.add_field(name='Név: ', value=member.mention)
    rangembed.add_field(name='Rang: ', value=role.mention)
    rangembed.add_field(name='Indok: ', value=reason)

    msg = await ctx.send(embed=rangembed)
    await msg.add_reaction("✅")

    def check(reaction, user):
        return user.guild_permissions.manage_roles and user.top_role > role and reaction.message.id == msg.id


    try:
        reaction, user = await bot.wait_for('reaction_add',timeout=180, check=check, )
    except asyncio.TimeoutError:
        await ctx.send("kész")
    else:
        if str(reaction.emoji) == '✅':
            await member.add_roles(role)

@bot.command()
async def rangle(ctx, member: discord.Member, role: discord.Role, *, reason=None):
    if reason == None:
        await ctx.send('Kérlek írj indokot')
        return
    guild = ctx.guild
    fjump = discord.utils.get(guild.roles, name = "FRAKCIÓJUMP")
    await ctx.message.delete()
    rangembed = discord.Embed(colour=0xfecb01)
    rangembed.set_author(name=f'{ctx.message.author} rang kérelme')
    rangembed.add_field(name='Név: ', value=f"{member.mention}")
    rangembed.add_field(name='Rang: ', value=f"{role.mention}")
    rangembed.add_field(name='Indok: ', value=f"{reason}")

    msg = await ctx.send(embed=rangembed)
    await msg.add_reaction("✅")
    await msg.add_reaction("🇫")

    def check(reaction, user):
        return user.guild_permissions.manage_roles and user.top_role > role and reaction.message.id == msg.id


    try:
        reaction, user = await bot.wait_for('reaction_add',timeout=180, check=check, )
    except asyncio.TimeoutError:
        await ctx.send("kész")
    else:
        if str(reaction.emoji) == '✅':
            await member.remove_roles(role)
    try:
        reaction, user = await bot.wait_for('reaction_add',timeout=180, check=check, )
    except asyncio.TimeoutError:
        await ctx.send("kész")

    else:
        if str(reaction.emoji) == '🇫':
            await member.add_roles(fjump)
            
    
    
        
  
  




@bot.command()
@commands.has_permissions(ban_members=True)
async def removerole(ctx, member: discord.Member, *, role:discord.Role):
    
    await member.remove_roles(role)
    await ctx.send(f"You remove a {role.mention} from {member.mention}")


@bot.command()
@commands.has_permissions(ban_members=True)
async def membercount(ctx, members:discord.Member):
    await ctx.send(f"There are {members} on the server")
    


@bot.command()
async def gold(ctx):
    await ctx.send("Aranyköpések")
    await ctx.send("Vibal: 'A Visual studio nehezebb mint a python?'")
    await ctx.send("DudaLevko11: 'Kevés az FPS-em mert nem jó az internet'")


@bot.command()
async def bug(ctx, *, message2):
    await ctx.channel.purge(limit=1)
    bugEmbed = discord.Embed(colour=0xfecb01)
    bugEmbed.set_author(name =f'{ctx.message.author}', icon_url = f'{ctx.author.avatar.url}')
    bugEmbed.add_field(name ='Bug jelentés', value = 'Sikeresen rögzítettük az általad beküldött problémát!')

    message = await ctx.send(embed=bugEmbed)
    
    
    channel = bot.get_channel(963716962180009984)
    
    bugEmbed2 = discord.Embed(colour=0xfecb01)
    bugEmbed2.set_author(name =f'{ctx.message.author}', icon_url = f'{ctx.author.avatar.url}')
    bugEmbed2.add_field(name ='bug', value=f'{message2}')

    message = await channel.send(embed=bugEmbed2)




@bot.listen("on_raw_reaction_add")
async def on_raw_reaction_add(payload):
    ourMessageID = 964934552927756349
    if ourMessageID == payload.message_id: 
        member = payload.member
        guild = member.guild

        emoji = payload.emoji.  name
        if emoji == '\N{WHITE HEAVY CHECK MARK}':
            role = discord.utils.get(guild.roles, name="|🎮| Játékos")
        await member.add_roles(role)




@bot.listen("on_raw_reaction_add")
async def on_raw_reaction_add(payload):
    ourMessageID = 973607698262265896
    if ourMessageID == payload.message_id: 
        member = payload.member
        guild = member.guild

        emoji = payload.emoji.name
        if emoji == '👀':
            role = discord.utils.get(guild.roles, name="|👀| Frakciót keresek")
        await member.add_roles(role)





@bot.command(pass_context=True)
@commands.has_permissions(manage_messages=True)
async def verify (ctx):
    embed = discord.Embed(
        title= 'Frakciót keresek.',
        description = 'Amennyiben frakciót keresel, nyomd meg a 👀-t, hogy Frakciót keresek rangot kapj, ezáltal értesülni fogsz a frakció tagfelvételekről.',
        url= '',
        color= 0xfecb01
    )

    msg= await ctx.send(embed=embed)
    await msg.add_reaction('👀')


@bot.command()
@commands.has_permissions(ban_members=True)
async def cho(ctx):
    select = Select(
    placeholder="Make a selec",
    options=[
        discord.SelectOption(label="Smile", emoji="😀", description="Smile"),
        discord.SelectOption(label="Moon", emoji= "🌒", description="Moon")
        
        ])
    view = View()   
    view.add_item(select)


    await ctx.send("Test", view=view)

server = fivempy.Server("87.237.52.47:30226")





bot.run('OTU5MTA4MzY0MDg2OTM1NjIw.YkXFRQ.wVUxBmUImW5vFaydpzr1-szTjVE')