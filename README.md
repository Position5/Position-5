# Position-5

[![Pylint](https://github.com/appi147/Position-5/actions/workflows/pylint.yml/badge.svg?branch=main)](https://github.com/appi147/Position-5/actions/workflows/pylint.yml)

Dedicated to best position 5 support.

## Setting Up

- Install Python 3.10+
- Install dependencies: `pip install -r requirements.txt`
- Create a `.env` file in root directory, and place following tokens:
```
DISCORD_BOT_TOKEN=token-goes-here
CRIC_API=token-goes-here
REDDIT_ID=token-goes-here
REDDIT_SECRET=token-goes-here
```

### Linting

Use `black` and `pylint` to lint and format code:

- `pylint position5`
- `black position5`

### Run the bot

Run from root folder

- `py position5`
