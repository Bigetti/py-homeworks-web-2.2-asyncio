#main.py

import sqlite3
import db, api
import asyncio
import json
import aiohttp
import aiosqlite

from api import fetch_character, fetch_all_characters



# Функция для получения названий из URL
async def get_names_from_urls(session, urls):
    names = []
    for url in urls:
        async with session.get(url) as resp:
            data = await resp.json()
            names.append(data['title'])
    return names

 



# Функция для проверки существования персонажа в базе данных
async def character_exists(conn, name):
    async with conn.execute('SELECT 1 FROM characters WHERE name=?', (name,)) as cursor:
        return await cursor.fetchone() is not None



# Функция для вставки персонажа в базу данных
async def insert_character(conn, character):
    try:
        # Проверяем, существует ли персонаж в базе данных
        if not await character_exists(conn, character['name']):
            # Получаем список фильмов персонажа, если они есть
            film_urls = character.get('films', [])
            # Получаем список видов персонажа, если они есть
            species_urls = character.get('species', [])
            # Получаем список кораблей персонажа, если они есть
            starship_urls = character.get('starships', [])
            # Получаем список транспорта персонажа, если они есть
            vehicle_urls = character.get('vehicles', [])

            # Получаем названия фильмов, видов, кораблей и транспорта
            async with aiohttp.ClientSession() as session:
                film_names = await get_names_from_urls(session, film_urls)
                species_names = await get_names_from_urls(session, species_urls)
                starship_names = await get_names_from_urls(session, starship_urls)
                vehicle_names = await get_names_from_urls(session, vehicle_urls)

            # Обновляем персонажей с названиями фильмов, видов, кораблей и транспорта
            character['films'] = ', '.join(film_names)
            character['species'] = ', '.join(species_names)
            character['starships'] = ', '.join(starship_names)
            character['vehicles'] = ', '.join(vehicle_names)

            # Вставляем персонажа в базу данных
            await conn.execute('''
                INSERT INTO characters (birth_year, eye_color, films, gender, hair_color, height, homeworld, mass, name, skin_color, species, starships, vehicles, created, edited, url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (character.get('birth_year'), character.get('eye_color'), character.get('films'), character.get('gender'), character.get('hair_color'), character.get('height'), character.get('homeworld'), character.get('mass'), character.get('name'), character.get('skin_color'), character.get('species'), character.get('starships'), character.get('vehicles'), character.get('created'), character.get('edited'), character.get('url')))
            await conn.commit()  # Не забываем коммитить изменения
            print(f"Персонаж {character['name']} успешно добавлен в базу данных.")
        else:
            print(f"Персонаж {character['name']} уже существует в базе данных.")
    except sqlite3.Error as e:
        print(f"Произошла ошибка при получении или вставке данных для персонажа {character['name']}: {e}")
        # Продолжаем работу, не прерывая ее

# Пример использования функции insert_character в цикле
async def process_characters(characters):
    async with aiosqlite.connect('starwars.db') as conn:
        for character in characters:
            try:
                await insert_character(conn, character)
            except Exception as e:
                print(f"Произошла ошибка при обработке персонажа {character['name']}: {e}")
                # Продолжаем работу, не прерывая ее

                


        # Продолжаем работу, не прерывая ее

# Пример использования функции insert_character в цикле
async def process_characters(characters):
    async with aiosqlite.connect('starwars.db') as conn:
        for character in characters:
            try:
                await insert_character(conn, character)
            except Exception as e:
                print(f"Произошла ошибка при обработке персонажа {character['name']}: {e}")
                # Продолжаем работу, не прерывая ее






# Главная асинхронная функция, которая управляет выполнением всего кода
async def main():

    characters = await fetch_all_characters()  # Этот вызов является асинхронным, если fetch_all_characters() также асинхронная функция

    # Распечатать список персонажей для проверки на дубликаты
    print(characters)



    db.create_db()  # Этот вызов синхронной функции, потому что create_db() не асинхронная
    print("База данных успешно создана.")

    # Вставляем персонажей в базу данных
    # Этот блок кода также выполняется асинхронно, потому что он использует aiosqlite для асинхронного взаимодействия с базой данных
    async with aiosqlite.connect('starwars.db') as conn:
        try:
            for character in characters:
                await insert_character(conn, character)
        except Exception as e:
            print(f"Произошла ошибка при получении или вставке данных: {e}")
    print("Соединение с базой данных закрыто.")

# Точка входа в программу, которая запускает асинхронный цикл событий
if __name__ == '__main__':
    asyncio.run(main())