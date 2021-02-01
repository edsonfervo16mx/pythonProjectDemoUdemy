import sys
from collections import OrderedDict
import datetime
from peewee import *
import os

db = SqliteDatabase('diary.db')

class Entry(Model):
    content = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)
    class Meta:
        database = db

def add_entry():
    """Crear"""
    print("Introduce tu registro. Preciona Ctrl + D cuando termines")
    data = sys.stdin.read().strip()
    if data:
        if input("Guardar entrada? [Y/n]").lower() != 'n':
            Entry.create(content=data)
            print("Se han guardado los datos.")

def view_entries(search_query=None):
    """Consultar"""
    entries = Entry.select().order_by(Entry.timestamp.desc())

    if search_query:
        entries = entries.where(Entry.content.contains(search_query))

    for entry in entries:
        timestamp = entry.timestamp.strftime('%A %B %d, %Y %I:%M%p')
        clear()
        print(timestamp)
        print('*'*len(timestamp))
        print(entry.content)
        print("\n\n"+"*"*len(timestamp))
        print('n| siguiente entrada')
        print('d| borrar entrada')
        print('q| salir al menu')

        next_action = input('Accion a realizar: [Nq]').lower().strip()

        if next_action == 'q':
            break
        elif next_action == 'd':
            delete_entry(entry)

def search_entries():
    """Buscar"""
    view_entries(input('Texto a buscar: '))

def delete_entry(entry):
    """Eliminar"""
    response = input("Estas seguro? [y/N]").lower()
    if response == 'y':
        entry.delete_instance()
        print("Entrada borrada")

menu = OrderedDict([
    ('a',add_entry),
    ('b',view_entries),
    ('s',search_entries),
    ('c',delete_entry)
])

def menu_loop():
    """Menu"""
    choise = None
    while choise != 'q':
        clear()
        print("Presiona 'q' para salir")
        for key, value in menu.items():
            print('{} | {}'.format(key,value.__doc__))
        choise = input('Eleccion: ').lower().strip()

        if choise in menu:
            clear()
            menu[choise]()

def initialize():
    db.connect()
    db.create_tables([Entry],safe=True)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == '__main__':
    initialize()
    menu_loop()