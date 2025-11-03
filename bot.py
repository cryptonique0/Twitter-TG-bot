"""
Telegram Bot for finding early Twitter/X accounts
"""
import os
import logging
from typing import Optional
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from twitter_api import TwitterAPI
from twitter_utils import filter_early_account, format_account_info
import config

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize Twitter API
try:
    twitter_api = TwitterAPI()
except ValueError as e:
    logger.error(f"Failed to initialize Twitter API: {e}")
    twitter_api = None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    welcome_message = """
🤖 **Welcome to the Twitter Early Account Finder Bot!**

This bot helps you find early-stage Twitter/X accounts (projects) by analyzing:
- Bio keywords related to crypto, blockchain, web3, etc.
- Post count (maximum of 2 posts within a week of creation)
- Post keywords indicating new projects

**Commands:**
/start - Show this welcome message
/help - Show help information
/check @username - Check if a Twitter account matches the criteria
/search keyword - Search for accounts (limited functionality)
/settings - Show current filter settings

**Usage Example:**
Simply send: `/check @username`
Or send a username: `@username` or `username`
"""
    await update.message.reply_text(welcome_message)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_message = """
📖 **Help - How to Use**

**Main Commands:**
• `/check @username` - Analyze a Twitter account
• `/search keyword` - Search for accounts (basic)
• `/settings` - View current filter settings

**Filter Criteria:**
1. **Bio Keywords:** Account bio must contain keywords like: crypto, blockchain, web3, nft, defi, token, project, launch, building, founder, developer
2. **Post Count:** Maximum of 2 posts within the first week of account creation
3. **Post Keywords:** Posts must contain keywords like: launch, building, project, new, announcement, gm, alpha, beta, presale, whitelist

**Tips:**
- You can send just the username without the /check command
- The bot will analyze the account and tell you if it matches all criteria
- Early accounts are typically new projects in the crypto/web3 space

Need more help? Contact the bot administrator.
"""
    await update.message.reply_text(help_message)


async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show current filter settings."""
    settings_message = f"""
⚙️ **Current Filter Settings**

**Bio Keywords:**
{', '.join(config.BIO_KEYWORDS)}

**Post Keywords:**
{', '.join(config.POST_KEYWORDS)}

**Filter Rules:**
- Max posts within timeframe: {config.MAX_POSTS_WITHIN_WEEK}
- Timeframe: {config.ACCOUNT_AGE_DAYS} days from account creation

All three criteria must be met for an account to match:
✓ Bio contains at least one bio keyword
✓ Account has posted ≤ {config.MAX_POSTS_WITHIN_WEEK} times in first {config.ACCOUNT_AGE_DAYS} days
✓ Posts contain at least one post keyword
"""
    await update.message.reply_text(settings_message)


async def check_account(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Check a Twitter account against criteria."""
    if not twitter_api:
        await update.message.reply_text(
            "❌ Twitter API is not configured. Please set up your Twitter API credentials."
        )
        return
    
    # Get username from command or message
    username = None
    
    if context.args:
        username = context.args[0]
    elif update.message.text:
        # Extract username from message text
        text = update.message.text.strip()
        # Remove /check command if present
        text = text.replace('/check', '').strip()
        username = text
    
    if not username:
        await update.message.reply_text(
            "❌ Please provide a Twitter username.\n\n"
            "Usage: `/check @username` or `/check username`"
        )
        return
    
    # Remove @ if present
    username = username.lstrip('@')
    
    await update.message.reply_text(f"🔍 Analyzing @{username}... Please wait.")
    
    try:
        # Fetch user data and tweets
        result = twitter_api.get_user_profile_and_tweets(username, max_tweets=100)
        
        if not result:
            await update.message.reply_text(
                f"❌ Could not find Twitter account: @{username}\n\n"
                "Please check the username and try again."
            )
            return
        
        user_data, tweets = result
        
        # Filter account based on criteria
        filter_results = filter_early_account(
            user_data=user_data,
            tweets=tweets,
            bio_keywords=config.BIO_KEYWORDS,
            post_keywords=config.POST_KEYWORDS,
            max_posts=config.MAX_POSTS_WITHIN_WEEK,
            days=config.ACCOUNT_AGE_DAYS
        )
        
        # Format and send results
        if filter_results['matches']:
            message = format_account_info(filter_results)
            message += f"\n\n🔗 Profile: https://twitter.com/{username}"
            await update.message.reply_text(message)
        else:
            # Send details about why it didn't match
            details = filter_results['details']
            message = f"""
❌ **Account Does Not Match Criteria**

👤 **Name:** {details['name']}
🐦 **Username:** @{details['username']}
📅 **Created:** {details['created_at']}

**Filter Results:**
- Bio keywords: {'✓ Matched' if filter_results['bio_match'] else '✗ Not matched'}
- Post count (within limit): {'✓ Matched' if filter_results['post_count_match'] else '✗ Not matched'}
- Post keywords: {'✓ Matched' if filter_results['post_keywords_match'] else '✗ Not matched'}

All criteria must be met for an account to be considered an "early account."
"""
            await update.message.reply_text(message)
    
    except Exception as e:
        logger.error(f"Error checking account @{username}: {e}")
        await update.message.reply_text(
            f"❌ An error occurred while analyzing @{username}.\n\n"
            f"Error: {str(e)}"
        )


async def search_accounts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Search for Twitter accounts (limited functionality)."""
    if not twitter_api:
        await update.message.reply_text(
            "❌ Twitter API is not configured. Please set up your Twitter API credentials."
        )
        return
    
    if not context.args:
        await update.message.reply_text(
            "❌ Please provide a search keyword.\n\n"
            "Usage: `/search keyword`"
        )
        return
    
    query = ' '.join(context.args)
    
    await update.message.reply_text(f"🔍 Searching for accounts related to '{query}'... Please wait.")
    
    try:
        users = twitter_api.search_recent_users(query, max_results=10)
        
        if not users:
            await update.message.reply_text(
                f"❌ No accounts found for query: {query}"
            )
            return
        
        await update.message.reply_text(
            f"✅ Found {len(users)} accounts. Analyzing each one...\n\n"
            "This may take a moment."
        )
        
        matching_accounts = []
        
        for user_data in users:
            # Get tweets for each user
            tweets = twitter_api.get_user_tweets(user_data['id'], max_tweets=100)
            
            # Filter account
            filter_results = filter_early_account(
                user_data=user_data,
                tweets=tweets,
                bio_keywords=config.BIO_KEYWORDS,
                post_keywords=config.POST_KEYWORDS,
                max_posts=config.MAX_POSTS_WITHIN_WEEK,
                days=config.ACCOUNT_AGE_DAYS
            )
            
            if filter_results['matches']:
                matching_accounts.append(filter_results)
        
        if matching_accounts:
            await update.message.reply_text(
                f"🎉 Found {len(matching_accounts)} matching early accounts!"
            )
            
            for result in matching_accounts[:5]:  # Limit to 5 results
                message = format_account_info(result)
                username = result['details']['username']
                message += f"\n\n🔗 Profile: https://twitter.com/{username}"
                await update.message.reply_text(message)
        else:
            await update.message.reply_text(
                "❌ No accounts matched the early account criteria."
            )
    
    except Exception as e:
        logger.error(f"Error searching accounts with query '{query}': {e}")
        await update.message.reply_text(
            f"❌ An error occurred while searching.\n\n"
            f"Error: {str(e)}"
        )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle messages that might be Twitter usernames."""
    text = update.message.text.strip()
    
    # Check if message looks like a Twitter username
    # Twitter usernames: start with @ or are 3-15 alphanumeric chars plus underscore
    if text.startswith('@'):
        # Treat as username and check it
        context.args = [text]
        await check_account(update, context)
    elif len(text) >= 3 and len(text) <= 15 and all(c.isalnum() or c == '_' for c in text):
        # Could be a username without @
        context.args = [text]
        await check_account(update, context)
    else:
        await update.message.reply_text(
            "I didn't understand that. Use /help to see available commands."
        )


def main() -> None:
    """Start the bot."""
    # Get token from environment
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN not found in environment variables")
        print("Error: Please set TELEGRAM_BOT_TOKEN in your .env file")
        return
    
    # Create the Application
    application = Application.builder().token(token).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("settings", settings_command))
    application.add_handler(CommandHandler("check", check_account))
    application.add_handler(CommandHandler("search", search_accounts))
    
    # Add message handler for plain usernames
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Start the Bot
    logger.info("Starting bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
