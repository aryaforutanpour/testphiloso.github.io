import threading  # thread / lock
import requests  # request
import json  # dumps / loads
import nltk  # word_corpus
import time  # time / sleep
import linecache  # getline
import datetime  # date
import random  # randint
import os  # environ

# General code description at the bottom of the file

# Downloading English word corpus from NLTK package
nltk.download('words')

# HuggingFace API constants
_API_URL = "https://api-inference.huggingface.co/models/sullyd/PhilosophicalQuotes"
_API_KEY = os.environ["API_KEY"]
_headers = {"Authorization": "Bearer " + str(_API_KEY)}

# Define invalid characters and word corpus
_invalid_characters = '.!"#$%&()-*+,/:;<=>?@[\\]^_`{|}~0123456789'
_word_corpus = set(nltk.corpus.words.words())


# Private function to validate the generated quote
def _is_valid_text(text):
  # If the text is empty, return False
  if len(text) == 0:
    return False

  # Split the text into individual words
  words = text.split(' ')

  # Iterate through each word
  for index in range(0, len(words)):
    word = words[index]

    # Replace each invalid character with a space
    for char in _invalid_characters:
      word = word.replace(char, ' ')

    # Remove leading/trailing spaces and split the resulting string in case the removal of invalid characters led to multiple words
    word = word.strip()
    new_words = word.split(' ')

    # Remove the old word before adding new word(s)
    words.pop(index)
    for new_word in new_words:
      # Add each new word to the list of words
      words.insert(index, new_word.strip().lower())
      index += 1

  # Remove any empty strings from the word list
  words = [word for word in words if word != '']

  for word in words:
    # If the word is not in the corpus (discounting plurals) or it contains an apostrophe in the last three characters in the word
    if (word not in _word_corpus
        and word[-1] != 's') or (word.find('\'') != -1
                                 and word.find('\'') < len(word) - 3):
      return False

  return True


def _prompt_quote(prompt, count=0):
  # Return a random daily quote if more than 3 failed attempts
  if count > 3:
    return _random_daily_quote()

  # Prepare data for the HuggingFace API call
  data = json.dumps({
    "inputs": str(prompt.strip()),
    "parameters": {
      "top_k": None,
      "top_p": 0.75,
      "temperature": 1.0,
      "repetition_penalty": 5,
      "max_new_tokens": 50,
      "max_time": 10,
      "return_full_text": False,
      "num_return_sequences": 1,
      "do_sample": True
    },
    "options": {
      "use_cache":
      False,  # Determines whether to use previously identical cached input
      "wait_for_model":
      True  # If the model is not ready, wait for it instead of receiving 503
    }
  })

  try:
    # Make POST request to HuggingFace API
    response = requests.request("POST", _API_URL, headers=_headers, data=data)

    content = json.loads(response.content.decode('utf-8'))

    # If response is empty or contains an error, raise an exception to retry quote generation
    if len(content) <= 0 or 'error' in content[0]:
      raise Exception

    # Extract generated quote text from response
    quote = content[0]['generated_text'].replace('\n', '')

    if _is_valid_text(quote):
      return prompt + quote

    # If not valid, retry or return a random daily quote if max retries exceeded
    if count >= 3:
      raise Exception
    return _prompt_quote(prompt, count + 1)

  except Exception:
    # Retry generating quote in case of exceptions, up to 3 retries
    if count < 3:
      return _prompt_quote(prompt, count + 1)

    return _random_daily_quote()


# Private function to generate random quote using a random quote starter
def _random_quote():
  number = random.randint(1, 1382)
  quote = linecache.getline('static/ai/quote_starters.txt', number)
  quote = str(quote).replace('\n', '')
  return _prompt_quote(quote)


# Private function to get a random daily quote
def _random_daily_quote():
  number = random.randint(1, 2195)
  quote = linecache.getline('static/ai/daily_quotes.txt', number)
  quote = str(quote).replace('\n', '')
  return quote


# Private lock to ensure thread-safe access to quote queue
_quotes_lock = threading.Lock()

# Private list of quotes and control variables for quote generation thread
_quotes = []  # Generated quote queue
_queue_size = 40  # Max quote queue size
_wait_time = 5  # Seconds between filling up the quote queue
_should_end = False  # Determines if the second thread should end


# Private function running in second thread to generate random quotes and fill the quote queue
def _generate_quotes():
  # Initialize / access variables
  global _should_end, _quote_thread, _quotes_lock, _quotes
  end = False
  tmp_quotes = []

  # Keep generating quotes until signalled to stop
  while not end:
    # Record the start time
    start_time = time.time()

    # Try to fill up half the queue size with new quotes
    for i in range(0, round(_queue_size / 2) - len(tmp_quotes)):
      # Generate a new random quote and append to the temporary queue
      tmp_quotes.append(_random_quote())

      # Break the loop if quote generation took longer than the wait time
      if time.time() - start_time > _wait_time:
        break

    # If quote generation was faster than the wait time, sleep for the remaining duration
    if time.time() - start_time < _wait_time:
      time.sleep(_wait_time - (time.time() - start_time))

    # Lock the quote queue before manipulating it
    with _quotes_lock:
      # Update the end variable inside the lock to ensure thread safety
      end = _should_end

      # Fill up the quote queue from the newly generated quotes
      for i in range(0, round(_queue_size / 2) - len(_quotes)):
        # Break the loop if there are no more new quotes
        if len(tmp_quotes) == 0:
          break

        # Add the new quote to the queue and remove from the new quotes list
        _quotes.append(tmp_quotes[0])
        del tmp_quotes[0]


# Create second thread with the _generate_quotes function as its target
_quote_thread = threading.Thread(target=_generate_quotes)


# Public function to get the daily quote depending on the number of days passed since a start date
def get_daily_quote():
  start_date = datetime.date(2023, 6, 20)
  current_date = datetime.date.today()
  delta = current_date - start_date
  daily_number = delta.days % 2195
  quote = linecache.getline('static/ai/daily_quotes.txt', daily_number)
  quote = str(quote).replace('\n', '')
  return quote


# Public function to get a random quote from the quote queue or generate a new one if the queue is empty
def get_random_quote():
  # Access variables
  global _should_end, _quote_thread, _quotes_lock, _quotes

  # Lock the quote list before manipulating it
  with _quotes_lock:
    # If the quote queue is not empty
    if len(_quotes) > 0:
      print("Queue Size: " + str(len(_quotes)))

      # Return the first quote from the queue and delete it
      quote = _quotes[0]
      del _quotes[0]
      return quote
    else:
      # If the quote queue is empty, generate a new random quote
      return _random_quote()


# Public function to generate a prompted quote
def get_prompted_quote(prompt):
  return _prompt_quote(prompt)


# Public function to start the quote generation thread
def start_quote_generation():
  global _quote_thread
  _quote_thread.start()


# Public function to stop the quote generation thread
def end_quote_generation():
  global _quote_thread, _quotes_lock, _should_end
  with _quotes_lock:
    _should_end = True
  _quote_thread.join(timeout=5)


"""

MAIN THREAD:
  - Manages flask / website
  - Grabs random quote generated by the second thread
    - If the quote queue is empty, generate random quote on main thread
  - Generates prompted quotes
  - Gets message of the day


SECOND THREAD:
  - Manages quote generation
    - Constantly fills up the quote queue with random quotes until full
  - Provides random quotes to the main thread via the quote queue


QUOTE GENERATION:
  - Prompted quotes
    1. Sends prompt and generation settings to huggingface
    2. Waits for response
    3. Validates generated quote (see 'quote validation' below)
      - If validation fails attempt quote generation up to 3 more times
      - If all 4 attempts fail, return a random daily quote

  - Random quotes
    1. Grabs random 3 word prompt from quote_starters.txt
    2. Generates quote with prompt (see 'prompted quotes' above)

  - Daily message
    - Returns the Xth line in daily_quotes.txt, with X being the amount of days since Jun 20
    - daily_quotes.txt is a list of pre-generated quotes

  - Quote validation
    1. Splits generated quote into words
    2. Remove all non-alphabetic characters
    3. Checks for any non-dictionary words
      - Returns false if any found, returns true otherwise

"""
