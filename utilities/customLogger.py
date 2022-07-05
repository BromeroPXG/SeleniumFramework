import logging


class logGen:
    @staticmethod
    def loggen():
        logging.basicConfig(filename='C:/Users/bromero/PycharmProjects/SeleniumFramework/Logs/automation.log',
                            format='%(asctime)s: %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        return logger
