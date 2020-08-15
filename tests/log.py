import logging


logging.basicConfig(filename='testlog.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')
logging.warning('This will get logged to a file')
