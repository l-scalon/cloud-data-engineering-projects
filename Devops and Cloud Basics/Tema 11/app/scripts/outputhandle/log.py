import logging, time

def config():
    logging.basicConfig(format = '%(message)s', level = logging.INFO)

def info(name, size):
    config()
    logging.info('TWITTER API query for: %s', name)
    time.sleep(1)
    logging.info('Results: %s', size)
    time.sleep(1)


def total(results):
    config()
    logging.info('Total: %s', results)