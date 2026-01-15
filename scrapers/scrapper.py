from abc import ABC, abstractmethod


from models.filter import Filter
class Scrapper(ABC):
    @abstractmethod
    def scrape():
        pass 
    def set_filter(self,filter):
        self.filter = filter