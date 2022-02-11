import discord
import random
import datetime
import os 
import os
from discord.utils import get 
import youtube_dl
from discord.ext import commands 
import requests
from PIL import Image, ImageFont, ImageDraw
import io




PREFIX = '.'
bot = commands.Bot( command_prefix = PREFIX)
bot.remove_command( 'help' )

#Words

hello_words = [ 'hello', 'hi', 'привет', 'privet', 'хай', 'ky', 'ку', 'здарова']

answer_words = [ 'узнать информацию о сервере', 'какая информация', 'команды', 
                'команды сервера', 'что здесь делать', 'что за сервер?' ]

goodbye_words = [ 'poka', 'пока', 'алидеберчи', 'bb all', 'bb', 'удачи всем', 'пока всем', 'пока сервер', 'алидеберчи'  ]

bad_words = [ 'флуд', 'далбаеб', 'дурак', 'шлюха', 'сука', 'иди нахуй', 'пошел нахуй', 'дура', 'иди нах', 'пошел нах', 'бля', '6лять', '6ля']

uzbek_words = [ 'salom', 'qalaysilar?', 'nagap', 'nimagap', 'salom bolla' ]

godd_uzbek = [ 'bopdi man ketdim', 'bopdi', 'xayr', 'hayr', 'boladi bolla man ketdim', 'man ketivoman']



@bot.event

async def on_ready():
    print( 'BOT CONNECTED' )
    await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game("Kristal Team")) 
# Выдача роля

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(938082368219123813) # Передайте ID канала
    role = discord.utils.get(member.guild.roles, id=937386428822847521) # Передайте ID роли

    await member.add_roles(role)
    await channel.send( embed = discord.Embed(description = f'Пользователь ``{ member.name}``, присоединился к нам!', color = 0x0c0c0c) )

# Clear message
@bot.command( pass_context = True )
@commands.has_permissions(administrator=True)
async def clear(ctx,amount : int):
    await ctx.channel.purge(limit = amount )
#Error
@bot.event
async def on_command_error(ctx,error):
    pass
# Clear 2
@clear.error
async def clear_error(ctx, error):
    if isinstance( error, commands.MissingRequiredArgument ):
        await ctx.send( f'{ ctx.author.name }, обязательно укажите аргумент!')

    if isinstance( error, commands.MissingPermissions ):
        await ctx.send( f'{ ctx.author.name }, у вас недостаточно прав!')


# Clear command
@bot.command(pass_context = True )
@commands.has_permissions(administrator=True)
async def hello(ctx, amount = 1):
    await ctx.channel.purge( limit = amount )

    author = ctx.message.author
    await ctx.send( f'Hello{author.mention}' )

# Kick
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason = None):
    await ctx.channel.purge(limit=1)

    await member.kick(reason=reason)
    await ctx.send(f'Kick user {member.mention}')

#Ban
@bot.command( pass_context = True )
@commands.has_permissions( administrator = True )
async def ban(ctx, member: discord.Member, *, reason = None):
    emb = discord.Embed( title = 'Ban', colour = discord.Color.red())
    await ctx.channel.purge(limit=1)

    await member.ban(reason=reason)
    emb.set_author( name = member.name, icon_url = member.avatar_url )
    emb.add_field( name = 'Ban user', value = 'Banned user : {}'.format( member.mention ) )
    emb.set_footer( text = 'Был забанен администратором {}'.format( ctx.author.name ), icon_url = ctx.author.avatar_url )

    await ctx.send( embed = emb )
    
#Unban
@bot.command( pass_context = True )
@commands.has_permissions(administrator=True)
async def unban( ctx, *, member ):
    await ctx.channel.purge( limit = 1 )

    banned_users = await ctx.guild.bans()

    for ban_entry in banned_users:
        user = ban_entry.user

        await ctx.guild.unban( user )
        await ctx.send( f'Unbanned user { user.mention }' )

        return 


#Help
@bot.command( pass_context = True )
@commands.has_permissions(administrator=True)
async def help(ctx): 
    emb = discord.Embed( title = 'Help Menu' )

    emb.add_field( name = '{}clear'.format(PREFIX),value = 'Очистка чата')
    emb.add_field( name = '{}ban'.format(PREFIX),value = 'Выдать ограничение участнику')
    emb.add_field( name = '{}unban'.format(PREFIX),value = 'Снять огроничение участнику')
    emb.add_field( name = '{}mute'.format(PREFIX),value = 'Выдать мут игроку')
    # emb.add_field( name = '{}забрать'.format(PREFIX),value = 'Забрать кэш от игрока')
    # emb.add_field( name = '{}наградить'.format(PREFIX),value = 'Выдать кэш игроку')
    # emb.add_field( name = '{}balance'.format(PREFIX),value = 'Выдать кэш игроку')
    # emb.add_field( name = '{}cash'.format(PREFIX),value = 'Выдать кэш игроку')
    emb.add_field( name = '{}kick'.format(PREFIX),value = 'Кикнуть игрока')
    # emb.add_field( name = '{}магазин'.format(PREFIX),value = 'Узнать что находится в мазагине')
    # emb.add_field( name = '{}удалить-товар'.format(PREFIX),value = 'Что бы удалить роль с магазина')
    # emb.add_field( name = '{}добавить-роль'.format(PREFIX),value = 'Что бы добавить роль в магазин')
    emb.add_field( name = '{}time'.format(PREFIX),value = 'Узнать время')
    emb.add_field( name = '{}send_m'.format(PREFIX),value = 'Приветстиве от игрока')
    emb.add_field( name = '{}send_a'.format(PREFIX),value = 'Приветствие')
    emb.add_field( name = '{}я, карта'.format(PREFIX),value = 'Карточка игрока')
    emb.add_field( name = '{}join'.format(PREFIX),value = 'Подключить бота в канал')
    emb.add_field( name = '{}leave'.format(PREFIX),value = 'отключить бот от канала')
    await ctx.send( embed = emb)


#Mute
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member):
    await ctx.channel.purge(limit=1)

    mute_role = discord.utils.get(ctx.message.guild.roles, name = "mute")

    await member.add_roles(mute_role)
    await ctx.send(f"{member.mention} вы нарушали правила #〘📚〙дискорд-правила")

#join
@bot.command(name="join", brief="Подключение к голосовому каналу", usage="join")
async def join(ctx):
    global voice
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    channel = ctx.message.author.voice.channel

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        await ctx.send(f"Bot was connected to the voice channel")

#leave
@bot.command(name="leave", brief="Отключение от голосового канала", usage="leave")
async def leave(ctx):
    global voice
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    channel = ctx.message.author.voice.channel

    if voice and voice.is_connected():
        await voice.disconnect()
    else:
        voice = await channel.disconnect()
        await ctx.send(f"Bot was connected to the voice channel")

#Музыка
@bot.command()
async def play( ctx, url : str ):
    song_there = os.path.isfile('song.mp3')

    try:
        if song_there:
            os.remove('song.mp3')
            print('[log] Старый файл удален!')
    except PermissionEror:
        print('[log] Не удалось удалить файл!')

    await ctx.send('Пожалуйста ожидайте.')

    voice = get(client.voice_clients, guild = ctx.guild)

    ydl_opts = {
        'format' : 'bestaudio/best',
        'postprocessors' : [{
            'key' : 'FFmpegExtartAudio',
            'preferredcodec' : 'mp3',
            'preferredqualit' : '192'

        }]
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print('[log] Загружаю музыку....')
        ydl.download([url])

    for file in os.listdir('./'):
        if file.endswith('.mp3'):
            name = file 
            print(f'[log] Переименовываю файл: {file}')
            os.rename(file, 'song.mp3')

    voice.play(discord.FFmpegPCMAudio('song.mp3'), after = lambda e: print(f'[log] { name }, музыка закончилась свое проигрывание.'))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    song_name = name.rsplit('-', 2)
    await ctx.send(f'Сейчас проигрывает музыка: { song_name[0]}')

# Карточка 


@bot.command( aliases = ['Я', 'карта']) #.я
async def card_user(ctx):
    await ctx.channel.purge(limit = 1)

    img = Image.new('RGBA', (400,200), '#232529')
    url = str(ctx.author.avatar_url)[:-10] #size = 1024

    respons = requests.get(url, stream = True )
    respons = Image.open(io.BytesIO(respons.content))
    respons = respons.convert('RGBA')
    respons = respons.resize((100, 100), Image.ANTIALIAS)

    img.paste(respons, (15, 15, 115, 115))

    idraw = ImageDraw.Draw(img)
    name = ctx.author.name # Kristalix
    tag = ctx.author.discriminator # 5024

    headline = ImageFont.truetype('arial.ttf', size = 20)
    undertext = ImageFont.truetype('arial.ttf', size = 12)

    idraw.text((145, 15),f'{name}#{tag}', font = headline) #Kristalix#5024
    idraw.text((145, 15), f'ID: {ctx.author.id}', font = undertext)

    img.save('user_card.png')

    await ctx.send(file = discord.File(fp = 'user_card.png'))


#Красивый ввод
@bot.command( pass_context = True )
@commands.has_permissions(administrator=True)

async def time( ctx ):
    emb = discord.Embed( title = 'Your time', description = 'Вы можете узнать текущее время', colour = discord.Color.green(), url = 'https://www.timeserver.ru/cities/kz/taldykorgan')

    emb.set_author( name = bot.user.name, icon_url = bot.user.avatar_url )
    emb.set_footer( text = 'Спасибо за использование нашего бота!' )
   
    now_date = datetime.datetime.now()
    emb.add_field( name = 'Time', value = 'Time : {}'.format(now_date) )
    
    await ctx.send( embed = emb )




#words answers
@bot.event

async def on_message( message ):
    await bot.process_commands(message)
    msg = message.content.lower()
    if msg in hello_words:
        await message.channel.send( 'Хай,чего хотел?' )
    if msg in answer_words:
        await message.channel.send( 'Пропиши в чат команду .help, и все узнаешь!' )
    if msg in goodbye_words:
        await message.channel.send( 'Пока,удачи тебе!' )
    if msg in uzbek_words:
        await message.channel.send( 'Salom,yaxshimisan?' )
    if msg in godd_uzbek:
        await  message.channel.send( 'Xayr,omad tilayman!' )
    if msg in bad_words:
        await message.channel.send( 'Э-э-э ты че апупел?! Забаню щяс, удали!' )
    if msg in bad_uzbek:
        await message.channel.send( 'Udalit qimaseng BAN!' )
# СООБЩЕНИЕ
@bot.command()
async def send_a( ctx ):
    await ctx.author.send( 'Хай добро пожаловать на наш сервер старайся не нарушать правила!' )

@bot.command()
async def send_m( ctx, member: discord.Member ):
    await member.send( f'{ member.name }, привет от  { ctx.author.name}' )
#Connect

token = open( 'token.txt', 'r' ).readline()

bot.run ( token )
