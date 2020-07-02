import argparse
from let_me_answer_for_you.chatbot import ChatBot

parser = argparse.ArgumentParser('Specialized Chatbot that uses context and FAQ technologies')
parser.add_argument('--context_file', type =str, help = 'csv contexts file',default=None)
parser.add_argument('--faq_file', type =str, help = 'csv FAQs file',default=None)
parser.add_argument('--config_file', type =str, help = 'json config faq file',default=None)
parser.add_argument('--download', type =str, help = 'download configuration files',default=None)
args = parser.parse_args()

cb = ChatBot(context_data_file = args.context_file,
 faq_data_file=args.faq_file, 
 configs_faq=args.config_file, 
 download_models= args.download)

cb.chatbot()