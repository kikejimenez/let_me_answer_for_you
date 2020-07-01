# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/02_dialog_system.ipynb (unless otherwise specified).

__all__ = ['DialogSystem']

# Cell
from .settings import *
from deeppavlov import train_model
import logging
from unittest.mock import patch
from collections import defaultdict

import pandas as pd

logging.basicConfig(
    #filename='example.log',
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.ERROR,
    datefmt='%I:%M:%S'
)

logging.debug(" Debug Log Active")
logging.info("Hello! Welcome to our automated dialog system!")
logging.warning(' Warning Log Active')
#logging.error(' Error Log Active ')

# Cell
class DialogSystem:
    ''' The DialogSystem class implements the main methods
    defined in settings module. \n
    INPUT: \n
    - context_data_file: csv file of contexts (default: None)\n
    - faq_data_file: csv file of FAQs (default: None)\n
    - configs_faq: json config file (default: None)\n
    - download_models: Indicates if download configuration files (default: True)\n

    If the context or the faq files are not provided, a *data* directory with the missing files,
    will be created (in the same path where the module is running). \n
    When an instance is created, the 'run_shell_installs()' and 'load_and_prepare_data()' routines are called,
    also the *data* and *qa_models* attributes are created, they store the information of the dataframes
    and of the models, respectively.
    '''
    def __init__(
        self,
        context_data_file=None,
        faq_data_file=None,
        configs_faq=None,
        download_models=True
    ):
        ''' The init of the class  '''
        run_shell_installs()
        self.data = {'context': defaultdict(str), 'faq': defaultdict(str)}
        self.download = download_models
        load_and_prepare_data(
            context_data_file=context_data_file,
            faq_data_file=faq_data_file,
            configs_faq=configs_faq,
            data=self.data
        )
        self.qa_models = load_qa_models(
            config_tfidf=self.data['faq']['config'], download=self.download
        )

    def question_answer(self, question):
        ''' Gets answers to a question. \n
        INPUT: \n
        - *question* parameter \n
        The method creates the following attributes:\n
        - 'self.question' -> the question parameter \n
        - 'self.response' -> a list of possible responses \n
        - 'self.formatted_responses' -> string of the question-answer pair
        '''
        self.question = question
        self.responses, self.formatted_responses = get_responses(
            self.data['context']['df'],
            question,
            self.qa_models,
            nb_squad_results=1
        )

    def new_question_answer(self, question, answer):
        '''Adds a new question-answer pair.\n
        INPUT:\n
        - question\n
        - answer\n

        The new question-answer pair is stored in the csv in the path *self.data['faq']['path']*
        '''
        _faq = self.data['faq']
        new_faq = pd.DataFrame({'Question': [question], 'Answer': [answer]})
        _faq['df'] = _faq['df'].append(new_faq)
        _faq['df'].to_csv(_faq['path'], index=False)
        self.qa_models['faq']['tfidf'] = train_model(
            _faq['config'], download=False
        )
        self.question, self.answer = question, answer
        logging.info('FAQ dataset and model updated..')

    def new_context(self, topic, context):
        ''' Adds a new context. \n
        INPUT:\n
        - topic (The title of the context)
        - context

        The new context is stored in the csv in the path *self.data['context']['path']*
        '''
        _ctx = self.data['context']
        new_context = pd.DataFrame({'topic': [topic], 'context': [context]})
        _ctx['df'] = _ctx['df'].append(new_context)
        _ctx['df'].to_csv(_ctx['path'], index=False)
        self.topic, self.context = topic, context
        logging.info('contexts dataset updated..')