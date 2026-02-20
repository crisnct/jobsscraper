from pydantic import BaseModel
from src.common.types.filter_options import FilterOptions
from src.common.types.scraper_options import ScrapperOptions


class AppRequest(BaseModel):
    scrapper:ScrapperOptions
    filter:FilterOptions