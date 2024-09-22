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
