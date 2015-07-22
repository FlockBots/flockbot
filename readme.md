# Flockbot
Flockbot is a Python module to quickly create a bot for Reddit. 
The module is based on PRAW and uses regex to check for calls to the bots in messages, submissions and comments.

## Installation
**Using git:** 
Clone the repository and place the `flockbot` directory in the root of your application. 
Then make sure to install the dependencies listed in requirements.txt (e.g `pip install -r requirements.txt`) 

**Using pip:** 
Easier would be to just run `pip install git+https://github.com/flockbots/flockbot`. 
This should pull the dependencies with it right away. 

## Usage
Using this package consists of a few steps.

1. Creating a bot instance

        my_bot = flockbot.Bot(db_filename, log_filename)

2. Configuring it  
Read more about acquiring oauth information on Reddit in the [praw docs](http://praw.readthedocs.org/en/latest/pages/oauth.html).

        my_bot.config.subreddits = ['funny', 'pics']
        my_bot.login(
            'Some user-agent',
            {
                'client_id': 'oauth_client_id',
                'client_secret': 'oauth_client_secret'
            },
            'oauth_refresh_token'
        )


3. Creating callbacks

        class CallbackController:
            def __init__(self, some_dependency):
                self.some_dependency = some_dependency

            def reply_with_joke(self, editable, match):
                # do something with the comment/submission/message stored in editable
                # or with the regex match stored in match
                joke = "I'm old. Hello `I'm old`, I'm dad."
                return joke

4. Registering the callbacks

        some_dependency = SomeDependency()
        my_callbacks = CallbackController(some_dependency)
        
        # add the controller instance to the bot
        my_bot.attach_controller(my_callbacks)i

        # register the function with a regular expression.
        # if it finds a message/submission/comment matching the regex, it will call the function 
        my_bot.register_callback('message', 'tell me something (funny|amusing)', 'CallbackController@reply_with_joke')

It is also possible to register a regular function as a callback, as long as it accepts two parameters 
(the editable [comment, submission or message] and regex match [list of strings]).

If the callback returns a string, the bot will add it to its reply. When all callbacks have been called, it will reply every result in a single comment.

That's pretty much the gist of it. I do plan on adding some proper documentation some time. In the mean while, if you are still confused check out [Flockbots/Cigarbot](https://github.com/FlockBots/Cigarbot) as an example.


## Testing
A few tests have been added and can be run by typing `python -m unittest`.
This is far for complete and I should probably focus on adding more first.
