import sqlite3
from datetime import datetime


class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect('work_finder.db', check_same_thread=False)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT UNIQUE NOT NULL,
                            password TEXT NOT NULL,
                            email TEXT,
                            phone TEXT,
                            experience TEXT,
                            user_type TEXT DEFAULT 'job_seeker',
                            created_at TIMESTAMP
                            DEFAULT CURRENT_TIMESTAMP)''')
        try:
            self.cursor.execute("ALTER TABLE users ADD COLUMN user_type TEXT DEFAULT 'job_seeker'")
            self.conn.commit()
        except sqlite3.OperationalError:
            pass

        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS vacancies
                            ( id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, description TEXT, salary TEXT, company TEXT, category TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                            )
                            ''')

        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS responses
                            ( id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, vacancy_id INTEGER, status TEXT DEFAULT 'pending', created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY
                            (
                                user_id
                            ) REFERENCES users
                            (
                                id
                            ),
                                FOREIGN KEY
                            (
                                vacancy_id
                            ) REFERENCES vacancies
                            (
                                id
                            )
                                )
                                
        
                            ''')

        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS notifications
                            ( id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, message TEXT NOT NULL, is_read BOOLEAN DEFAULT 0, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY
                            (
                                user_id
                            ) REFERENCES users
                            (
                                id
                            )
                                )
                            ''')
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS chats
                            ( id INTEGER PRIMARY KEY AUTOINCREMENT, employer_id INTEGER, job_seeker_id INTEGER, vacancy_id INTEGER, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY
                            (
                                employer_id
                            ) REFERENCES users
                            (
                                id
                            ),
                                FOREIGN KEY
                            (
                                job_seeker_id
                            ) REFERENCES users
                            (
                                id
                            ),
                                FOREIGN KEY
                            (
                                vacancy_id
                            ) REFERENCES vacancies
                            (
                                id
                            ),
                                UNIQUE
                            (
                                employer_id,
                                job_seeker_id,
                                vacancy_id
                            )
                                )
                            ''')

        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS messages
                            ( id INTEGER PRIMARY KEY AUTOINCREMENT, chat_id INTEGER, sender_id INTEGER, message_text TEXT NOT NULL, is_read BOOLEAN DEFAULT 0, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY
                            (
                                chat_id
                            ) REFERENCES chats
                            (
                                id
                            ),
                                FOREIGN KEY
                            (
                                sender_id
                            ) REFERENCES users
                            (
                                id
                            )
                                )
                            ''')

        self.conn.commit()

    def insert_sample_data(self):
        sample_vacancies = [
            ('Разработчик Python', 'Разработка backend на Django/Flask', '80000 руб.', 'IT Company', 'IT'),
            ('Официант', 'Работа в кафе вечером', '50000 руб.', 'Coffee Shop', 'Обслуживание'),
            ('Курьер', 'Доставка еды по городу', '45000 руб.', 'Delivery Service', 'Логистика'),
            ('Менеджер по продажам', 'Продажа услуг по телефону', '60000 руб.', 'Sales Company', 'Продажи'),
            ('Репетитор математики', 'Занятия со школьниками', '70000 руб.', 'Education Center', 'Образование')
        ]

        self.cursor.executemany('''
                                INSERT
                                OR IGNORE INTO vacancies (title, description, salary, company, category)
            VALUES (?, ?, ?, ?, ?)
                                ''', sample_vacancies)

        self.conn.commit()

    def register_user(self, username, password, email, user_type='job_seeker'):
        try:
            self.cursor.execute('''
                                INSERT INTO users (username, password, email, user_type)
                                VALUES (?, ?, ?, ?)
                                ''', (username, password, email, user_type))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def login_user(self, username, password):
        self.cursor.execute('''
                            SELECT *
                            FROM users
                            WHERE username = ?
                              AND password = ?
                            ''', (username, password))
        return self.cursor.fetchone()

    def get_user_type(self, user_id):
        self.cursor.execute('SELECT user_type FROM users WHERE id = ?', (user_id,))
        result = self.cursor.fetchone()
        return result[0] if result else 'job_seeker'

    def get_user_data(self, user_id):
        self.cursor.execute('''
                            SELECT username, email, phone, experience
                            FROM users
                            WHERE id = ?
                            ''', (user_id,))
        return self.cursor.fetchone()

    def get_all_vacancies(self):
        print("=== ОТЛАДКА: Получение всех вакансий ===")
        self.cursor.execute('SELECT * FROM vacancies ORDER BY created_at DESC')
        vacancies = self.cursor.fetchall()
        print(f"Найдено вакансий: {len(vacancies)}")
        for v in vacancies:
            print(f"Вакансия: {v[1]} - {v[4]}")
        return vacancies

    def search_vacancies(self, query, category):
        print(f"=== ОТЛАДКА ПОИСКА: query='{query}', category='{category}' ===")

        if category == 'Все' or category == 'Все категории':
            self.cursor.execute('''
                                SELECT *
                                FROM vacancies
                                WHERE title LIKE ?
                                   OR description LIKE ?
                                   OR company LIKE ?
                                ORDER BY created_at DESC
                                ''', (f'%{query}%', f'%{query}%', f'%{query}%'))
        else:
            self.cursor.execute('''
                                SELECT *
                                FROM vacancies
                                WHERE (title LIKE ? OR description LIKE ? OR company LIKE ?)
                                  AND category = ?
                                ORDER BY created_at DESC
                                ''', (f'%{query}%', f'%{query}%', f'%{query}%', category))

        results = self.cursor.fetchall()
        print(f"Найдено вакансий: {len(results)}")
        return results

    def add_vacancy(self, title, description, salary, company, category):
        self.cursor.execute('''
                            INSERT INTO vacancies (title, description, salary, company, category)
                            VALUES (?, ?, ?, ?, ?)
                            ''', (title, description, salary, company, category))
        self.conn.commit()
        return self.cursor.lastrowid

    def add_response(self, user_id, vacancy_id):
        print(f"=== ДОБАВЛЕНИЕ ОТКЛИКА: user_id={user_id}, vacancy_id={vacancy_id} ===")

        self.cursor.execute('''
                            SELECT id, status
                            FROM responses
                            WHERE user_id = ?
                              AND vacancy_id = ?
                            ''', (user_id, vacancy_id))

        existing_response = self.cursor.fetchone()

        if existing_response:
            response_id, status = existing_response
            print(f"Уже откликался! response_id={response_id}, status={status}")
            return False
        else:
            self.cursor.execute('''
                                INSERT INTO responses (user_id, vacancy_id, status)
                                VALUES (?, ?, 'pending')
                                ''', (user_id, vacancy_id))
            self.conn.commit()
            new_id = self.cursor.lastrowid
            print(f"Успешно добавлен отклик! ID: {new_id}")
            return True

    def get_user_responses(self, user_id):
        self.cursor.execute('''
                            SELECT v.title, v.company, r.status, r.created_at
                            FROM responses r
                                     JOIN vacancies v ON r.vacancy_id = v.id
                            WHERE r.user_id = ?
                            ''', (user_id,))
        return self.cursor.fetchall()

    def update_profile(self, user_id, email, phone, experience):
        self.cursor.execute('''
                            UPDATE users
                            SET email      = ?,
                                phone      = ?,
                                experience = ?
                            WHERE id = ?
                            ''', (email, phone, experience, user_id))
        self.conn.commit()

    def get_employer_responses(self, employer_id):
        self.cursor.execute('SELECT experience FROM users WHERE id = ?', (employer_id,))
        employer_data = self.cursor.fetchone()

        if not employer_data or not employer_data[0]:
            return []

        company_name = employer_data[0]

        self.cursor.execute('''
                            SELECT r.id, v.title, u.username, r.status, r.created_at
                            FROM responses r
                                     JOIN vacancies v ON r.vacancy_id = v.id
                                     JOIN users u ON r.user_id = u.id
                            WHERE v.company = ?
                            ORDER BY r.created_at DESC
                            ''', (company_name,))
        return self.cursor.fetchall()

    def update_response_status(self, response_id, status):
        self.cursor.execute('''
                            UPDATE responses
                            SET status = ?
                            WHERE id = ?
                            ''', (status, response_id))
        self.conn.commit()

    def debug_employer_data(self, employer_id):
        print(f"=== ОТЛАДКА РАБОТОДАТЕЛЯ ID: {employer_id} ===")

        self.cursor.execute('SELECT username, experience FROM users WHERE id = ?', (employer_id,))
        employer = self.cursor.fetchone()
        print(f"Работодатель: {employer}")

        if employer:
            company_name = employer[1]
            print(f"Название организации: '{company_name}'")

            self.cursor.execute('SELECT id, title FROM vacancies WHERE company = ?', (company_name,))
            vacancies = self.cursor.fetchall()
            print(f"Вакансии компании: {vacancies}")

            if vacancies:
                vacancy_ids = [v[0] for v in vacancies]
                print(f"ID вакансий: {vacancy_ids}")

                self.cursor.execute('''
                                    SELECT r.id, v.title, u.username
                                    FROM responses r
                                             JOIN vacancies v ON r.vacancy_id = v.id
                                             JOIN users u ON r.user_id = u.id
                                    WHERE v.company = ?
                                    ''', (company_name,))
                responses = self.cursor.fetchall()
                print(f"Отклики: {responses}")

        print("=== КОНЕЦ ОТЛАДКИ ===")

    def create_test_responses(self):
        self.cursor.execute('SELECT id, experience FROM users WHERE user_type = "employer" LIMIT 1')
        employer = self.cursor.fetchone()

        if employer:
            employer_id, company_name = employer
            print(f"Тестовый работодатель: {employer_id}, компания: {company_name}")

            self.cursor.execute('SELECT id FROM vacancies WHERE company = ? LIMIT 1', (company_name,))
            vacancy = self.cursor.fetchone()

            if vacancy:
                vacancy_id = vacancy[0]
                self.cursor.execute('SELECT id FROM users WHERE user_type = "job_seeker" LIMIT 1')
                job_seeker = self.cursor.fetchone()

                if job_seeker:
                    job_seeker_id = job_seeker[0]
                    self.cursor.execute('''
                                        INSERT
                                        OR IGNORE INTO responses (user_id, vacancy_id, status)
                        VALUES (?, ?, 'pending')
                                        ''', (job_seeker_id, vacancy_id))
                    self.conn.commit()
                    print("Создан тестовый отклик!")

    def get_all_vacancies_simple(self):
        self.cursor.execute('SELECT * FROM vacancies')
        return self.cursor.fetchall()

    def add_notification(self, user_id, message):
        self.cursor.execute('''
                            INSERT INTO notifications (user_id, message)
                            VALUES (?, ?)
                            ''', (user_id, message))
        self.conn.commit()

    def get_user_notifications(self, user_id):
        self.cursor.execute('''
                            SELECT message, created_at, is_read
                            FROM notifications
                            WHERE user_id = ?
                            ORDER BY created_at DESC
                            ''', (user_id,))
        return self.cursor.fetchall()

    def mark_notification_read(self, notification_id):
        self.cursor.execute('''
                            UPDATE notifications
                            SET is_read = 1
                            WHERE id = ?
                            ''', (notification_id,))
        self.conn.commit()

    def update_response_status(self, response_id, status, employer_username, vacancy_title):
        self.cursor.execute('''
                            SELECT r.user_id, u.username, v.title, r.vacancy_id
                            FROM responses r
                                     JOIN users u ON r.user_id = u.id
                                     JOIN vacancies v ON r.vacancy_id = v.id
                            WHERE r.id = ?
                            ''', (response_id,))
        response_data = self.cursor.fetchone()

        if not response_data:
            return False

        job_seeker_id, job_seeker_username, actual_vacancy_title, vacancy_id = response_data

        self.cursor.execute('''
                            UPDATE responses
                            SET status = ?
                            WHERE id = ?
                            ''', (status, response_id))

        if status == 'accepted':
            self.cursor.execute('SELECT id FROM users WHERE username = ?', (employer_username,))
            employer_data = self.cursor.fetchone()
            if employer_data:
                employer_id = employer_data[0]
                chat_id = self.create_chat(employer_id, job_seeker_id, vacancy_id)
                if chat_id:
                    welcome_message = f"Здравствуйте! Ваш отклик на вакансию '{actual_vacancy_title}' принят. Давайте обсудим детали!"
                    self.add_message(chat_id, employer_id, welcome_message)

        if status == 'accepted':
            message = f" Поздравляем! Ваш отклик на вакансию '{actual_vacancy_title}' принят работодателем {employer_username}. Ожидайте联系 для собеседования!"
        else:  # rejected
            message = f" К сожалению, ваш отклик на вакансию '{actual_vacancy_title}' отклонен работодателем {employer_username}. Не расстраивайтесь, продолжайте поиск!"

        self.cursor.execute('''
                            INSERT INTO notifications (user_id, message)
                            VALUES (?, ?)
                            ''', (job_seeker_id, message))

        self.conn.commit()
        return True

    def has_user_responded(self, user_id, vacancy_id):
        print(f"=== ОТЛАДКА: проверка отклика user_id={user_id}, vacancy_id={vacancy_id} ===")

        self.cursor.execute('''
                            SELECT id
                            FROM responses
                            WHERE user_id = ?
                              AND vacancy_id = ?
                            ''', (user_id, vacancy_id))

        result = self.cursor.fetchone()
        print(f"Результат проверки: {result}")
        print(f"Пользователь откликался: {result is not None}")
        print("=== КОНЕЦ ОТЛАДКИ ===")

        return result is not None

    def debug_all_responses(self):
        print("=== ВСЕ ОТКЛИКИ В БАЗЕ ===")
        self.cursor.execute('SELECT user_id, vacancy_id FROM responses')
        all_responses = self.cursor.fetchall()
        for response in all_responses:
            print(f"user_id: {response[0]}, vacancy_id: {response[1]}")
        print(f"Всего откликов: {len(all_responses)}")
        print("=== КОНЕЦ ===")

    def cleanup_duplicate_responses(self):
        print("=== ОЧИСТКА ДУБЛИКАТОВ ОТКЛИКОВ ===")

        self.cursor.execute('''
                            SELECT user_id, vacancy_id, COUNT(*) as count
                            FROM responses
                            GROUP BY user_id, vacancy_id
                            HAVING COUNT (*) > 1
                            ''')
        duplicates = self.cursor.fetchall()
        print(f"Найдено дубликатов: {len(duplicates)}")

        for dup in duplicates:
            user_id, vacancy_id, count = dup
            print(f"Дубликаты: user_id={user_id}, vacancy_id={vacancy_id}, count={count}")

            self.cursor.execute('''
                                DELETE
                                FROM responses
                                WHERE user_id = ?
                                  AND vacancy_id = ?
                                  AND id NOT IN (SELECT MIN(id)
                                                 FROM responses
                                                 WHERE user_id = ?
                                                   AND vacancy_id = ?)
                                ''', (user_id, vacancy_id, user_id, vacancy_id))

        self.conn.commit()
        print("Очистка завершена")

    def create_chat(self, employer_id, job_seeker_id, vacancy_id):
        try:
            self.cursor.execute('''
                                INSERT
                                OR IGNORE INTO chats (employer_id, job_seeker_id, vacancy_id)
                VALUES (?, ?, ?)
                                ''', (employer_id, job_seeker_id, vacancy_id))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            return None

    def add_message(self, chat_id, sender_id, message_text):
        self.cursor.execute('''
                            INSERT INTO messages (chat_id, sender_id, message_text)
                            VALUES (?, ?, ?)
                            ''', (chat_id, sender_id, message_text))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_user_chats(self, user_id):
        self.cursor.execute('''
                            SELECT c.id,
                                   CASE
                                       WHEN c.employer_id = ? THEN u2.username
                                       ELSE u1.username
                                       END as                partner_name,
                                   v.title as                vacancy_title,
                                   (SELECT message_text
                                    FROM messages
                                    WHERE chat_id = c.id
                                    ORDER BY created_at DESC LIMIT 1) as last_message,
                   (SELECT created_at FROM messages WHERE chat_id = c.id ORDER BY created_at DESC LIMIT 1) as last_message_time
                            FROM chats c
                                JOIN users u1
                            ON c.employer_id = u1.id
                                JOIN users u2 ON c.job_seeker_id = u2.id
                                JOIN vacancies v ON c.vacancy_id = v.id
                            WHERE c.employer_id = ? OR c.job_seeker_id = ?
                            ORDER BY last_message_time DESC
                            ''', (user_id, user_id, user_id))
        return self.cursor.fetchall()

    def get_chat_messages(self, chat_id):
        self.cursor.execute('''
                            SELECT m.id, m.sender_id, u.username, m.message_text, m.created_at
                            FROM messages m
                                     JOIN users u ON m.sender_id = u.id
                            WHERE m.chat_id = ?
                            ORDER BY m.created_at ASC
                            ''', (chat_id,))
        return self.cursor.fetchall()

    def get_chat_info(self, chat_id):
        self.cursor.execute('''
                            SELECT c.employer_id,
                                   c.job_seeker_id,
                                   v.title,
                                   u1.username as employer_name,
                                   u2.username as job_seeker_name
                            FROM chats c
                                     JOIN vacancies v ON c.vacancy_id = v.id
                                     JOIN users u1 ON c.employer_id = u1.id
                                     JOIN users u2 ON c.job_seeker_id = u2.id
                            WHERE c.id = ?
                            ''', (chat_id,))
        return self.cursor.fetchone()


