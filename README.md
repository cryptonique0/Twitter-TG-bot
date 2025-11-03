# Twitter-TG-bot
Telegram Bot for Finding Early Twitter/X Accounts

A Telegram bot that helps identify early-stage Twitter/X accounts (projects) by analyzing their bio, post frequency, and post content. Perfect for discovering new crypto, blockchain, and web3 projects.

## Features

- 🔍 **Bio Analysis**: Filters accounts by keywords in their bio (crypto, blockchain, web3, nft, defi, etc.)
- 📊 **Post Frequency Check**: Identifies accounts with maximum 2 posts within the first week of creation
- 📝 **Content Analysis**: Checks post content for project-related keywords (launch, building, announcement, etc.)
- 🤖 **Easy to Use**: Simple Telegram interface with multiple command options

## Requirements

- Python 3.8+
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- Twitter API Bearer Token (from [Twitter Developer Portal](https://developer.twitter.com/))

## Installation

1. Clone the repository:
```bash
git clone https://github.com/cryptonique0/Twitter-TG-bot.git
cd Twitter-TG-bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file from the example:
```bash
cp .env.example .env
```

4. Edit `.env` and add your API credentials:
```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TWITTER_BEARER_TOKEN=your_twitter_bearer_token_here
```

## Getting API Credentials

### Telegram Bot Token

1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` command
3. Follow the instructions to create your bot
4. Copy the bot token provided

### Twitter API Bearer Token

1. Go to [Twitter Developer Portal](https://developer.twitter.com/)
2. Create a new project and app
3. Go to your app's "Keys and tokens" section
4. Generate and copy the Bearer Token

## Usage

1. Start the bot:
```bash
python bot.py
```

2. Open Telegram and find your bot

3. Available commands:
   - `/start` - Show welcome message
   - `/help` - Show help information
   - `/check @username` - Analyze a specific Twitter account
   - `/search keyword` - Search for accounts (limited)
   - `/settings` - View current filter settings

4. You can also just send a Twitter username directly:
   - `@username`
   - `username`

## Filter Criteria

An account is considered an "early account" if it meets **ALL** of the following criteria:

1. **Bio Keywords**: The account bio contains at least one of these keywords:
   - crypto, blockchain, web3, nft, defi, token, project, launch, building, founder, developer

2. **Post Count**: The account has posted a maximum of 2 times within the first week of creation

3. **Post Keywords**: The posts contain at least one of these keywords:
   - launch, building, project, new, announcement, gm, alpha, beta, presale, whitelist

## Configuration

You can customize the filter criteria by editing `config.py`:

```python
# Keywords to search in bio
BIO_KEYWORDS = [...]

# Keywords to search in posts
POST_KEYWORDS = [...]

# Filter settings
MAX_POSTS_WITHIN_WEEK = 2  # Maximum posts allowed
ACCOUNT_AGE_DAYS = 7  # Days to check from account creation
```

## Example Output

When a matching account is found:

```
🔍 Early Account Found!

👤 Name: CryptoProject
🐦 Username: @newcryptoproject
📅 Created: 2024-10-28
👥 Followers: 45
📝 Tweets: 2

💬 Bio:
Building the next generation DeFi protocol. Join our community!

✅ Matches:
- Bio keywords: ✓
- Post count (within limit): ✓
- Post keywords: ✓

🔗 Profile: https://twitter.com/newcryptoproject
```

## Project Structure

```
Twitter-TG-bot/
├── bot.py              # Main Telegram bot implementation
├── twitter_api.py      # Twitter API wrapper
├── twitter_utils.py    # Utility functions for filtering
├── config.py           # Configuration and filter settings
├── requirements.txt    # Python dependencies
├── .env.example        # Example environment variables
├── .gitignore         # Git ignore file
└── README.md          # This file
```

## Troubleshooting

### "Twitter API is not configured"
- Make sure your `TWITTER_BEARER_TOKEN` is set correctly in the `.env` file
- Verify your Twitter API credentials are valid

### "Could not find Twitter account"
- Check that the username is correct (without @)
- The account might be private or suspended

### Rate Limiting
- Twitter API has rate limits. If you hit them, wait a few minutes before trying again
- Consider implementing caching for frequently checked accounts

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Disclaimer

This bot is for educational and research purposes. Make sure to comply with Twitter's Terms of Service and API usage guidelines when using this bot.
