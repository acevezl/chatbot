# Pizza Chatbot with RASA

## Stories

### Order Pizza
The main functionality of the chatbot is to help customers to place a pizza + drinks order. 

#### Happy Path
1. User greets the bot
    ```
    Examples:
    - Hello
    - Howdy
    ```

2. Bot utters `greet`
    ```
    Mamma mia! Welcome to Luigi-and-Dany's  pizzeria! What can I get you?`
    ```

3. User starts an order
    ```
    Examples:
    - I want to place an order
    - I want a pizza
    ```

4. Bot utters `ask_pizza_type`
    ```
    What pizza type would you like? (Margherita, Marinara, Hawaiian, Veggie, or Funghi)
    ```

5. User informs pizza type
    ```
    Examples:
    - [margherita](pizza_type)
    ```

6. Bot utters `ask_pizza_size`
    ```
    What pizza size would you like? (Small, Medium, Large)
    ```

7. User informs pizza size
    ```
    Examples:
    - [small](pizza_size)
    ```

8. Bot utters an "item added" message
    ```
    I've added a {pizza_size} {pizza_type} to your order
    ```

9. Bot utters `ask_what_else`
    ```
    Alright. What else?
    ```

10. User informs drink
    ```
    Exmaples:
    - [coke](drinks)
    - Add a [fanta](drinks)
    ```

11. Bot utters an "item added" message
    ```
    I've added a {pizza_size} {pizza_type} to your order
    ```

12. Bot utters `ask_what_else`, loop continues, user can add more pizzas or drinks, until they do a `deny` intent.

13. User says nothing else or no (i.e., `deny` intent)
    ```
    Examples:
    - nothing else
    - no thank you

    ```

14. Bot summarizes order

15. Bot utters `confirm`
    ```
    Should I place this order?
    ```

16. User says yes (i.e., `confirm_order`)
    ```
    Examples:
    - yes
    - a'ight
    ```

17. Bot utters `submit`
    ```
    I will now make your order.
    Here's your order:
        {order_items}
    Total: {total} €
    Pickup code: {code}
    Ciao!
    ```

#### Alternate 1: User starts with order (skips greeting)

1. User starts an order right away
    ```
    Examples:
    - I want to place an order
    - I want a pizza
    ```

2. Bot utters `greet`
    ```
    Mamma mia! Welcome to Luigi-and-Dany's  pizzeria! What can I get you?`
    ```

3. Bot utters `ask_pizza_type`
    ```
    What pizza type would you like? (Margherita, Marinara, Hawaiian, Veggie, or Funghi)
    ```

##### After this, follow step 5 from happy path

#### Alternate 2: User starst with specific order (skips greeting, skips start order)

1. User starts a specific order
    ```
    Examples:
    - [small](pizza_size) pizza
    - I want a [medium](pizza_size) pizza
    ```

2. Bot recognizes pizza_size and pizza_type, utters an "item added" message
    ```
    I've added a {pizza_size} {pizza_type} to your order
    ```

3. Bot utters `ask_what_else`, loop continues, user can add more pizzas or drinks, until they do a `deny` intent.

##### After this, follow step 13 of happy path

#### Alternate 3: User stars with specific drink order (skips greeting, skips start order)

1. User starts a specific drink order
    ```
    Examples:
    - [coke](drinks)
    - I want a [pibb](drinks)
    ```

2. Bot recognizes pizza_size and pizza_type, utters an "item added" message
    ```
    I've added a {drink} to your order
    ```

3. Bot utters `ask_what_else`, loop continues, user can add more pizzas or drinks, until they do a `deny` intent.

##### After this, follow step 13 of happy path

#### Alternate 4: Incorrect Order / Change Order

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

### Ask for Information
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
    - what drinks do you have
    - what drinks do you offer
    ```

2. Bot utters `drink_types`
    ```
    We make small (12 €), medium (14 €) and large (18 €) pizzas
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
    We make small (12 €), medium (14 €) and large (18 €) pizzas
    ```

## Tutorials

### RASA Forms Tutorial
https://www.youtube.com/watch?v=hIWnpyTWsLQ

RASA form is a building block to fetch relevant information from the conversatino and store it in long-lived slots to use in the rest of the conversation.

An active form can be thought as a loop that will keep asking for information that's missing. The form will keep asking for information until all the slots are filled.

RASA forms can be configured to detect slot values from entities.


## Activate .venve (With Python 3.10.20)
source /Users/arnaut/chatbot/rasa-env/bin/activate

## Init RASA
cd /Users/arnaut/chatbot
source rasa-env/bin/activate
export SQLALCHEMY_SILENCE_UBER_WARNING=1
rasa init

## Validate Data
rasa run validate

## Run Actions
rasa run actions

## Train Rasa
rasa train

## Run RASA
rasa shell

## Debugging

### ERROR: Failed to run custom action

If this error is displayed:
```
ERROR    rasa.core.actions.action  - Failed to run custom action 'action_start_restart_order'. Couldn't connect to the server at 'http://localhost:5055/webhook'. Is the server running? Error: Cannot connect to host localhost:5055 ssl:default [Connect call failed ('127.0.0.1', 5055)]
```

It means actions aren't running. Go to a separate terminal and run: 
```
run rasa actions
```
Then re-run rasa shell.