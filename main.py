import sqlite3
import db, api
import asyncio



def insert_character(conn, character):
    cursor = conn.cursor()

    cursor.execute('''
                   INSERT INTO characters (id, birth_year, eye_color, films, gender, hair_color, height, homeworld, mass, name, skin_color, species, starships, vehicles)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (character['id'], character['birth_year'], character['eye_color'], ', '.join(character['films']), character['gender'], character['hair_color'], character['height'], character['homeworld'], character['mass'], character['name'], character['skin_color'], ', '.join(character['species']), ', '.join(character['starships']), ', '.join(character['vehicles'])))

    conn.commit()


async def main():
    db.create_db()
    conn = sqlite3.connect('starwars.db')


    characters = await api.fetch_all_characters()
    
    for character in characters:
        if 'id' in character:  # Проверяем наличие ключа 'id'
            insert_character(conn, character)
        else:
            print(f"Пропуск персонажа без идентификатора: {character}")

    conn.close()


if __name__ == '__main__':
    asyncio.run(main())