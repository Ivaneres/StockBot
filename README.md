# StockBot

![example workflow](https://github.com/Ivaneres/StockBot/actions/workflows/python-app.yml/badge.svg)

Developed with [Can Narin](https://github.com/cannarin025).

StockBot is a stock monitor tool with Discord integration, used to monitor stock of graphics cards in the ongoing shortage.

- Monitors popular websites for stock of Nvidia graphics cards
- Sends a Discord message when stock is available
- Designed to be extendable to other websites or products with minimal effort

## Roadmap

 * [x] Basic Discord integration
 * [x] Parsing of stock data from JSON API responses
 * [x] Parsing of stock data from HTML webpages
 * [x] Merging data monitors with Discord bot
 * [x] More flexible website and JSON data definitions - YML files
 * [x] Test suite
 * [x] Product category definitions
 * [ ] Discord thread-based new stock notification messages
 * [ ] Per-user persistent product subscription system with price filtering
 * [ ] Production ready!
 * [ ] Advanced data definitions - companion .py files and extension of `StockMonitor` class
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

This project relies on relatively new Discord API features, so the latest version of [pycord](https://github.com/Pycord-Development/pycord) is required. To install it, run

```
git submodule init
git submodule update --remote
cd pycord ; pip install .
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

### Extension

New data sources and products may be added easily to this bot. 

#### Sources

Sources are defined in the `sources/` directory, using YAML files. The YAML layout is as follows:
```yaml
type: api | html
url: website or api url
headers: any necessary request headers
products: products directories
selectors: (see selectors docs for details)
```

#### Products

YAML files. Define a key `match` which is used to regex match by titles, and `name`.

See the implemented sources for examples.

---

### Structure

#### data/

Everything related to scraping data from the web or APIs. Abstract class `StockMonitor` in `monitor.py` defines an interface for monitors - custom implementations of monitors inherit this.

#### discord_bot/

Discord bot files. Settings are in `config.yml`, commands are defined in `cogs`.

---

If you find a bug, please submit an issue!
