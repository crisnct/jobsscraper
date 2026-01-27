from abc import ABC, abstractmethod
from src.models.filter import Filter

class Scrapper(ABC):
    def __init__(self, filter: Filter):
        self.filter = filter
        
    @abstractmethod
    def scrape():
        pass 
    def set_filter(self,filter):
        self.filter = filter