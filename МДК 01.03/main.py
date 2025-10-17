from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from database import DatabaseManager
from UI_layouts import MainScreen, AllVacanciesScreen, SearchScreen, AddVacancyScreen, MyResponsesScreen, ProfileScreen, RegisterScreen, LoginScreen, EmployerResponsesScreen, NotificationsScreen, ChatListScreen, ChatScreen


class WorkFinderApp(App):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()

    def build(self):
        self.db.create_tables()
        self.db.insert_sample_data()

        self.db.cleanup_duplicate_responses()
        self.db.debug_all_responses()

        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(AllVacanciesScreen(name='all_vacancies'))
        sm.add_widget(SearchScreen(name='search'))
        sm.add_widget(AddVacancyScreen(name='add_vacancy'))
        sm.add_widget(MyResponsesScreen(name='my_responses'))
        sm.add_widget(ProfileScreen(name='profile'))
        sm.add_widget(EmployerResponsesScreen(name='employer_responses'))
        sm.add_widget(NotificationsScreen(name='notifications'))
        sm.add_widget(ChatListScreen(name='chat_list'))
        sm.add_widget(ChatScreen(name='chat'))
        return sm

if __name__ == '__main__':
    WorkFinderApp().run()