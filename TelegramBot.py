from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from telegram import ReplyKeyboardMarkup
import logging
import prioritizationMethods as pm

# Структуры для обработки состояний
CREATE_FEATURE, EDIT_FEATURE, CHOOSE_PRIORITIZATION, VIEW_REPORT = range(4)

# Команды для взаимодействия
ADMIN_ACTIONS = ["Create Feature", "Edit Feature", "Prioritize Features"]

# Логирование ошибок
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

user_roles = {'admin','user'}

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
    if update.effective_user.id == 123456789:  # замените на свой ID или ID создателя бота
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
        rice_score = RICE(reach=1000, impact=5, confidence=80, effort=1).calculate_rice_score()
        results.append((feature['name'], rice_score))

    results.sort(key=lambda x: x[1], reverse=True)
    report = "Отчет по RICE:\n" + "\n".join([f"{name}: {score}" for name, score in results])
    await update.message.reply_text(report)


# Аналогично можно реализовать ICE и Kano

def main():
    # Замените "YOUR_BOT_TOKEN" на токен вашего бота
    application = ApplicationBuilder().token("YOUR_BOT_TOKEN").build()

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