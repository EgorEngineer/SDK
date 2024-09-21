from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler
from telegram import ReplyKeyboardMarkup
from dotenv import load_dotenv, find_dotenv
import logging
import prioritizationMethods as pm
import os
import psycopg2
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import io

# Устанавливаем соединение с базой данных PostgreSQL
def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="SDK_DB",
        user="postgres",
        password="students"
    )

# Команды для взаимодействия
ADMIN_ACTIONS = ["Create Feature", "Edit Feature", "Prioritize Features"]

# Структуры для обработки состояний
CREATE_FEATURE, EDIT_FEATURE, CHOOSE_PRIORITIZATION, VIEW_REPORT = range(4)


# Логирование ошибок
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

user_roles = {'admin','user'}
users =[]
features =[]
# Проверка роли пользователя
def is_admin(user_id):
    return user_roles.get(user_id, 'user') == 'admin'

# /start команда
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in users:
        users[user_id] = update.effective_user.username
        user_roles[user_id] = 'user'

    if is_admin(user_id):
        await update.message.reply_text("Привет, Администратор! Что бы вы хотели сделать?",
                                        reply_markup=ReplyKeyboardMarkup([ADMIN_ACTIONS], one_time_keyboard=True))
    else:
        await update.message.reply_text(
            "Привет! Вы можете проголосовать за фичи в текущем опросе. Используйте команду /vote")


# Добавляем роль администратора
async def make_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == 123456789:
        user_id = int(context.args[0])
        user_roles[user_id] = 'admin'
        await update.message.reply_text(f"Пользователь с ID {user_id} теперь является администратором.")
    else:
        await update.message.reply_text("У вас нет доступа к этой команде.")


# Начало работы с созданием фичи
async def create_feature(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("У вас нет доступа к этой команде.")
        return ConversationHandler.END

    await update.message.reply_text("Введите название новой фичи:")
    return CREATE_FEATURE


# Завершение создания фичи
async def save_feature(update: Update, context: ContextTypes.DEFAULT_TYPE):
    feature_name = update.message.text
    features.append({'name': feature_name, 'votes': 0, 'positive_votes': 0, 'negative_votes': 0})
    await update.message.reply_text(f"Фича '{feature_name}' создана.")
    return ConversationHandler.END


# Голосование за фичу
async def vote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    feature_names = [feature['name'] for feature in features]
    if not feature_names:
        await update.message.reply_text("Нет доступных фич для голосования.")
        return

    await update.message.reply_text("Выберите фичу для голосования:",
                                    reply_markup=ReplyKeyboardMarkup([feature_names], one_time_keyboard=True))
    return CREATE_FEATURE


async def handle_vote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    feature_name = update.message.text
    feature = next((f for f in features if f['name'] == feature_name), None)
    if not feature:
        await update.message.reply_text("Неверная фича.")
        return ConversationHandler.END

    feature['votes'] += 1
    await update.message.reply_text(f"Ваш голос за '{feature_name}' учтен.")
    return ConversationHandler.END


# Выбор метода приоритизации
async def prioritize_features(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("У вас нет доступа к этой команде.")
        return ConversationHandler.END

    await update.message.reply_text("Выберите метод приоритизации: /rice, /ice или /kano")


# Запуск приоритизации RICE
async def rice_prioritization(update: Update, context: ContextTypes.DEFAULT_TYPE):
    results = []
    for feature in features:
        rice_score = pm.RICE(reach=1000, impact=5, confidence=80, effort=1).calculate_rice_score()
        results.append((feature['name'], rice_score))

    results.sort(key=lambda x: x[1], reverse=True)
    report = "Отчет по RICE:\n" + "\n".join([f"{name}: {score}" for name, score in results])
    await update.message.reply_text(report)

# Метод для получения роли пользователя
def get_user_role(user_id):
    return user_roles.get(user_id, 'user')

async def generate_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if get_user_role(update.effective_user.id) != 'admin':
        await update.message.reply_text("У вас нет доступа к этой команде.")
        return

    # Получение данных о голосах и фичах из базы данных
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT f.feature_name, COUNT(v.vote_id) as total_votes,
               SUM(CASE WHEN v.vote_value > 0 THEN 1 ELSE 0 END) as positive_votes,
               SUM(CASE WHEN v.vote_value < 0 THEN 1 ELSE 0 END) as negative_votes
        FROM Features f
        LEFT JOIN Votes v ON f.feature_id = v.feature_id
        GROUP BY f.feature_id
        ORDER BY total_votes DESC
    """)
    data = cur.fetchall()
    conn.close()

    # Преобразуем данные в DataFrame
    df = pd.DataFrame(data, columns=['Feature Name', 'Total Votes', 'Positive Votes', 'Negative Votes'])

    # Если данных нет, сообщаем об этом
    if df.empty:
        await update.message.reply_text("Нет данных для отчета.")
        return

    # Настраиваем размер графика
    plt.figure(figsize=(10, 6))

    # Создаем график
    sns.barplot(x='Feature Name', y='Total Votes', data=df, palette="viridis")
    plt.title('Total Votes for Each Feature')
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    # Сохраняем график во временный файл
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Отправляем график администратору
    await update.message.reply_photo(photo=buffer)

    # Закрываем ресурсы
    buffer.close()
    plt.clf()
def main():
    application = ApplicationBuilder().token(os.getenv('TOKEN')).build()

    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("make_admin", make_admin))
    application.add_handler(CommandHandler("rice", rice_prioritization))

    # Определение обработчика голосования
    vote_handler = ConversationHandler(
        entry_points=[CommandHandler('vote', vote)],
        states={
            CREATE_FEATURE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_vote)],
        },
        fallbacks=[],
    )

    # Добавляем обработчик создания фичи
    feature_handler = ConversationHandler(
        entry_points=[CommandHandler('create_feature', create_feature)],
        states={
            CREATE_FEATURE: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_feature)],
        },
        fallbacks=[]
    )

    application.add_handler(vote_handler)
    application.add_handler(feature_handler)

    application.run_polling()


if __name__ == "__main__":
    main()