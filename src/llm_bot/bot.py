from pathlib import Path
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

from src.common.config import LLMBotConfig
from src.common.logger import get_logger
from src.llm_bot.conversation_manager import ConversationManager
from src.llm_bot.openai_client import OpenAIClient, load_system_prompt

logger = get_logger(__name__)


class LLMBot:
    def __init__(self, config: LLMBotConfig):
        self.config = config
        self.application = Application.builder().token(config.token).build()
        
        self.conversation_manager = ConversationManager(
            max_history=config.max_conversation_history
        )
        self.openai_client = OpenAIClient(config)
        
        prompt_path = Path(__file__).parent.parent.parent / "data" / "prompts" / "system_prompt.txt"
        self.system_prompt = load_system_prompt(prompt_path)
        
        self.setup_handlers()
        logger.info("LLM Bot initialized successfully")
    
    def setup_handlers(self):
        self.application.add_handler(CommandHandler("start", self.handle_start))
        self.application.add_handler(CommandHandler("help", self.handle_help))
        self.application.add_handler(CommandHandler("reset", self.handle_reset))
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
        )
    
    async def handle_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        welcome_message = (
            f"¡Hola {user.first_name}! 👋🍽️\n\n"
            "Soy tu asistente gastronómico inteligente de Sabores de Bogotá.\n\n"
            "Puedo ayudarte con:\n"
            "• Recomendaciones personalizadas de restaurantes\n"
            "• Sugerencias de platos según tus gustos\n"
            "• Opciones por tipo de cocina, presupuesto o ubicación\n"
            "• Conversaciones naturales sobre gastronomía\n\n"
            "¡Cuéntame qué se te antoja! 🍕🍜🥘"
        )
        await update.message.reply_text(welcome_message)
        logger.info(f"User {user.id} started conversation")
    
    async def handle_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        help_message = (
            "🍽️ *Comandos disponibles:*\n\n"
            "/start - Iniciar conversación\n"
            "/help - Mostrar esta ayuda\n"
            "/reset - Reiniciar conversación\n\n"
            "💬 Habla conmigo de forma natural sobre:\n"
            "• Qué tipo de comida buscas\n"
            "• Tu presupuesto o ubicación preferida\n"
            "• Restricciones dietarias (vegetariano, vegano, etc.)\n"
            "• Ocasiones especiales\n\n"
            "Recuerdo el contexto de nuestra conversación para darte mejores recomendaciones."
        )
        await update.message.reply_text(help_message, parse_mode='Markdown')
    
    async def handle_reset(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        self.conversation_manager.reset_conversation(user_id)
        
        reset_message = (
            "✅ Conversación reiniciada.\n\n"
            "¿Qué se te antoja ahora? 🍽️"
        )
        await update.message.reply_text(reset_message)
        logger.info(f"User {user_id} reset conversation")
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_message = update.message.text
        user_id = update.effective_user.id
        
        logger.info(f"User {user_id} sent: {user_message}")
        
        try:
            self.conversation_manager.add_user_message(user_id, user_message)
            
            messages = self.conversation_manager.get_messages_for_api(
                user_id, 
                self.system_prompt
            )
            
            response = await self.openai_client.get_completion(messages)
            
            self.conversation_manager.add_assistant_message(user_id, response)
            
            await update.message.reply_text(response)
            logger.info(f"Sent response to user {user_id}")
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            error_message = (
                "Lo siento, hubo un error al procesar tu mensaje. "
                "Por favor, intenta de nuevo en un momento."
            )
            await update.message.reply_text(error_message)
    
    def run(self):
        logger.info("Starting LLM Bot...")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)
