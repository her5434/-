
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox, ttk
from datetime import datetime
import random
import platform

# Возможные смайлы
EMOJIS = [
    "🙂", "😀", "😂", "😍", "😢", "😎",
    "😜", "🤔", "🥳", "😡", "😱", "😇"
]

# Шутки про 2017 год
JOKES_2017 = [
    "Почему 2017 был худшим годом для музыки? Все перепевали одни и те же песни!",
    "Как 2017 год смотрел на другие года? 'Я просто период перехода!'",
    "Почему в 2017 году так много мемов? Потому что люди просто не знали, как это пережить!",
    "Какую машину купил 2017 год? 'Мартин Мартин'-надоум! Понимаете, это отсылка к тому, что в это время вышло много фильмов!",
    "Почему 2017 год был слишком долгим? Потому что мы все ждали окончания сезона 'Игры престолов'!"
]

# Шутки про Linux и Windows
JOKES_LINUX_WINDOWS = [
    "Почему линуксеры не могут играть в прятки? Потому что хорошего хоста найти трудно!",
    "Почему Windows лучше Linux? Потому что Windows не требует машинного времени для компиляции!",
    "Почему программисты не могут работать на Windows? Потому что им слишком трудно выдавать ошибки!",
    "Как отличить пользователя Windows от пользователя Linux? Очень просто, пользователь Windows не знает, как перезагрузить систему без мыши!",
    "Почему Linux лучше Windows? Потому что Linux не спрашивает: 'Вы уверены?' каждые 5 минут!"
]

class ChatClient:
    def __init__(self, host='127.0.0.1', port=5555):
        self.root = tk.Tk()
        self.root.title("Чат")
        self.root.geometry("400x600")
        self.root.configure(bg="#eaeaea")
        
        # Отображаемая операционная система
        os_info = platform.system() + " " + platform.release()
        os_label = ttk.Label(self.root, text=f"Операционная система: {os_info}", font=("Arial", 12))
        os_label.pack(pady=5)

        # Стили
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Счётчик пользователей
        self.user_count_label = ttk.Label(self.root, text="Пользователей в чате: 0", font=("Arial", 12))
        self.user_count_label.pack(pady=5)

        # Чат
        self.font_size = 10
        self.chat_area = scrolledtext.ScrolledText(self.root, state='disabled', wrap=tk.WORD,
                                                    bg="#f9f9f9", font=("Arial", self.font_size), fg="black",
                                                    borderwidth=0)
        self.chat_area.pack(padx=10, pady=10, fill='both', expand=True)

        # Фрейм для ввода
        input_frame = ttk.Frame(self.root)
        input_frame.pack(padx=10, pady=5, fill='x')

        # Поле ввода
        self.message_entry = ttk.Entry(input_frame)
        self.message_entry.pack(side=tk.LEFT, fill='x', expand=True)

        # Кнопки
        emoji_button = ttk.Button(input_frame, text="😊", command=self.insert_emoji, width=2)
        emoji_button.pack(side=tk.LEFT)
        
        time_button = ttk.Button(input_frame, text="Время", command=self.show_time, width=10)
        time_button.pack(side=tk.LEFT)
        
        self.send_button = ttk.Button(input_frame, text="Отправить", command=self.send_message, width=10)
        self.send_button.pack(side=tk.LEFT)
        
        program_info_button = ttk.Button(input_frame, text="О программе", command=self.show_info)
        program_info_button.pack(side=tk.LEFT)

        # Кнопка выбора темы
        theme_button = ttk.Button(input_frame, text="Выбор темы", command=self.change_theme)
        theme_button.pack(side=tk.RIGHT)

        # Кнопка настроек
        settings_button = ttk.Button(input_frame, text="Настройки", command=self.open_settings)
        settings_button.pack(side=tk.RIGHT)

        # Вкладка для шуток
        joke_button = ttk.Button(input_frame, text="Шутки", command=self.open_joke_window)
        joke_button.pack(side=tk.RIGHT)

        # Запрос ника
        self.nickname = self.get_nickname()
        if not self.nickname:
            self.nickname = "Гость"

        # Соединение
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

        self.user_list = []  # Список пользователей
        threading.Thread(target=self.receive_messages, daemon=True).start()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def open_joke_window(self):
        joke_window = tk.Toplevel(self.root)
        joke_window.title("Шутки")
        joke_window.geometry("300x400")

        # Окно для шуток с оранжевым текстом
        joke_area = scrolledtext.ScrolledText(joke_window, state='disabled', wrap=tk.WORD,
                                                bg="#f9f9f9", font=("Arial", 10), fg="orange",
                                                borderwidth=0)
        joke_area.pack(padx=10, pady=10, fill='both', expand=True)

        # Кнопки для выбора типа шуток
        joke_2017_button = ttk.Button(joke_window, text="Шутка про 2017", command=lambda: self.display_joke(joke_area, JOKES_2017))
        joke_2017_button.pack(pady=5)
        
        joke_linux_windows_button = ttk.Button(joke_window, text="Шутка про Linux/Windows", command=lambda: self.display_joke(joke_area, JOKES_LINUX_WINDOWS))
        joke_linux_windows_button.pack(pady=5)

    def display_joke(self, joke_area, jokes):
        joke = random.choice(jokes)
        joke_area.configure(state='normal')
        joke_area.insert(tk.END, f"{joke}\n")
        joke_area.configure(state='disabled')
        joke_area.see(tk.END)

    def show_info(self):
        messagebox.showinfo("О программе", "Чат-программа для общения.\nВерсия 1.0")

    def change_theme(self):
        themes = [
            ("Светлая", "#ffffff", "#eaeaea", "#f9f9f9", "black"),
            ("Тёмная", "#333333", "#444444", "#555555", "white"),
            ("Зелёная", "#4caf50", "#388e3c", "#e8f5e9", "white"),
            ("Синяя", "#2196f3", "#1976d2", "#bbdefb", "white"),
            ("Красная", "#f44336", "#d32f2f", "#ffcdd2", "white"),
            ("Серая", "#9e9e9e", "#757575", "#efefef", "black"),
        ]
        theme_names = [theme[0] for theme in themes]
        selected_theme = simpledialog.askstring("Выбор темы", "Введите название темы: \n(Светлая, Тёмная, Зелёная, Синяя, Красная, Серая)")

        for theme in themes:
            if selected_theme and selected_theme.lower() == theme[0].lower():
                self.style.configure("TButton", background=theme[1], foreground=theme[4])
                self.root.configure(bg=theme[2])
                self.chat_area.configure(bg=theme[3], fg=theme[4], font=("Arial", self.font_size))
                return
        
        messagebox.showerror("Ошибка", "Такой темы не существует!")

    def open_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Настройки")
        settings_window.geometry("300x400")

        # Размер шрифта
        self.font_size = simpledialog.askinteger("Размер шрифта", "Введите размер шрифта:", initialvalue=10)

        font_size_label = ttk.Label(settings_window, text="Размер шрифта:")
        font_size_label.pack(pady=10)

        font_size_entry = ttk.Entry(settings_window)
        font_size_entry.insert(0, str(self.font_size))
        font_size_entry.pack(pady=10)

        apply_button = ttk.Button(settings_window, text="Применить", command=lambda: self.apply_font_size(font_size_entry.get()))
        apply_button.pack(pady=10)

        # Выбор стиля заголовков окон
        ttk.Label(settings_window, text="Выберите стиль заголовка окон:").pack(pady=10)

        self.header_style_var = tk.StringVar(value="Обычный")  # Устанавливаем обычный стиль по умолчанию
        ttk.Radiobutton(settings_window, text="Обычный", value="Обычный", variable=self.header_style_var, command=self.change_header_style).pack(anchor=tk.W)
        ttk.Radiobutton(settings_window, text="Aero", value="Aero", variable=self.header_style_var, command=self.change_header_style).pack(anchor=tk.W)

    def change_header_style(self):
        selected_style = self.header_style_var.get()
        if selected_style == "Aero":
            self.root.wm_attributes("-alpha", 0.9)  # Прозрачность (Aero)
        else:
            self.root.wm_attributes("-alpha", 1.0)  # Обычный стиль

    def apply_font_size(self, size):
        try:
            self.font_size = int(size)
            self.chat_area.configure(font=("Arial", self.font_size))
            messagebox.showinfo("Успех", "Размер шрифта применён!")
        except ValueError:
            messagebox.showerror("Ошибка", "Введите действительное число.")

    def get_nickname(self):
        nickname = simpledialog.askstring("Никнейм", "Введите ваш никнейм:", parent=self.root)
        if nickname:
            return nickname.strip()
        else:
            messagebox.showerror("Ошибка", "Никнейм обязателен!")
            self.root.destroy()
            return None

    def send_message(self):
        message = self.message_entry.get()
        if message:
            timestamp = datetime.now().strftime("[%H:%M:%S]")  # Добавляем время
            full_message = f"{timestamp} {self.nickname}: {message}"
            self.socket.send(full_message.encode('utf-8'))
            self.display_message(full_message)
            self.message_entry.delete(0, tk.END)

    def insert_emoji(self):
        emoji_window = tk.Toplevel(self.root)
        emoji_window.title("Выберите смайл")
        emoji_window.geometry("200x300")

        for emoji in EMOJIS:
            button = ttk.Button(emoji_window, text=emoji, command=lambda e=emoji: self.add_emoji_to_entry(e), width=2)
            button.pack(pady=5)

    def add_emoji_to_entry(self, emoji):
        current_text = self.message_entry.get()
        self.message_entry.delete(0, tk.END)
        self.message_entry.insert(0, current_text + emoji)

    def show_time(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.display_message(f"[Системное сообщение] Текущее время: {current_time}")

    def display_message(self, message):
        self.chat_area.configure(state='normal')
        self.chat_area.insert(tk.END, message + '\n')
        self.chat_area.configure(state='disabled')
        self.chat_area.see(tk.END)

    def update_user_count(self):
        self.user_count_label.config(text=f"Пользователей в чате: {len(self.user_list)}")

    def receive_messages(self):
        while True:
            try:
                message = self.socket.recv(4096)
                decoded_message = message.decode('utf-8')
                if decoded_message.startswith("USER_LIST:"):
                    self.user_list = decoded_message.split(":")[1].split(",")
                    self.update_user_count()
                else:
                    self.display_message(decoded_message)
            except Exception:
                break

    def on_closing(self):
        self.socket.close()
        self.root.quit()

if __name__ == "__main__":
    ChatClient()
