# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/01_dialog_system.ipynb (unless otherwise specified).

__all__ = ['run_shell_installs', 'action_over_list_f', 'replacement_f', 'updates_faq_config_file',
           'select_faq_responses', 'select_squad_responses', 'load_qa_models', 'format_responses', 'get_responses',
           'get_input', 'new_answer', 'question_response', 'set_minimal_faq_questions', 'set_minimal_contexts',
           'set_data_dict', 'load_and_prepare_data', 'dialog_system']

# Cell
# export
from deeppavlov import configs,build_model,train_model
import json
from os import path,popen,mkdir
from shutil import copyfile
import pandas as pd
import numpy as np
from pathlib import Path
import logging
from collections import defaultdict

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG, datefmt='%I:%M:%S')
logging.info("Hello! Welcome to our automated dialog system!")
logging.debug("test: for Debug?")
logging.error(' Error Log Active ')

# Cell
def run_shell_installs():
    ''' Run install commands
    '''
    command_strings = (
        ' pip install deeppavlov',
        ' python -m deeppavlov install squad',
        ' python -m deeppavlov install squad_bert',
        ' python -m deeppavlov install fasttext_avg_autofaq',
        ' python -m deeppavlov install fasttext_tfidf_autofaq',
        ' python -m deeppavlov install tfidf_autofaq',
        ' python -m deeppavlov install tfidf_logreg_autofaq ',
        ' python -m deeppavlov install tfidf_logreg_en_faq'
    )
    for command in command_strings:
        logging.debug(command)
        logging.debug(popen(command).read())


# Cell
def action_over_list_f(arr, v):

    k_id, v_id = next(iter(v[0].items()))

    for p, a in enumerate(arr):
        if k_id in a.keys() and a[k_id] == v_id:
            for k_rep, v_rep in v[1].items():
                arr[p][k_rep] = v_rep


def replacement_f(model_config, **args):
    '''Replaces the model config dictionary with new values
    '''
    for k, v in args.items():
        if isinstance(v, dict):
            replacement_f(model_config[k], **v)
        if isinstance(v, str):
            model_config[k] = v
        if isinstance(model_config[k], list):
            action_over_list_f(model_config[k], v)

# Cell
def updates_faq_config_file(
    configs_path,
    **args
):
    '''Updates deepplavov json config file
    '''
    #set FAQ data in config file
    model_config = json.load(open(configs_path))

    if 'data_url' in model_config['dataset_reader']:
        del model_config['dataset_reader']['data_url']

    replacement_f(model_config=model_config,**args)

    json.dump(model_config, open(configs_path, 'w'))

# Cell
def select_faq_responses(faq_model, question):
    '''Calls Deeppavlov FAQ model
    '''
    return faq_model([question])[0]

# Cell
def select_squad_responses(
    contexts, squad_model, question, best_results=1
):
    '''Calls Deeppavlov BERT and RNET Context Question Answering
    '''
    responses = contexts.context.apply(
        lambda context: squad_model([context], [question])
    ).values

    logging.debug(f'Responses: {responses}')
    top_responses = [
        r[0][0] for r in sorted(responses, key=lambda x: -1 * x[2][0])
        [:best_results]
    ]

    logging.debug(f'Top Responses: {top_responses}')
    return responses, top_responses

# Cell
def load_qa_models(
    config_rnet=configs.squad.squad,
    config_bert=configs.squad.squad_bert,
    config_tfidf=configs.faq.tfidf_logreg_en_faq,
    download=True
):
    qa_models = {
        'squad':
            {
                'rnet': build_model(config_rnet, download=download),
                'bert': build_model(config_bert, download=download)
            },
        'faq': {
            'tfidf': train_model(config_tfidf, download=download)
        }
    }
    return qa_models


def format_responses(question, responses):
    formatted_response = f'{question}:\n\n'
    for k, res in enumerate(responses):
        formatted_response += f'{k}: {res}\n'
    return formatted_response


def get_responses(contexts, question, qa_models, nb_squad_results=1):
    responses = []
    for squad_model in qa_models['squad'].values():
        responses.extend(
            select_squad_responses(
                contexts, squad_model, question, best_results=nb_squad_results
            )[1]
        )
    for faq_model in qa_models['faq'].values():
        responses.extend(select_faq_responses(faq_model, question))
    return responses, format_responses(
        question, set([r for r in responses if r.strip()])
    )

# Cell
def get_input(text):
    '''This redundancy is needed for testing'''
    return input(text)


def new_answer(question, data, qa_models):

    if get_input('Give a better anwser [y/n]?')[0].lower() != 'y':
        return 'no data updates..'

    if get_input('Give the answer as a context [y/n]?')[0].lower() == 'y':
        new_context = pd.DataFrame(
            {
                'topic': [get_input('Give context a title:\n')],
                'context': [get_input('Introduce the context:\n')]
            }
        )
        data['context']['df'] = data['context']['df'].append(new_context)
        data['context']['df'].to_csv(data['context']['path'])

        return 'contexts dataset updated..'
    else:
        new_faq = pd.DataFrame(
            {
                'Question': [question],
                'Answer': [get_input('Introduce the answer:\n')]
            }
        )
        data['faq']['df'] = data['faq']['df'].append(new_faq)
        data['faq']['df'].to_csv(data['faq']['path'])
        qa_models['faq']['tfidf'] = train_model(
            data['faq']['config'], download=False
        )
        return 'FAQ dataset and model updated..'


def question_response(data, qa_models, num_returned_values_per_squad_model=1):
    question = get_input('Introduce question:\n')

    _, formatted_responses = get_responses(
        data['context']['df'], question, qa_models, nb_squad_results=2
    )

    return formatted_responses, new_answer(question, data, qa_models)

# Cell
def set_minimal_faq_questions(data):
    if data['df'].shape[0] > 1:
        return
    minimal_questions = [
        'Is this the Intekglobal Dialog System?',
        'What is the purpose of these two automated questions?'
    ]
    minimal_answers = [
        'This is the Intekglobal Dialog System', 'To populate the FAQ data file'
    ]
    minimal_faqs_df = pd.DataFrame(
        {
            'Question': minimal_questions,
            'Answer': minimal_answers
        }
    )
    data['df'] = pd.concat([data['df'], minimal_faqs_df])
    data['df'].to_csv(data['path'], index=False)
    logging.info(f' File created at {data["path"]}')


def set_minimal_contexts(data):
    if data['df'].shape[0] > 0:
        return

    minimal_context_df = pd.DataFrame({'topic': [], 'context': []})
    data['df'] = minimal_context_df
    data['df'].to_csv(data['path'], index=False)

    logging.info(f' File created at {data["path"]}')


def set_data_dict(file, data, question_type, data_dir):

    data['path'] = file if file is not None else path.join(
        data_dir, question_type + '_data.csv'
    )

    data['df'] = pd.read_csv(data['path']) if path.isfile(data['path']
                                                         ) else pd.DataFrame()

    if question_type == 'faq':
        set_minimal_faq_questions(data)
    if question_type == 'context':
        set_minimal_contexts(data)


def load_and_prepare_data(context_data_file, faq_data_file, data, configs_faq):

    PARENT_DIR = popen('dirname $PWD').read().strip()

    if faq_data_file or context_data_file is None:
        DATA_DIR = path.join(PARENT_DIR, 'data')

        if not path.isdir(DATA_DIR):
            mkdir(DATA_DIR)
            logging.info(f'Data directory created at {DATA_DIR}')

    if configs_faq is None:
        configs_faq = path.join(PARENT_DIR, 'config_faq.json')
        copyfile(configs.faq.tfidf_logreg_en_faq, configs_faq)

    data['faq']['config'] = configs_faq

    set_data_dict(
        file=faq_data_file,
        data=data['faq'],
        question_type='faq',
        data_dir=DATA_DIR
    )
    set_data_dict(
        file=context_data_file,
        data=data['context'],
        question_type='context',
        data_dir=DATA_DIR
    )

    updates_faq_config_file(
        configs_path=configs_faq,
        dataset_reader={'data_path': data['faq']['path']}
    )

# Cell
def dialog_system(context_data_file=None, faq_data_file=None, configs_faq=None):
    '''
     Main Dialog System
    '''
    run_shell_installs()
    qa_models = load_qa_models()

    data = {'context': defaultdict(str), 'faq': defaultdict(str)}

    load_and_prepare_data(
        context_data_file=context_data_file,
        faq_data_file=faq_data_file,
        configs_faq=configs_faq,
        data=data
    )

    while True:
        try:
            question_response(data=data, qa_models=qa_models)
        except (KeyboardInterrupt, EOFError, SystemExit):
            logging.debug('Goodbye!')
            return 'Goodbye!'