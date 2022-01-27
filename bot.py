# bot.py
import os
import random
import mysql.connector
from mysql.connector import Error
import discord
import datetime
from datetime import date
from dotenv import load_dotenv
from discord.ext import commands    

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix="$")
categorias = ["LM","ISO","FOL","FH","PAR","GBD"]
msgID = 'idiota jaja'
username = 'xD'
chID= '121'
categoria = '0'
name = ''
@bot.command()
async def ping(ctx):
	await ctx.channel.send("pong")


@bot.command()
async def Tareas(ctx):
    id = str(ctx.guild.id)
    tareas = id + '_tareas'
    query_tar = """SELECT * FROM {} WHERE DATE(enddate) >= CURDATE() ORDER BY enddate;
    """.format(tareas)
    try:
        connection = mysql.connector.connect(host=os.getenv('HOST'),
                                            database=os.getenv('DATABASE'),
                                            user=os.getenv('USER'),
                                            password=os.getenv('PASSWORD'))
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor(buffered=True)
            cursor.execute("select database();")
            cursor.execute(query_tar)
            records = cursor.fetchall()
            connection.commit()
            print(cursor.rowcount, "Record inserted successfully into Laptop table")
    except Error as e:
        print("Error while connecting to MYSQL",e)
    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")

    embedVar = discord.Embed(title="Tareas", description="-Esta es la lista de tareas para entregar en los proximos días", color=0x00ffff)
    for row in records:
        embedVar.add_field(name="{} ({})".format(row[3],row[0]), value="Hay que realizar ({}) para el dia {}".format(row[1],row[2]), inline=False)

    await ctx.send(embed=embedVar)


async def Examenes(ctx):
    id = str(ctx.guild.id)
    examenes = id + '_examenes'
    query_tar = """SELECT * FROM {} WHERE DATE(enddate) >= CURDATE() ORDER BY enddate;
    """.format(tareas)
    try:
        connection = mysql.connector.connect(host=os.getenv('HOST'),
                                            database=os.getenv('DATABASE'),
                                            user=os.getenv('USER'),
                                            password=os.getenv('PASSWORD'))
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor(buffered=True)
            cursor.execute("select database();")
            cursor.execute(query_tar)
            records = cursor.fetchall()
            connection.commit()
            print(cursor.rowcount, "Record inserted successfully into Laptop table")
    except Error as e:
        print("Error while connecting to MYSQL",e)
    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")

    embedVar = discord.Embed(title="Tareas", description="-Esta es la lista de examenes para los proximos días", color=0x00ffff)
    for row in records:
        embedVar.add_field(name=row[3], value="El examen sobre ({}) para el dia {}".format(row[1],row[2]), inline=False)

    await ctx.send(embed=embedVar)

@bot.command()
async def NuevaT(ctx,*args):
    if len(args)!= 3:
        await ctx.send('El formato es invalido debe ser algo del estilo: Matemáticas "Ejercicios pagina 2" 22/09/2021')
        return
    try:
        endtime = datetime.datetime.strptime(args[2], '%d/%m/%Y')
    except ValueError:
        await ctx.send('El formato de fecha es invalido el formato correcto es: 22/09/2021 DD/MM/YYYY')
        return
    cat = args[0]
    #if not cat in categorias:
    #    await ctx.send('La categoria {} no coincide con las de la lista {}'.format(cat, ', '.join(categorias)))
    #    return
    name = args[1]
    id = str(ctx.guild.id)
    tareas = id + '_tareas'
    query_tar= """INSERT INTO {} (name, enddate,cat)
    VALUES
    ('{}','{}','{}');
    """.format(tareas,name,endtime,cat)
    await ctx.send('@{} la tarea {} debera ser entregada el dia {}'.format(cat, name, endtime)      )
    try:
        connection = mysql.connector.connect(host=os.getenv('HOST'),
                                            database=os.getenv('DATABASE'),
                                            user=os.getenv('USER'),
                                            password=os.getenv('PASSWORD'))
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor(buffered=True)
            cursor.execute("select database();")
            cursor.execute(query_tar)
            connection.commit()
            print(cursor.rowcount, "Record inserted successfully into Laptop table")
    except Error as e:
        print("Error while connecting to MYSQL",e)
    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")


@bot.command()
async def NuevoE(ctx,*args):
        if len(args)!= 3:
            await ctx.send('El formato es invalido debe ser algo del estilo: Matemáticas "Tema 2" 22/09/2021')
            return
        try:
            endtime = datetime.datetime.strptime(args[2], '%d/%m/%Y')
        except ValueError:
            await ctx.send('El formato de fecha es invalido el formato correcto es: 22/09/2021 DD/MM/YYYY')
            return
        cat = args[0]
        #if not cat in categorias:
        #    await ctx.send('La categoria {} no coincide con las de la lista {}'.format(cat, ', '.join(categorias)))
        #    return
        name = args[1]
        id = str(ctx.guild.id)
        exa = id + '_examenes'
        query_tar= """INSERT INTO {} (name, enddate,cat)
        VALUES
        ('{}','{}','{}');
        """.format(exa,name,endtime,cat)
        await ctx.send('@{} El examen de {} es el dia {}'.format(cat, name, endtime)      )
        try:
        connection = mysql.connector.connect(host=os.getenv('HOST'),
                                            database=os.getenv('DATABASE'),
                                            user=os.getenv('USER'),
                                            password=os.getenv('PASSWORD'))
            if connection.is_connected():
                db_Info = connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                cursor = connection.cursor(buffered=True)
                cursor.execute("select database();")
                cursor.execute(query_tar)
                connection.commit()
                print(cursor.rowcount, "Record inserted successfully into Laptop table")
        except Error as e:
            print("Error while connecting to MYSQL",e)
        finally:
            if connection.is_connected():
                connection.close()
                print("MySQL connection is closed")



@bot.command()
async def Ayuda(ctx):
    #embed = discord.Embed(title='Hola bienvenido a la ayuda de agenbot \n -Esta es la lista de comandos que puedes utilizar, si quieres añadir alguno a la lista dile a mi creador: Rick S.#4895',
     #                     description="```",
      #                    colour=0x00FFFF)
    #ctx.send(embed=embed)
    embedVar = discord.Embed(title="Hola bienvenido a la ayuda de agenbot", description="-Esta es la lista de comandos que puedes utilizar, si quieres añadir alguno a la lista dile a mi creador: Rick S.#4895", color=0x00ffff)
    embedVar.add_field(name='$NuevaT', value='-Comando $NuevaT sirve para agregar una nueva tarea por ejemplo Matemáticas "Ejercicios pagina 2" 22/09/2021', inline=False)
    embedVar.add_field(name='$NuevoE', value='-Comando $NuevoE sirve para agregar un nuevo examen por ejemplo Matemáticas "Tema 2" 22/09/2021', inline=False)
    embedVar.add_field(name="$Examenes", value="-Comando $Examenes sirve para mostrar todos los examenes que aun no se hayan realizado", inline=False)
    embedVar.add_field(name="$Tareas", value="-Comando $Tareas sirve para mostrar todas las tareas que aun no se hayan realizado", inline=False)
    embedVar.add_field(name="$TareasDia", value="-Comando $TareasDia <DD/MM/YYYY> Sirve para mostrar todas las tareas de un día en especifico ejemplo: $TareasDia 23/09/2021", inline=False)
    embedVar.add_field(name="$TareasMes", value="-Comando $TareasMes <MM> Sirve para mostrar todas las tareas de un mes en especifico ejemplo: $TareasMes 09 ", inline=False)
    embedVar.add_field(name="$ExamenMes", value="-Comando $ExamenMes <MM> muestra todos los examenes de un mes en especifico ejemplo: $ExamenMes 09", inline=False)
    embedVar.colour = 0x00FFFF
    await ctx.send(embed=embedVar)

#Comando $Tareas muestra todas las tareas aun no entregadas
#Comando $Examenes muestra los examenes futuros
#Comando $TareaDia DD/MM/YYYYY muestra las tareas que se debian entregar este dia.
#Comando $TareaMes MM muestra las tareas que se debian entregar ese mes.
#Comando $ExamenMes MM muestra los examenes que se debian realizar ese mes.
#SELECT * FROM Project WHERE MONTH(DueDate) = 1 AND YEAR(DueDate) = 2010

@bot.command()
async def RDRSS0IwWVJJQ0tTQU5DSEVa(ctx):
    id = str(ctx.guild.id)
    tareas = id + '_tareas'
    examenes = id + '_examenes'
    query_exam= """CREATE TABLE IF NOT EXISTS `{}` (
    `ID` int(11) NOT NULL AUTO_INCREMENT,
    `name` text COLLATE utf8mb4_unicode_ci NOT NULL,
    `enddate` datetime NOT NULL,
    `cat` char(50) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
    PRIMARY KEY (`ID`)
    ); """.format(examenes)
    query_tar= """CREATE TABLE IF NOT EXISTS `{}` (
    `ID` int(11) NOT NULL AUTO_INCREMENT,
    `name` text COLLATE utf8mb4_unicode_ci NOT NULL,
    `enddate` datetime NOT NULL,
    `cat` char(50) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
    PRIMARY KEY (`ID`)
    ); """.format(tareas)
    try:
        connection = mysql.connector.connect(host='141.136.41.101',
                                                database='u371264032_shadow_script',
                                                user='u371264032_shadow_script',
                                                password='jz:KU=N2')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor(buffered=True)
            cursor.execute("select database();")
            cursor.execute(query_exam)
            connection.commit()
            print(cursor.rowcount, "Record inserted successfully into Laptop table")
            cursor.execute(query_tar)
            connection.commit()
            print(cursor.rowcount, "Record inserted successfully into Laptop table")
    except Error as e:
        print("Error while connecting to MYSQL",e)
    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")


@bot.event
async def on_guild_join(guild):
    general = await guild.create_text_channel("💼Agenda")
    await general.send("Hola @everyone, soy tu bot personal recordante que existo y mira mi cara de felicidad, es gracias a que voy a estar todo el año dandote por culo como la buena agenda que soy.")
bot.run(TOKEN)