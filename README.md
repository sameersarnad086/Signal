# Signal

**An intelligent AI news filtering and delivery system that sends personalized daily AI briefings to users based on their learning goals and knowledge level.**

Signal is a personalized AI content curation agent that fetches articles from RSS feeds, filters them through a multi-gate AI evaluation system, and delivers curated daily "bits" via WhatsApp or email. Built for business professionals who want to stay current with AI without the noise.

## Overview

Signal solves the information overload problem by:
- Fetching AI-related content from curated RSS feeds
- Running each article through a 3-gate AI filter (relevance, level, signal value)
- Generating personalized summaries tailored to each user's learning layer
- Delivering maximum 3 articles per day via WhatsApp or email
- Tracking what users have seen to avoid duplicates

## How It Works

```
RSS Feeds → Fetch → Deduplicate → 3-Gate Filter → AI Summarization → Delivery
```

### The Three-Gate Filter System

1. **Gate 1 - Relevance**: Does the article match the user's learning goal and topic interests?
2. **Gate 2 - Level**: Is it appropriate for the user's knowledge level and learning layer?
3. **Gate 3 - Signal Value**: Does it teach something genuinely useful, or is it noise/clickbait?

### Learning Layers

- **Layer 1**: Core concepts - foundational AI knowledge for beginners
- **Layer 2**: Strategy and application - how to use AI in business contexts
- **Layer 3**: Advanced thinking - deeper understanding of AI systems and trade-offs

## Features

- **Personalized Content**: Each user gets articles filtered for their specific learning goals
- **Multi-User Support**: Configure multiple users with different profiles
- **Dual Delivery**: Send via WhatsApp (Twilio) or Email (Sendinblue)
- **Deduplication**: Tracks seen articles per user to avoid repetition
- **Token Tracking**: Monitors API usage across all filtering and generation stages
- **Comprehensive Logging**: JSON logs for every run with metrics and article details
- **Rate Limit Handling**: Automatic retry logic with exponential backoff

## Architecture

### Core Components

- **`agent.py`**: Main orchestration logic
- **`feeds.py`**: RSS feed URLs curated by learning layer
- **`fetcher.py`**: RSS feed parser using feedparser
- **`filter.py`**: AI-powered 3-gate filtering system
- **`deduplicator.py`**: Per-user article tracking
- **`prompts.py`**: System prompts for AI summarization
- **`delivery.py`**: WhatsApp delivery via Twilio
- **`email_delivery.py`**: Email delivery via Sendinblue
- **`logger.py`**: Run metrics and history tracking

### AI Models Used

- **Gates 1 & 2**: `gemma-3-12b-it` (fast, efficient filtering)
- **Gate 3**: `gemini-2.5-flash-lite` (quality evaluation)
- **Summarization**: `gemini-2.5-flash` (high-quality content generation)

## Setup

### Prerequisites

- Python 3.13+ (Python 3.9 is end-of-life and not supported)
- Google Gemini API key
- Twilio account (for WhatsApp delivery)
- Sendinblue API key (for email delivery)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Signal
```

2. Create and activate a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:

Create a `.env` file in the project root:

```env
# Google Gemini API
GEMINI_API_KEY=your_gemini_api_key_here

# Twilio (for WhatsApp delivery)
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# Sendinblue (for Email delivery)
SENDINBLUE_API_KEY=your_sendinblue_api_key
SIGNAL_FROM_EMAIL=your_sender_email@example.com
```

### Configuration

Edit `config.json` to add users:

```json
{
  "users": [
    {
      "name": "John Doe",
      "whatsapp_number": "+1234567890",
      "delivery": "whatsapp",
      "knowledge_level": "beginner",
      "learning_goal": "understand AI well enough to lead teams using it",
      "learning_layer": "Layer 2",
      "topic_interests": ["AI tools", "AI strategy", "LLMs and agents"]
    },
    {
      "name": "Jane Smith",
      "email": "jane@example.com",
      "delivery": "email",
      "knowledge_level": "beginner",
      "learning_goal": "learn how to use AI in day to day work",
      "learning_layer": "Layer 1",
      "topic_interests": ["AI tools", "productivity", "workplace AI"]
    }
  ]
}
```

### Configuration Fields

- **`name`**: User's display name
- **`delivery`**: `"whatsapp"` or `"email"`
- **`whatsapp_number`** (required for WhatsApp): Full number with country code
- **`email`** (required for email): Email address
- **`knowledge_level`**: User's AI knowledge (`"beginner"`, `"intermediate"`, `"advanced"`)
- **`learning_goal`**: What the user wants to achieve
- **`learning_layer`**: `"Layer 1"`, `"Layer 2"`, or `"Layer 3"`
- **`topic_interests`**: Array of topics the user cares about

## Usage

Run Signal manually:

```bash
source .venv/bin/activate
python src/agent.py
```

### Automating Daily Runs

Use cron (macOS/Linux) or Task Scheduler (Windows):

```bash
# Run daily at 8 AM
0 8 * * * cd /path/to/Signal && /path/to/Signal/.venv/bin/python src/agent.py
```

## Project Structure

```
Signal/
├── src/
│   ├── agent.py              # Main orchestration
│   ├── feeds.py              # RSS feed URLs
│   ├── fetcher.py            # RSS parsing
│   ├── filter.py             # 3-gate AI filtering
│   ├── deduplicator.py       # Article tracking
│   ├── prompts.py            # System prompts
│   ├── delivery.py           # WhatsApp delivery
│   ├── email_delivery.py     # Email delivery
│   └── logger.py             # Run logging
├── config.json               # User profiles
├── .env                      # API keys and secrets
├── requirements.txt          # Python dependencies
├── seen_articles.json        # Deduplication tracking
└── signal_log.json           # Run history and metrics
```

## Data Files

### `seen_articles.json`
Tracks which articles each user has already received to prevent duplicates:

```json
{
  "Sameer": ["https://article1.com", "https://article2.com"]
}
```

### `signal_log.json`
Comprehensive logs for each run including:
- Timestamp
- Articles fetched and passed
- Token usage per stage
- Delivery status
- User-specific metrics

## Dependencies

- **`google-genai`**: Google's official Gemini API SDK
- **`python-dotenv`**: Environment variable management
- **`feedparser`**: RSS feed parsing
- **`twilio`**: WhatsApp message delivery
- **`sib-api-v3-sdk`**: Sendinblue email delivery

## Output Format

### WhatsApp Message Example
```
*Signal's daily AI bits — filtered for what matters to you and your goals.*

*Bit 1*
Why Microsoft's AI training focuses on limitations, not capabilities...
[content]
(Layer 2 — building on your foundations)
Link: https://example.com

Reply with 👍 liked it, 👎 missed the mark, or 💡 teach me more.
```

### Email Format
Professionally formatted HTML email with:
- Styled header with Signal branding
- Each bit in a visually distinct card
- Layer notation for each article
- Links to original sources
- Feedback prompt footer

## Cost Optimization

Signal is designed to minimize API costs:
- Gates 1 & 2 use the efficient Gemma model
- Gate 3 uses the lite Gemini model
- Only 3 articles maximum per user per day
- Token usage tracked and logged for monitoring

## Troubleshooting

### Import Errors
If you see `Import "google.genai" could not be resolved`:
- Ensure you're using Python 3.13+
- Recreate your virtual environment: `rm -rf .venv && python3 -m venv .venv`
- Reinstall dependencies: `pip install -r requirements.txt`

### Rate Limits
If you hit Gemini API rate limits:
- The system will auto-retry with exponential backoff
- Check your quota at: https://ai.dev/rate-limit
- Consider upgrading your API plan

### WhatsApp Delivery Issues
- Verify your Twilio sandbox is active
- Ensure the recipient has sent the join code to your Twilio number
- Check that WhatsApp number includes country code (e.g., `+1234567890`)

## Future Enhancements

- [ ] User feedback loop (thumbs up/down reactions)
- [ ] Adaptive learning layer progression
- [ ] Multiple delivery time preferences
- [ ] Web dashboard for configuration
- [ ] A/B testing different prompt styles
- [ ] Integration with Slack/Discord

## License

Private project - All rights reserved

## Contact

For questions or issues, contact the project maintainer.
