# Pizza Chatbot with RASA

## 

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