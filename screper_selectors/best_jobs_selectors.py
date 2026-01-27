from enum import Enum


class BestJobsSelectors(Enum):
    BASE_URL = "https://www.bestjobs.eu/"
    LOCATION_SEARCH = "locuri-de-munca-in-"
    JOB_URL = "a[href].absolute.inset-0.z-1"
    COMPANY_NAME = "div.mt-2.line-clamp-1.w-full.text-sm.text-ink-medium"
    PAYMENT = "div.ml-2 span.text-base.font-bold"
    EXPERIENCE = "div.ml-2 a.hover\\:text-ink"
    WORK_TYPE = "div.flex-1 span.font-bold"
    