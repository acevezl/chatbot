# Pizza Chatbot with RASA

## How to run
Professor Juan, please follow these instructions to install and run the chatbot.

**Important:** This conversational agent specifically requires Python `3.10.x` due to RASA dependencies. It will not run with newer or older versions. A .venv is highly recommended to run this bot.

### Create a Virtual Environment (.venv) with Python 3.10.20
```
cd ~/rasa-chatbot
brew install python@3.10
python3.10 -m venv rasa-env
python --version
```

You should see Python `3.10.x` and your prompt should read something like:
```
(rasa-env) [prompt] $
```

#### Install RASA inside the .venv
```
python -m pip install --upgrade pip
pip install rasa
```
**Note:** Make sure you're inside ~/rasa-chatbot (`cd ~/rasa-chatbot`)

#### Init RASA
```
source rasa-env/bin/activate
export SQLALCHEMY_SILENCE_UBER_WARNING=1
rasa init
```

#### From now on, always use the .venv when running this chatbot
```
cd ~/rasa-chatbot
source rasa-env/bin/activate
```

#### Commands to run the chatbot
1. On Termina 1: Run actions
    ```
    rasa run actions
    ```
2. On Terminal 2: Train model and run shell
    ```
    rasa train
    rasa shell
    ```

#### Validate Chatbot (if needed)
```
rasa run validate
```

#### If you see this error: 
```
ERROR    rasa.core.actions.action  - Failed to run custom action 'action_start_restart_order'. Couldn't connect to the server at 'http://localhost:5055/webhook'. Is the server running? Error: Cannot connect to host localhost:5055 ssl:default [Connect call failed ('127.0.0.1', 5055)]
```

It means actions.py ain't running. Go to a separate terminal and run: 
```
run rasa actions
```
Then re-run rasa shell.


## Sample runs
The main functionality of the chatbot is to help customers to place a pizza + drinks order. Please follow the sample runs below to evaluate the bot's functionality.

### Ordering pizza and drinks
#### Happy Path
1. User greets the bot
    ```
    Examples:
    - Hello
    - Howdy
    ```

2. Bot utters `greet`
    ```
    Mamma mia! Welcome to Luigi-and-Dany's Pizzeria!
    I'm a Pizza Bot, how can I help you today?
    You can place an order or ask about our pizzas, sizes, drinks, promotions, and opening hours.
    ```

3. User starts an order
    ```
    Examples:
    - I want to place an order
    - I want a pizza
    ```

4. Bot utters `start_order`
    ```
    Alright, let's start your order. What would you like?
    ```

5. User asks for a pizza
    ```
    Examples:
    - I want a pizza
    - Can I get a pizza?
    ```

6. Bot utters `ask_pizza_type`
    ```
    We have Margherita, Marinara, Hawaiian, Veggie, or Funghi, what would you like?
    ```
   
7. User informs order
    ```
    Examples:
    - I want a margherita pizza
    - I want a veggie pizza
    ```

8. Bot utters `ask_pizza_size`
    ```
    What size would you like? (Small, Medium, Large)
    ```

9.  User informs pizza size
    ```
    Examples:
    - Small
    - Sm
    - Large
    - md
    ```

10. Bot utters an "item added" message
    ```
    I've added a {pizza_size} {pizza_type} to your order
    ```

11. Bot utters `ask_what_else`
    ```
    Alright. What else can I get you?
    ```

12. User informs drink
    ```
    Exmaples:
    - coke
    - Add a fanta
    - I want a pibb
    ```

13. Bot utters an "item added" message
    ```
    I've added a {drink} to your order.
    ```

14. Bot utters `ask_what_else`, loop continues, user can add more pizzas or drinks, until they do a `deny` intent.

15. User says nothing else or no (i.e., `deny` intent)
    ```
    Examples:
    - nothing else
    - nothing
    - all set
    ```

16. Bot summarizes order
    ```
    Here's your order:
    + small margherita pizza: 12 €
       - promo: -2 €
    + coke: 3 €
    ====================
    Total: 13 €
    ```

17. Bot utters `confirm`
    ```
    Should I place this order?
    ```

18. User says yes (i.e., `confirm_order`)
    ```
    Examples:
    - yes
    - yep
    ```

19. Bot utters `submit`
    ```
    Here's your pickup code: PIZZA-504G
    Ciao! Come back soon for more delicious pizza and drinks from Luigi-and-Dany's Pizzeria!
    ```

#### Alternate 1: User starts with order (skips greeting)

1. User starts an order right away
    ```
    Examples:
    - I want to place an order
    - Can I place an order? 
    ```

##### Then, bot follows step 4 from happy path

#### Alternate 2: User starts by asking for pizza (skips greeting, skips start order, asks for pizza)
1. User asks for a pizza right away
    ```
    Examples:
    - I want a pizza
    - Pizza
    ```

##### Then, bot follows step 6 from happy path

#### Alternate 3: User starts with specific pizza type (skips greeting, skips start order, asks for pizza type)

1. User starts a specific order
    ```
    Examples:
    - I want a veggie pizza
    - I want a margherita
    ```

2. Bot recognizes pizza_type, and utters `ask_pizza_size`
    ```
    What size would you like? (Small, Medium, Large)
    ```

3. User informs pizza size
    ```
    Examples:
    - Medium
    - md
    ```

4. Bot utters `ask_what_else`, loop continues, user can add more pizzas or drinks, until they do a `deny` intent.

#### Alternate 4: User starts with specific pizza size and type

1. User starts a specific order
    ```
    Examples:
    - I want a large marge
    - I want a medium veggie
    ```

2. Bot recognizes pizza_type and pizza_size, and adds the pizza to the order
    ```
    I've added a large margherita pizza to your order
    ```

3. Bot utters `ask_what_else`, loop continues, user can add more pizzas or drinks, until they do a `deny` intent.

#### Alternate 5: User stars with specific drink order (skips greeting, skips start order, skips pizza)

1. User starts a specific drink order
    ```
    Examples:
    - I want a coke
    - Gimme a pibb
    ```

2. Bot recognizes the drink type and utters an "item added" message
    ```
    I've added a {drink} to your order
    ```

3. Bot utters `ask_what_else`, loop continues, user can add more pizzas or drinks, until they do a `deny` intent.

#### Alternate 6: Incorrect Order / Change Order

##### After steps 1 through 14 of happy path, the customer replys with `deny` intent because the order is incorrect or they want to change it

15. Bot utters `confirm`
    ```
    Should I place this order?
    ```

16. User informs `deny` intent
    ```
    - No
    - Change order
    - Incorrect
    ```

17. Bot restarts order and utters `restart_order`

##### After this, depending on user input, it can go to happy path, or any other alternate

### Asking for Information
Another functionality of the ChatBot is to allow customers to ask for information regarding the menu (pizza types and prices), the pizza sizes, the drink types, and the opening hours.

#### Ask for pizza types

1. User asks for the menu or about what pizzas types are available
    ```
    Examples:
    - Give me the menu
    - What types of pizza do you have
    ```

2. Bot utters `pizza_types`
    ```
    We make Margherita, Marinara, Hawaiian, Veggie, or Funghi
    ```

#### Ask for pizza sizes or price

1. User asks for the pizza sizes that are available or price
    ```
    Examples:
    - What sizes do you have
    - What pizza sizes are available
    - What price are the pizzas
    ```

2. Bot utters `pizza_sizes`
    ```
    We make small (12 €), medium (14 €) and large (18 €) pizzas
    ```

#### Ask for drink types

1. User asks what drinks are available
    ```
    Examples:
    - What drinks do you have
    - What drinks do you offer
    ```

2. Bot utters `drink_types`
    ```
    We have Coke, Fanta, and Pibb, all drinks are 3 €
    ```

#### Ask for promotions

1. User asks what promotions are available
    ```
    Examples:
    - what promotions do you have
    - promos?
    ```

2. Bot utters `promotions`
    ```
    All margherita pizzas of all sizes are 2 € off!
    ```

#### Ask to summarize order

1. At any point, User asks to summarize order
    ```
    Examples:
    - Summarize my order
    - What have I ordered?
    ```

2. If the orred is NOT empty (the user has asked for pizzas and/or drinks already), the bot summarizes the order and utters `utter_confirm` to confirm if the order can be submitted.
    ```

    ```

3. If the order is empty, the bot informs the user they haven't ordered anything and asks what to get them.
   ```
   It seems you haven't ordered anything. What can I get you?
   ```

## Reference

### RASA Forms Tutorial
The following tutorial was reviewed as a base to build this chatbot.
https://www.youtube.com/watch?v=hIWnpyTWsLQ

RASA form is a building block to fetch relevant information from the conversatino and store it in long-lived slots to use in the rest of the conversation.

An active form can be thought as a loop that will keep asking for information that's missing. The form will keep asking for information until all the slots are filled.

RASA forms can be configured to detect slot values from entities.
