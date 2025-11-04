from pathlib import Path
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

from src.common.config import NLPBotConfig
from src.common.logger import get_logger
from src.nlp_bot.nlp_engine import NLPEngine, load_corpus_from_json

logger = get_logger(__name__)


class NLPBot:
    def __init__(self, config: NLPBotConfig):
        self.config = config
        self.application = Application.builder().token(config.token).build()
        
        corpus_path = Path(__file__).parent.parent.parent / "data" / "corpus" / "qa_pairs.json"
        corpus = load_corpus_from_json(corpus_path)
        self.nlp_engine = NLPEngine(
            corpus=corpus,
            similarity_threshold=config.similarity_threshold
        )
        
        self.setup_handlers()
        logger.info("NLP Bot initialized successfully")
    
    def setup_handlers(self):
        self.application.add_handler(CommandHandler("start", self.handle_start))
        self.application.add_handler(CommandHandler("help", self.handle_help))
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
        )
    
    async def handle_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        welcome_message = (
            f"¡Hola {user.first_name}! 👋🍽️\n\n"
            "Bienvenido a Sabores de Bogotá, tu asistente gastronómico.\n\n"
            "Puedo ayudarte con:\n"
            "• Recomendaciones de restaurantes\n"
            "• Sugerencias de platos\n"
            "• Opciones por tipo de cocina\n"
            "• Lugares según tu presupuesto\n\n"
            "¿Qué se te antoja hoy?"
        )
        await update.message.reply_text(welcome_message)
        logger.info(f"User {user.id} started conversation")
    
    async def handle_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        help_message = (
            "🍽️ *Comandos disponibles:*\n\n"
            "/start - Iniciar conversación\n"
            "/help - Mostrar esta ayuda\n\n"
            "💬 Pregúntame sobre restaurantes, platos, o tipos de cocina. "
            "Por ejemplo:\n"
            "• '¿Dónde puedo comer sushi?'\n"
            "• 'Quiero comida italiana'\n"
            "• 'Recomiéndame algo vegetariano'\n"
            "• '¿Restaurantes económicos?'"
        )
        await update.message.reply_text(help_message, parse_mode='Markdown')
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_message = update.message.text
        user_id = update.effective_user.id
        
        logger.info(f"User {user_id} sent: {user_message}")
        
        try:
            answer, score = self.nlp_engine.find_best_match(user_message)
            
            if answer:
                response = answer
                logger.info(f"Matched with score {score:.3f}")
            else:
                response = self.nlp_engine.get_fallback_response()
                logger.info(f"No match found (best score: {score:.3f})")
            
            await update.message.reply_text(response)
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            error_message = (
                "Lo siento, hubo un error al procesar tu mensaje. "
                "Por favor, intenta de nuevo."
            )
            await update.message.reply_text(error_message)
    
    def run(self):
        logger.info("Starting NLP Bot...")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)
