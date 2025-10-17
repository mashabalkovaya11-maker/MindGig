from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.spinner import Spinner
from app_logic import current_user
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.uix.widget import Widget

Builder.load_string('''
<LoginScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 50
        spacing: 20

        Label:
            text: 'Вход в MindGig'
            font_size: 24
            size_hint_y: 0.2
            color: 0,0.5,1,1

        TextInput:
            id: username_input
            hint_text: 'Логин'
            size_hint_y: 0.1
            font_size: 18

        TextInput:
            id: password_input
            hint_text: 'Пароль'
            password: True
            size_hint_y: 0.1
            font_size: 18

        Button:
            text: 'Войти'
            font_size: 18
            size_hint_y: 0.1
            background_color: 0.2, 0.6, 0.8, 1
            on_release: root.login()

        Button:
            text: 'Регистрация'
            font_size: 18
            size_hint_y: 0.1
            background_color: 0.3, 0.7, 0.3, 1
            on_release: root.manager.current = 'register'


<RegisterScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 50
        spacing: 15

        Label:
            text: 'Регистрация'
            font_size: 24
            size_hint_y: 0.15
            color: 0,0.5,1,1

        TextInput:
            id: reg_username
            hint_text: 'Логин'
            size_hint_y: 0.1
            font_size: 18

        TextInput:
            id: reg_password
            hint_text: 'Пароль'
            password: True
            size_hint_y: 0.1
            font_size: 18

        TextInput:
            id: reg_email
            hint_text: 'Email (не обязательно для заполнения)'
            size_hint_y: 0.1
            font_size: 18
            
        Label:
            text: 'Тип аккаунта:'
            font_size: 16
            size_hint_y: 0.05
            color: 0,0,0,1
            bold: True
            
        Spinner:
            id: user_type_spinner
            text: 'Выберите тип аккаунта'
            values: ['Я соискатель (ищу работу)', 'Я работодатель']
            size_hint_y: 0.1
            font_size: 18
            background_color: 0.9, 0.9, 0.5, 1

        Button:
            text: 'Зарегистрироваться'
            font_size: 18
            size_hint_y: 0.1
            background_color: 0.3, 0.7, 0.3, 1
            on_release: root.register()

        Button:
            text: 'Назад'
            font_size: 18
            size_hint_y: 0.1
            background_color: 0.8, 0.2, 0.2, 1
            on_release: root.manager.current = 'login'

<MainScreen>:
    orientation: 'vertical'
    Label:
        text: "Добро пожаловать в MindGig"
        pos_hint: {'center_x': 0.5, 'center_y': 0.9}
        font_size: 24
        size_hint_y: 0.2
        color: 0,0.5,1,1
        bold: True

    Button:
        id: all_vacancies_btn
        size_hint: (0.3, 0.12)
        pos_hint: {'center_x': 0.2, 'center_y': 0.7}
        text: 'Все вакансии'
        font_size: 16
        background_color: (0.2, 0.6, 0.8, 1)
        on_release: 
            root.manager.current = 'all_vacancies'

    Button:
        id: search_btn
        text: 'Поиск работы'
        font_size: 16
        size_hint: (0.3, 0.12)
        pos_hint: {'center_x': 0.2, 'center_y': 0.55}
        background_color: 0.3, 0.7, 0.3, 1
        on_release: root.manager.current = 'search'

    Button:
        id: my_responses_btn
        text: 'Мои отклики'
        font_size: 16
        size_hint: (0.3, 0.12)
        pos_hint: {'center_x': 0.2, 'center_y': 0.4}
        background_color: 0.9, 0.6, 0.2, 1
        on_release: 
            root.load_responses()
            root.manager.current = 'my_responses'

    Button:
        id: add_vacancy_btn
        text: 'Разместить вакансию'
        font_size: 16
        size_hint: (0.3, 0.12)
        pos_hint: {'center_x': 0.2, 'center_y': 0.25}
        background_color: 0.8, 0.5, 0.2, 1
        on_release: root.manager.current = 'add_vacancy'

    Button:
        id: employer_responses_btn
        text: 'Отклики на мои вакансии'
        font_size: 14
        size_hint: (0.3, 0.12)
        pos_hint: {'center_x': 0.2, 'center_y': 0.1}
        background_color: 0.7, 0.3, 0.7, 1
        on_release: root.manager.current = 'employer_responses'

    Button:
        text: 'Профиль'
        font_size: 16
        size_hint: (0.3, 0.12)
        pos_hint: {'center_x': 0.8, 'center_y': 0.7}
        background_color: 0.5, 0.3, 0.8, 1
        on_release: root.manager.current = 'profile'

    Button:
        text: 'Выйти'
        font_size: 16
        size_hint: (0.3, 0.12)
        pos_hint: {'center_x': 0.8, 'center_y': 0.55}
        background_color: 0.8, 0.2, 0.2, 1
        on_release: root.logout()

    Button:
        text: 'Уведомления'
        font_size: 16
        size_hint: (0.3, 0.12)
        pos_hint: {'center_x': 0.8, 'center_y': 0.4}
        background_color: 1, 0.8, 0, 1
        on_release: root.manager.current = 'notifications'
        
    Button:
        text: 'Мои чаты'
        font_size: 16
        size_hint: (0.3, 0.12)
        pos_hint: {'center_x': 0.8, 'center_y': 0.25}
        background_color: 0.2, 0.8, 0.8, 1
        on_release: root.manager.current = 'chat_list'
        
<AllVacanciesScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 10
        
        Label:
            text: 'Все вакансии'
            font_size: 24
            size_hint_y: 0.1
            color: 0,0.5,1,1
        
        ScrollView:
            GridLayout:
                id: vacancies_container
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                padding: 10
        
        Button:
            text: 'Назад'
            font_size: 18
            size_hint_y: 0.1
            background_color: 0.8, 0.2, 0.2, 1
            on_release: root.manager.current = 'main'

<SearchScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 10
        
        Label:
            text: 'Поиск работы'
            font_size: 24
            size_hint_y: 0.1
            color: 0,0.5,1,1
        
        TextInput:
            id: search_query
            hint_text: 'Профессия, ключевые слова'
            size_hint_y: 0.1
            font_size: 16
        
        Spinner:
            id: category_spinner
            text: 'Все категории'
            values: ['Все', 'IT', 'Обслуживание', 'Логистика', 'Продажи', 'Образование']
            size_hint_y: 0.1
        
        Button:
            text: 'Найти'
            font_size: 18
            size_hint_y: 0.1
            background_color: 0.3, 0.7, 0.3, 1
            on_release: root.search_vacancies()
        
        ScrollView:
            GridLayout:
                id: search_results
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                padding: 10
        
        Button:
            text: 'Назад'
            font_size: 18
            size_hint_y: 0.1
            background_color: 0.8, 0.2, 0.2, 1
            on_release: root.manager.current = 'main'

<AddVacancyScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 10
        
        Label:
            text: 'Разместить вакансию'
            font_size: 24
            size_hint_y: 0.1
            color: 0,0.5,1,1
        
        TextInput:
            id: vacancy_title
            hint_text: 'Название вакансии'
            size_hint_y: 0.1
        
        TextInput:
            id: vacancy_company
            hint_text: 'Компания'
            size_hint_y: 0.1
        
        TextInput:
            id: vacancy_salary
            hint_text: 'Зарплата'
            size_hint_y: 0.1
        
        Spinner:
            id: vacancy_category
            text: 'Выберите категорию'
            values: ['IT', 'Обслуживание', 'Логистика', 'Продажи', 'Образование']
            size_hint_y: 0.1
        
        TextInput:
            id: vacancy_description
            hint_text: 'Описание вакансии'
            size_hint_y: 0.3
            multiline: True
        
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: 0.1
            
            Button:
                text: 'Опубликовать'
                background_color: 0.3, 0.7, 0.3, 1
                on_release: root.add_vacancy()
            
            Button:
                text: 'Назад'
                background_color: 0.8, 0.2, 0.2, 1
                on_release: root.manager.current = 'main'

<MyResponsesScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 10
        
        Label:
            text: 'Мои отклики'
            font_size: 24
            size_hint_y: 0.1
            color: 0,0.5,1,1
        
        ScrollView:
            GridLayout:
                id: responses_container
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                padding: 10
        
        Button:
            text: 'Назад'
            font_size: 18
            size_hint_y: 0.1
            background_color: 0.8, 0.2, 0.2, 1
            on_release: root.manager.current = 'main'

<ProfileScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 10
        
        Label:
            text: 'Профиль'
            font_size: 24
            size_hint_y: 0.1
            color: 0,0.5,1,1

        TextInput:
            id: profile_email
            hint_text: 'Email'
            size_hint_y: 0.1

        TextInput:
            id: profile_phone
            hint_text: 'Телефон'
            size_hint_y: 0.1

        TextInput:
            id: profile_info
            hint_text: 'Опыт работы/место учебы'
            size_hint_y: 0.3
            multiline: True

        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: 0.1

            Button:
                text: 'Сохранить'
                background_color: 0.3, 0.7, 0.3, 1
                on_release: root.save_profile()
            
            Button:
                text: 'Выйти'  
                background_color: 0.8, 0.2, 0.2, 1
                on_release: root.logout()
                
            Button:
                text: 'Назад'
                background_color: 0.8, 0.2, 0.2, 1
                on_release: root.manager.current = 'main'
                
<EmployerResponsesScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 10
        
        Label:
            text: 'Отклики на мои вакансии'
            font_size: 24
            size_hint_y: 0.1
            color: 0,0.5,1,1
        
        ScrollView:
            GridLayout:
                id: employer_responses_container
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                padding: 10
        
        Button:
            text: 'Назад'
            font_size: 18
            size_hint_y: 0.1
            background_color: 0.8, 0.2, 0.2, 1
            on_release: root.manager.current = 'main'
            
<NotificationsScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 10
        
        Label:
            text: 'Мои уведомления'
            font_size: 24
            size_hint_y: 0.1
            color: 0,0.5,1,1
        
        ScrollView:
            GridLayout:
                id: notifications_container
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                padding: 10
        
        Button:
            text: 'Назад'
            font_size: 18
            size_hint_y: 0.1
            background_color: 0.8, 0.2, 0.2, 1
            on_release: root.manager.current = 'main'
  # Экран списка чатов          
<ChatListScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 10
        
        Label:
            text: 'Мои чаты'
            font_size: 24
            size_hint_y: 0.1
            color: 0,0.5,1,1
        
        ScrollView:
            GridLayout:
                id: chats_container
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                padding: 10
        
        Button:
            text: 'Назад'
            font_size: 18
            size_hint_y: 0.1
            background_color: 0.8, 0.2, 0.2, 1
            on_release: root.manager.current = 'main'

# Экран конкретного чата
<ChatScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 0
        
        # Шапка чата
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: 0.1
            padding: 10
            canvas.before:
                Color:
                    rgba: 0.2, 0.5, 0.8, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
            
            Button:
                text: '← Назад'
                size_hint_x: 0.3
                font_size: 16
                background_color: 0.2, 0.5, 0.8, 1
                background_normal: ''
                on_release: root.manager.current = 'chat_list'
            
            Label:
                id: chat_title
                text: 'Загрузка...'
                font_size: 16
                bold: True
                color: 1, 1, 1, 1
                halign: 'center'
        
        # Область сообщений - БЕЛЫЙ ФОН
        ScrollView:
            id: messages_scroll
            do_scroll_x: False
            do_scroll_y: True
            canvas.before:
                Color:
                    rgba: 1, 1, 1, 1  # БЕЛЫЙ ФОН
                Rectangle:
                    pos: self.pos
                    size: self.size
            
            GridLayout:
                id: messages_container
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                padding: [10, 10]
                spacing: 5
        
        # Панель ввода сообщения
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: 0.12
            padding: [10, 5]
            spacing: 10
            
            TextInput:
                id: message_input
                hint_text: 'Введите сообщение...'
                size_hint_x: 0.75
                font_size: 16
                multiline: False
                on_text_validate: root.send_message()
            
            Button:
                text: 'Отправить'
                size_hint_x: 0.25
                font_size: 14
                background_color: 0.3, 0.7, 0.3, 1
                background_normal: ''
                on_release: root.send_message()
''')




class LoginScreen(Screen):
    def login(self):
        username = self.ids.username_input.text
        password = self.ids.password_input.text

        app = App.get_running_app()
        user = app.db.login_user(username, password)

        if user or (username == 'user123' and password == 'pass123'):
            if user:
                current_user.id = user[0]
                current_user.username = user[1]
                user_data = app.db.get_user_data(user[0])
                if user_data:
                    current_user.email = user_data[1] or ""
                    current_user.phone = user_data[2] or ""
                    current_user.experience = user_data[3] or ""
                    current_user.user_type = app.db.get_user_type(user[0])
            else:
                current_user.id = 1
                current_user.username = 'user123'
                current_user.email = "demo@example.com"
                current_user.phone = ""
                current_user.experience = ""
                current_user.user_type = 'job_seeker'

            current_user.is_logged_in = True
            self.manager.current = 'main'
        else:
            self.ids.username_input.text = ''
            self.ids.password_input.text = ''


class RegisterScreen(Screen):
    def register(self):
        username = self.ids.reg_username.text
        password = self.ids.reg_password.text
        email = self.ids.reg_email.text

        if self.ids.user_type_spinner.text == 'Я работодатель':
            user_type = 'employer'
        elif self.ids.user_type_spinner.text == 'Я соискатель (ищу работу)':
            user_type = 'job_seeker'
        else:
            self.ids.user_type_spinner.background_color = (1, 0.5, 0.5, 1)  # Красный фон
            return

        app = App.get_running_app()
        if app.db.register_user(username, password, email, user_type):
            self.manager.current = 'login'
        else:
            self.ids.reg_username.text = 'Логин занят!'


class MainScreen(Screen):
    def load_vacancies(self):
        app = App.get_running_app()
        vacancies = app.db.get_all_vacancies_simple()  # Используем простой метод

        screen = self.manager.get_screen('all_vacancies')
        self.manager.current = 'all_vacancies'

    def load_responses(self):
        if not current_user.is_logged_in:
            return

        app = App.get_running_app()
        responses = app.db.get_user_responses(current_user.id)
        screen = self.manager.get_screen('my_responses')
        screen.display_responses(responses)
        self.manager.current = 'my_responses'

    def on_enter(self):
        if not current_user.is_logged_in:
            self.manager.current = 'login'
        else:
            self.update_ui_for_user_type()

    def update_ui_for_user_type(self):
        if current_user.user_type == 'job_seeker':
            self.ids.all_vacancies_btn.opacity = 1
            self.ids.all_vacancies_btn.disabled = False
            self.ids.search_btn.opacity = 1
            self.ids.search_btn.disabled = False
            self.ids.my_responses_btn.opacity = 1
            self.ids.my_responses_btn.disabled = False

            self.ids.add_vacancy_btn.opacity = 0
            self.ids.add_vacancy_btn.disabled = True
            self.ids.employer_responses_btn.opacity = 0
            self.ids.employer_responses_btn.disabled = True


        else:
            self.ids.all_vacancies_btn.opacity = 0
            self.ids.all_vacancies_btn.disabled = True
            self.ids.search_btn.opacity = 0
            self.ids.search_btn.disabled = True
            self.ids.my_responses_btn.opacity = 0
            self.ids.my_responses_btn.disabled = True

            self.ids.add_vacancy_btn.opacity = 1
            self.ids.add_vacancy_btn.disabled = False
            self.ids.employer_responses_btn.opacity = 1
            self.ids.employer_responses_btn.disabled = False

    def logout(self):
        current_user.id = None
        current_user.username = None
        current_user.is_logged_in = False
        self.manager.current = 'login'

    def load_employer_responses(self):
        pass


class AllVacanciesScreen(Screen):
    def on_enter(self):
        self.load_vacancies()

    def load_vacancies(self):
        app = App.get_running_app()
        vacancies = app.db.get_all_vacancies()
        self.display_vacancies(vacancies)

    def display_vacancies(self, vacancies):
        container = self.ids.vacancies_container
        container.clear_widgets()

        app = App.get_running_app()

        for vacancy in vacancies:
            box = BoxLayout(orientation='vertical', size_hint_y=None, height=100)
            box.add_widget(Label(
                text=f"{vacancy[1]} - {vacancy[4]}",
                font_size=16,
                bold=True
            ))
            box.add_widget(Label(
                text=f"Зарплата: {vacancy[3]}",
                font_size=14
            ))


            has_responded = app.db.has_user_responded(current_user.id, vacancy[0])


            if has_responded:
                btn = Button(
                    text='Уже откликались!',
                    size_hint_y=None,
                    height=30,
                    background_color=(1, 0, 0, 1),
                    disabled=True
                )
            else:
                btn = Button(
                    text='Откликнуться',
                    size_hint_y=None,
                    height=30,
                    background_color=(0.2, 0.8, 0.2, 1)
                )
                btn.vacancy_id = vacancy[0]
                btn.bind(on_release=self.respond_to_vacancy)

            box.add_widget(btn)
            container.add_widget(box)

    def respond_to_vacancy(self, instance):
        if not current_user.is_logged_in:
            self.manager.current = 'login'
            return

        app = App.get_running_app()
        success = app.db.add_response(current_user.id, instance.vacancy_id)

        if success:
            instance.text = 'Отправлено!'
            instance.background_color = (0.5, 0.5, 0.5, 1)
            instance.disabled = True
            instance.unbind(on_release=self.respond_to_vacancy)
        else:
            instance.text = 'Уже откликались'
            instance.background_color = (1, 0, 0, 1)
            instance.disabled = True


class SearchScreen(Screen):
    def on_enter(self):
        self.ids.search_results.clear_widgets()
        self.ids.search_query.text = ''
        self.ids.category_spinner.text = 'Все категории'

    def search_vacancies(self):
        query = self.ids.search_query.text
        category = self.ids.category_spinner.text

        app = App.get_running_app()
        results = app.db.search_vacancies(query, category)
        self.display_results(results)

    def display_results(self, results):
        container = self.ids.search_results
        container.clear_widgets()

        app = App.get_running_app()

        if not results:
            container.add_widget(Label(text='Ничего не найдено'))
            return

        for vacancy in results:
            box = BoxLayout(orientation='vertical', size_hint_y=None, height=80)
            box.add_widget(Label(
                text=f"{vacancy[1]} - {vacancy[4]}",
                font_size=16
            ))
            box.add_widget(Label(
                text=f"{vacancy[3]} | {vacancy[5]}",
                font_size=12
            ))


            # has_responded = app.db.has_user_responded(current_user.id, vacancy[0])
            has_responded = False

            if has_responded:
                btn = Button(
                    text='Отправлено!',
                    size_hint_y=None,
                    height=30,
                    background_color=(0.5, 0.5, 0.5, 1),
                    disabled=True
                )
            else:
                btn = Button(
                    text='Откликнуться',
                    size_hint_y=None,
                    height=30,
                    background_color=(0.2, 0.8, 0.2, 1)
                )
                btn.vacancy_id = vacancy[0]
                btn.bind(on_release=self.respond_to_vacancy)

            box.add_widget(btn)
            container.add_widget(box)

    def respond_to_vacancy(self, instance):
        if not current_user.is_logged_in:
            self.manager.current = 'login'
            return

        app = App.get_running_app()
        success = app.db.add_response(current_user.id, instance.vacancy_id)

        if success:
            instance.text = 'Отправлено!'
            instance.background_color = (0.5, 0.5, 0.5, 1)
            instance.disabled = True
            instance.unbind(on_release=self.respond_to_vacancy)
        else:
            instance.text = 'Уже откликались'
            instance.background_color = (1, 0, 0, 1)
            instance.disabled = True

class AddVacancyScreen(Screen):
    def add_vacancy(self):
        title = self.ids.vacancy_title.text
        company = self.ids.vacancy_company.text
        salary = self.ids.vacancy_salary.text
        category = self.ids.vacancy_category.text
        description = self.ids.vacancy_description.text

        app = App.get_running_app()
        app.db.add_vacancy(title, description, salary, company, category)

        self.ids.vacancy_title.text = ''
        self.ids.vacancy_company.text = ''
        self.ids.vacancy_salary.text = ''
        self.ids.vacancy_description.text = ''

        self.manager.current = 'main'

class MyResponsesScreen(Screen):
    def display_responses(self, responses):
        container = self.ids.responses_container
        container.clear_widgets()

        if not responses:
            container.add_widget(Label(text='У вас пока нет откликов'))
            return

        for response in responses:
            box = BoxLayout(orientation='vertical', size_hint_y=None, height=60)
            box.add_widget(Label(
                text=f"{response[0]} - {response[1]}",
                font_size=14
            ))
            box.add_widget(Label(
                text=f"Статус: {response[2]}",
                font_size=12
            ))
            container.add_widget(box)

class ProfileScreen(Screen):
    def on_enter(self):
        if current_user.is_logged_in:
            self.ids.profile_email.text = current_user.email or ""
            self.ids.profile_phone.text = current_user.phone or ""

        if current_user.user_type == 'job_seeker':
            self.ids.profile_info.hint_text = 'Опыт работы'
            self.ids.profile_info.text = current_user.experience or ""
        else:
            self.ids.profile_info.hint_text = 'Название организации'
            self.ids.profile_info.text = current_user.experience or ""

    def save_profile(self):
        email = self.ids.profile_email.text
        phone = self.ids.profile_phone.text
        experience = self.ids.profile_info.text

        app = App.get_running_app()
        app.db.update_profile(current_user.id, email, phone, experience)

        current_user.email = email
        current_user.phone = phone
        current_user.experience = experience

        self.manager.current = 'main'

    def logout(self):
        current_user.id = None
        current_user.username = None
        current_user.is_logged_in = False
        self.manager.current = 'login'


class EmployerResponsesScreen(Screen):
    def on_enter(self):
        self.load_employer_responses()

    def load_employer_responses(self):
        container = self.ids.employer_responses_container
        container.clear_widgets()

        app = App.get_running_app()

        responses = app.db.get_employer_responses(current_user.id)
        print(f"Получено откликов: {len(responses)}")

        if not responses:
            app.db.cursor.execute('SELECT experience FROM users WHERE id = ?', (current_user.id,))
            user_data = app.db.cursor.fetchone()
            company_name = user_data[0] if user_data else "не указана"

            app.db.cursor.execute('SELECT COUNT(*) FROM vacancies WHERE company = ?', (company_name,))
            vacancy_count = app.db.cursor.fetchone()[0]

            debug_text = f'''
        Пока нет откликов на ваши вакансии

        Данные для отладки:
        - Ваша организация: "{company_name}"
        - Ваших вакансий: {vacancy_count}
        - ID пользователя: {current_user.id}

        Чтобы появились отклики:
        1. Убедитесь, что в профиле указано название организации
        2. Создайте вакансии (компания должна совпадать с названием организации)
        3. Попросите соискателей откликнуться на ваши вакансии
        '''
            label = Label(
                text=debug_text,
                font_size=14,
                text_size=(400, None),
                halign='center'
            )
            container.add_widget(label)
            return

        if not responses:
            label = Label(
                text='Пока нет откликов на ваши вакансии\n\nУбедитесь, что:\n1. Указано название организации в профиле\n2. Созданы вакансии\n3. Соискатели откликнулись на ваши вакансии',
                font_size=16,
                text_size=(400, None),
                halign='center'
            )
            container.add_widget(label)
            return

        for response in responses:
            response_id, vacancy_title, username, status, created_at = response

            box = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                height=120,
                padding=10,
                spacing=5
            )

            box.add_widget(Label(
                text=f'Вакансия: {vacancy_title}',
                font_size=16,
                bold=True,
                size_hint_y=0.3
            ))

            box.add_widget(Label(
                text=f'Соискатель: {username}',
                font_size=14,
                size_hint_y=0.25
            ))

            status_label = Label(
                text=f'Статус: {status}',
                font_size=14,
                size_hint_y=0.25
            )
            if status == 'pending':
                status_label.color = (1, 0.5, 0, 1)
            elif status == 'accepted':
                status_label.color = (0, 0.8, 0, 1)
            elif status == 'rejected':
                status_label.color = (1, 0, 0, 1)

            box.add_widget(status_label)

            btn_layout = BoxLayout(
                orientation='horizontal',
                size_hint_y=0.2,
                spacing=5
            )

            if status == 'pending':
                accept_btn = Button(
                    text='Принять',
                    size_hint_x=0.5,
                    background_color=(0, 0.7, 0, 1),
                    font_size=12
                )
                accept_btn.response_id = response_id
                accept_btn.vacancy_title = vacancy_title
                accept_btn.bind(on_release=self.accept_response)

                reject_btn = Button(
                    text='Отклонить',
                    size_hint_x=0.5,
                    background_color=(0.8, 0, 0, 1),
                    font_size=12
                )
                reject_btn.response_id = response_id
                reject_btn.vacancy_title = vacancy_title
                reject_btn.bind(on_release=self.reject_response)

                btn_layout.add_widget(accept_btn)
                btn_layout.add_widget(reject_btn)
            else:
                status_text = 'Принято' if status == 'accepted' else 'Отклонено'
                btn_layout.add_widget(Label(
                    text=status_text,
                    font_size=12,
                    color=(0.5, 0.5, 0.5, 1)
                ))

            box.add_widget(btn_layout)
            container.add_widget(box)

    def accept_response(self, instance):
        app = App.get_running_app()
        success = app.db.update_response_status(
            instance.response_id,
            'accepted',
            current_user.username,
            instance.vacancy_title
        )
        if success:
            self.load_employer_responses()

    def reject_response(self, instance):
        app = App.get_running_app()
        success = app.db.update_response_status(
            instance.response_id,
            'rejected',
            current_user.username,
            instance.vacancy_title
        )
        if success:
            self.load_employer_responses()


class NotificationsScreen(Screen):
    def on_enter(self):
        self.load_notifications()

    def load_notifications(self):
        container = self.ids.notifications_container
        container.clear_widgets()

        app = App.get_running_app()
        notifications = app.db.get_user_notifications(current_user.id)

        if not notifications:
            container.add_widget(Label(
                text='У вас пока нет уведомлений',
                font_size=16,
                halign='center'
            ))
            return

        for notification in notifications:
            message, created_at, is_read = notification

            box = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                height=80,
                padding=10
            )

            message_label = Label(
                text=message,
                font_size=14,
                text_size=(380, None),
                halign='left',
                valign='top'
            )

            date_label = Label(
                text=f"{created_at} {'(новое)' if not is_read else ''}",
                font_size=12,
                color=(0.5, 0.5, 0.5, 1)
            )

            box.add_widget(message_label)
            box.add_widget(date_label)
            container.add_widget(box)


class ChatListScreen(Screen):
    def on_enter(self):
        self.load_chats()

    def load_chats(self):
        container = self.ids.chats_container
        container.clear_widgets()

        app = App.get_running_app()
        chats = app.db.get_user_chats(current_user.id)

        if not chats:
            container.add_widget(Label(
                text='У вас пока нет чатов\n\nЧат появится когда работодатель примет ваш отклик',
                font_size=16,
                halign='center',
                text_size=(400, None)
            ))
            return

        for chat in chats:
            chat_id, partner_name, vacancy_title, last_message, last_message_time = chat

            btn = Button(
                text=f'{partner_name}\nВакансия: {vacancy_title}\nПоследнее: {last_message or "Нет сообщений"}',
                size_hint_y=None,
                height=100,
                background_color=(0.9, 0.95, 1, 1),
                background_normal='',
                font_size=12,
                halign='left',
                color=(0, 0, 0, 1)
            )
            btn.chat_id = chat_id
            btn.bind(on_release=self.open_chat)
            container.add_widget(btn)

    def open_chat(self, instance):
        self.manager.get_screen('chat').chat_id = instance.chat_id
        self.manager.current = 'chat'


class ChatScreen(Screen):
    chat_id = None

    def on_enter(self):
        if self.chat_id:
            self.load_chat()

    def load_chat(self):
        app = App.get_running_app()
        chat_info = app.db.get_chat_info(self.chat_id)
        messages = app.db.get_chat_messages(self.chat_id)

        if chat_info:
            employer_id, job_seeker_id, vacancy_title, employer_name, job_seeker_name = chat_info
            if current_user.id == employer_id:
                partner_name = job_seeker_name
                self.ids.chat_title.text = f' Чат с соискателем {partner_name}'
            else:
                partner_name = employer_name
                self.ids.chat_title.text = f' Чат с работодателем {partner_name}'
            self.ids.chat_title.text += f'\nВакансия: {vacancy_title}'

        container = self.ids.messages_container
        container.clear_widgets()

        for message in messages:
            msg_id, sender_id, username, text, timestamp = message

            time_display = self.format_time(timestamp)

            message_layout = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=80,
                padding=[10, 5]
            )

            if sender_id == current_user.id:
                message_layout.add_widget(Label(size_hint_x=0.5))

                content_box = BoxLayout(
                    orientation='vertical',
                    size_hint_x=0.5
                )

                message_text = f"[b]Я[/b] ({time_display}):\n{text}"
                message_label = Label(
                    text=message_text,
                    font_size=14,
                    color=(0, 0.5, 0, 1),
                    text_size=(350, None),
                    halign='right',
                    valign='top',
                    markup=True
                )
                message_label.bind(size=message_label.setter('text_size'))

                content_box.add_widget(message_label)
                message_layout.add_widget(content_box)

            else:
                content_box = BoxLayout(
                    orientation='vertical',
                    size_hint_x=0.5
                )

                message_text = f"[b]{username}[/b] ({time_display}):\n{text}"
                message_label = Label(
                    text=message_text,
                    font_size=14,
                    color=(0, 0, 0, 1),
                    text_size=(350, None),
                    halign='left',
                    valign='top',
                    markup=True
                )
                message_label.bind(size=message_label.setter('text_size'))

                content_box.add_widget(message_label)
                message_layout.add_widget(content_box)
                message_layout.add_widget(Label(size_hint_x=0.5))

            container.add_widget(message_layout)

        Clock.schedule_once(self.scroll_to_bottom, 0.1)

    def format_time(self, timestamp):
        if not timestamp:
            return ""
        time_part = str(timestamp).split(' ')[1] if ' ' in str(timestamp) else str(timestamp)
        return time_part[:5]

    def scroll_to_bottom(self, dt):
        scroll_view = self.ids.messages_scroll
        scroll_view.scroll_y = 0

    def send_message(self):
        message_text = self.ids.message_input.text.strip()
        if message_text and self.chat_id:
            app = App.get_running_app()
            app.db.add_message(self.chat_id, current_user.id, message_text)
            self.ids.message_input.text = ''
            self.load_chat()