from abc import ABC, abstractmethod
from src.common.types.filter_options import FilterOptions




class Scrapper(ABC):
    def __init__(self, filter: FilterOptions):
        self.filter = filter
        
    @abstractmethod
    def scrape():
        pass 
    def set_filter(self,filter):
        self.filter = filter