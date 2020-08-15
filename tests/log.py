import logging


logging.basicConfig(filemode='a', format='%(name)s - %(levelname)s - %(message)s')
logging.warning('This will get logged to a file')
