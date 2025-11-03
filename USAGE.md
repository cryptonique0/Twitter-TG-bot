# Usage Examples for Twitter-TG-bot

This document provides examples of how to use the Twitter-TG bot.

## Setup

1. Get your API credentials:
   - Create a Telegram bot via @BotFather
   - Get Twitter API Bearer Token from developer.twitter.com

2. Configure the bot:
```bash
cp .env.example .env
# Edit .env with your credentials
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the bot:
```bash
python bot.py
```

## Example Commands

### Starting the Bot

Send `/start` to the bot to see the welcome message:

```
🤖 Welcome to the Twitter Early Account Finder Bot!

This bot helps you find early-stage Twitter/X accounts (projects)...
```

### Checking a Twitter Account

**Option 1: Using the /check command**
```
/check @CryptoNewProject
```

**Option 2: Direct username input**
```
@CryptoNewProject
```

**Option 3: Username without @**
```
CryptoNewProject
```

### Example Response - Matching Account

When an account matches all criteria:

```
🔍 Early Account Found!

👤 Name: Crypto New Project
🐦 Username: @CryptoNewProject
📅 Created: 2024-10-28
👥 Followers: 45
📝 Tweets: 2

💬 Bio:
Building the next generation DeFi protocol on Ethereum. Join our community! 🚀

✅ Matches:
- Bio keywords: ✓
- Post count (within limit): ✓
- Post keywords: ✓

🔗 Profile: https://twitter.com/CryptoNewProject
```

### Example Response - Non-Matching Account

When an account doesn't meet the criteria:

```
❌ Account Does Not Match Criteria

👤 Name: Regular User
🐦 Username: @RegularUser
📅 Created: 2020-01-15

Filter Results:
- Bio keywords: ✗ Not matched
- Post count (within limit): ✓ Matched
- Post keywords: ✗ Not matched

All criteria must be met for an account to be considered an "early account."
```

### Searching for Accounts

```
/search crypto launch
```

This will search for recent tweets containing "crypto launch" and analyze the authors.

### Viewing Settings

```
/settings
```

Shows the current filter configuration:

```
⚙️ Current Filter Settings

Bio Keywords:
crypto, blockchain, web3, nft, defi, token, project, launch, building, founder, developer

Post Keywords:
launch, building, project, new, announcement, gm, alpha, beta, presale, whitelist

Filter Rules:
- Max posts within timeframe: 2
- Timeframe: 7 days from account creation
```

## Customizing Filters

Edit `config.py` to customize the filter criteria:

```python
# Add your own keywords
BIO_KEYWORDS = [
    "crypto",
    "blockchain",
    "your_custom_keyword"
]

# Adjust post limits
MAX_POSTS_WITHIN_WEEK = 3  # Allow up to 3 posts
ACCOUNT_AGE_DAYS = 14  # Check 14 days instead of 7
```

## Tips

1. **Finding New Projects**: Check accounts that recently tweeted about launches or announcements
2. **Avoiding False Positives**: The bot requires ALL criteria to match, ensuring quality results
3. **API Limits**: Be mindful of Twitter API rate limits when searching
4. **Privacy**: Never share your API tokens publicly

## Troubleshooting

### "Twitter API is not configured"
- Check your `.env` file has `TWITTER_BEARER_TOKEN` set
- Verify the token is valid on developer.twitter.com

### "Could not find Twitter account"
- Verify the username is correct
- Account might be private or suspended

### Rate Limiting
- Twitter API has limits (check developer.twitter.com for your tier)
- Wait 15 minutes if you hit rate limits
- Consider upgrading your Twitter API tier for more requests

## Example Workflow

1. User hears about a new crypto project on Twitter
2. User sends the username to the bot: `@NewCryptoDAO`
3. Bot analyzes:
   - Bio contains "DeFi" and "building" ✓
   - Account created 3 days ago with only 1 tweet ✓
   - Tweet contains "launch" and "announcement" ✓
4. Bot confirms it's an early account and provides profile link
5. User can investigate further and potentially find early opportunities
