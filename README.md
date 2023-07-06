## Introduction
Hello! On behalf of the Twilight Titans I would like to introduce you to our website and our robot: PhilosoBot.
Philosobot is a GPT-Neo Model trained on a dataset of inspirational quotes to generate original and helpful advice that can prove to be a motivating and inspirational tool in ones life. And now, before we properly introduce ourselfs,

We hope that Philosobot wil provide you with infinite inspirations for your infinite problems

## About the Team
Meet the Team: The following are the team members:
  - Arya: Project Manager
  - Sully: Machine Learning Engineer
  - Akillesh: Machine Learning Engineer
  - Aaron: Front-end Engineer
  - Renae: Front-end Designer
  - Payton: Data Scientist
  - Shanav: Instructor & Mentor

## How to Use
Landing page (Home):
  - Generate Message button (bottom left)
    - *Click to randomly generate an inspirational or philosophical quote by AI*
  - Message of the Day (right): Automatically generates one quote every 24 hrs

Generate Message:
- Page where generated quote is displayed
- Features:
  - Saved button: 
  - Prompt input: Allows users to input a sentence stem
    - Philosobot completes sentence stem in a philosophical and inspirational way
  - Generate Message button

Saved Quotes:
- Save button saves quotes you like
- Can find quotes in Saved Quotes
- Features:
  - Search bar: Users can search for saved quotes
  - Arrows: Users can easy navigate between saved quotes

## Technical Stack
Front-End: HTML, CSS, JS

Back-End: Python, Flask

## Dataset
The model is trained on two inspirational datasets, which provide a wide range of positive and uplifting content.

1. [Inspirational Quotes Dataset](https://www.kaggle.com/datasets/mattimansha/inspirational-quotes)
2. [Goodreads Quotes Dataset](https://www.kaggle.com/datasets/abhishekvermasg1/goodreads-quotes)

These two datasets were combined into a total quote count of 3500.
All quotes longer than 25 words were removed from the combined dataset to have a more uniform quote length and reduce padding.

## Type of Model
We opted to utilize the GPT Neo 125M parameter model, generously provided by AleutherAI. Our decision to select this particular model was driven by several factors. \
Its relatively smaller size and computational requirements compared to larger models, such as the 1.3B parameter model, made it more accessible for training within Colab.\
Despite our attempts with the larger model, the technical constraints of Colab prevented its training.

## Libraries Used
This project makes use of several libraries to facilitate the development and deployment of the inspirational quotes generator. The following libraries were instrumental in building the website and training the model:

- Tranformers: Providing the model to be trained
- NLTK: Tokenizing dataset and dictionary check generated words
- Torch: Training the model
- Requests: Generating quotes via HuggingFace API
- OS: Getting HuggingFace API key
- Json: Packaging and parsing data to send to HuggingFace
- Flask: Communicating with the front-end website
- Threading: Generating quotes before user presses generate button
- Time: Calculating how long a function has ran for and sleeping
- Linecache: Getting daily message and quote starters from files
- Random: Randomizing quote generation
- Datetime: Get current day for daily message

And we hope that Philosobot wil provide you with infinite inspirations for your infinite problems