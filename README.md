# StockBot

Developed with [Can Narin](https://github.com/cannarin025).

StockBot is a stock monitor tool with Discord integration, used to monitor stock of graphics cards in the ongoing shortage.

- Monitors popular websites for stock of Nvidia graphics cards
- Sends a Discord message when stock is available
- Designed to be extendable to other websites or products with minimal effort

## Roadmap

 * [x] Basic Discord integration
 * [x] Parsing of stock data from JSON API responses
 * [ ] Parsing of stock data from HTML webpages
 * [ ] Merging data monitors with Discord bot
 * [ ] More flexible website data definitions - JSON or YML files
 * [ ] Test suite
 * [ ] Production ready!
 * [ ] More customisation and control via Discord commands

## Getting Started

Python 3.9 and pip are required. 

Clone the repo, then run
```
cd StockBot
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Add a line containing your Discord bot token (https://discord.com/developers/applications) to `config.yml`:
```
token: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
and set the stock notifications channel and role.

## Usage

To run the bot, use
```
python main.py
```

The bot uses the `,` prefix by default, which may be modified in `config.yml`. Sending `,help` in any Discord channel will bring up a help message.

## Development

### Structure

Add to this once we figure out a proper structure.

### Extension

Extend APIParser or HTMLParser, defining selectors. Expand this!

---

If you find a bug, please submit an issue!
