import configparser

config = configparser.RawConfigParser()
config.read(".//configurations/config.ini")

class ReadConfig():
    @staticmethod
    def getApplicationURL(self):
        url = config.get("common info", "BASE_URL")
        return url

