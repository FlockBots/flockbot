# Flockbot
Flockbot is a Python module to quickly create a bot for Reddit. 
The module is based on PRAW and uses regex to check for calls to the bots in messages, submissions and comments.

## Installation
### Git - Clone the repository
Clone the repository and place the `flockbot` directory in the root of your application.
Then install the dependencies using pip: `pip install -r requirements.txt`

### pip
Easier would be to just run `pip install git+https://github.com/flockbots/flockbot`.
This should pull the dependencies with it right away.

## Usage
More info soon. Meanwhile checkout [Flockbots/Cigarbot](https://github.com/FlockBots/Cigarbot) to see this package in use.

## Testing
A few tests have been added and can be run by typing `python -m unittest`.
This is far for complete and I should probably focus on adding more first.

## Todo
First thing to do is add more tests.
Perhaps a few logging statements for those who want to keep track of the bot as it wanders Reddit.
