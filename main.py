import tkinter as tk
import random

# Создаем главное окно
root = tk.Tk()
root.title("Игра с переводами")

# Создаем текстовое поле для ввода слов и переводов
input_text = tk.Text(root, height=10, width=30, font=("Arial", 18))
input_text.pack(pady=20)

# Глобальные переменные для графической шкалы прогресса
progress_canvas = None
progress_rectangles = []

# Функция для начала игры после ввода слов и переводов
def start_game():
    global word_dict, english_words, current_word, random_translations, correct_translation, total_words, words_translated
    word_translation_pairs = input_text.get("1.0", "end").strip().split('\n')
    word_dict = {}
    for pair in word_translation_pairs:
        parts = pair.split('-')
        if len(parts) == 2:
            word_dict[parts[0].strip()] = parts[1].strip()
    if len(word_dict) < 4:
        result_label.config(text="Введите как минимум 4 слова с переводами!", fg="red")
    else:
        english_words = list(word_dict.keys())
        random.shuffle(english_words)
        total_words = len(english_words)
        words_translated = 0
        create_progress_bar()  # Создаем графическую шкалу прогресса
        choose_word()
        input_text.pack_forget()
        start_button.config(state=tk.DISABLED)
        paste_button.pack_forget()  # Убираем кнопку после начала игры
        progress_label.config(text=f"Прогресс: {words_translated}/{total_words}")

# Функция для выбора нового слова и вариантов перевода
def choose_word():
    global current_word, random_translations, correct_translation, english_words
    if not english_words:
        question_label.config(text="Вы перевели все слова!")
        for i in range(4):
            answer_buttons[i].config(text="", state=tk.DISABLED)
    else:
        current_word = english_words.pop()
        correct_translation = word_dict[current_word]
        translations = list(word_dict.values())
        translations.remove(correct_translation)
        random_translations = random.sample(translations, 3)
        random_translations.append(correct_translation)
        random.shuffle(random_translations)
        update_question()  # Перемещаем вызов функции update_question сюда

# Функция для обновления вопроса и вариантов ответов
def update_question():
    question_label.config(text=current_word)
    for i in range(4):
        answer_buttons[i].config(text=random_translations[i], state=tk.NORMAL)

# Функция для проверки ответа пользователя
def check_answer(selected_translation):
    global correct_translation, words_translated
    if selected_translation == correct_translation:
        result_label.config(text="Правильно!", fg="green")
        root.after(1000, lambda: result_label.config(text=""))
        words_translated += 1
        update_progress_bar()  # Обновляем графическую шкалу прогресса
        if words_translated == total_words:
            question_label.config(text="Игра завершена!")
            for button in answer_buttons:
                button.config(state=tk.DISABLED)
        else:
            choose_word()  # После правильного ответа продолжаем игру
    else:
        result_label.config(text="Неправильно!", fg="red")

# Функция для вставки текста из буфера обмена
def paste_from_clipboard():
    clipboard_text = root.clipboard_get()
    input_text.delete(1.0, "end")
    input_text.insert("1.0", clipboard_text)
    paste_button.pack_forget()  # Убираем кнопку после вставки

# Создаем кнопку "Вставить из буфера обмена"
paste_button = tk.Button(root, text="Вставить из буфера обмена", font=("Arial", 18), command=paste_from_clipboard)
paste_button.pack()

# Создаем кнопку для начала игры
start_button = tk.Button(root, text="Начать игру", font=("Arial", 18), command=start_game)
start_button.pack()

# Создаем метку для вопроса
question_label = tk.Label(root, text="", font=("Arial", 24))
question_label.pack(pady=20)

# Создаем метку для результата
result_label = tk.Label(root, text="", font=("Arial", 18))
result_label.pack(pady=20)

# Создаем группы кнопок
button_frame1 = tk.Frame(root)
button_frame1.pack()

button_frame2 = tk.Frame(root)
button_frame2.pack()

# Создаем кнопки для вариантов ответов
answer_buttons = []
for i in range(4):
    button = tk.Button(
        button_frame1 if i < 2 else button_frame2,
        text="", font=("Arial", 18), width=20, height=2,
        command=lambda i=i: check_answer(random_translations[i])
    )
    answer_buttons.append(button)
    answer_buttons[i].pack(side=tk.LEFT if i < 2 else tk.RIGHT)

# Создаем функцию для создания графической шкалы прогресса
def create_progress_bar():
    global progress_canvas, progress_rectangles
    progress_canvas = tk.Canvas(root, width=total_words * 20, height=20)
    progress_canvas.pack(pady=10)
    progress_rectangles = []
    for i in range(total_words):
        x1 = i * 20
        x2 = x1 + 15
        y1 = 0
        y2 = 20
        rectangle = progress_canvas.create_rectangle(x1, y1, x2, y2, fill="lightgray")
        progress_rectangles.append(rectangle)

# Создаем функцию для обновления графической шкалы прогресса
def update_progress_bar():
    global words_translated
    if words_translated <= total_words:
        x2 = words_translated * 20
        progress_canvas.coords(progress_rectangles[words_translated - 1], 0, 0, x2, 20)

# Запускаем главное окно
root.mainloop()
