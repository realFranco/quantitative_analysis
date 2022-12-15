from enum import Enum


class ArchimateValidConcepts(str, Enum):
    BusinessRole: str = 'BusinessRole'
    Strategy: str = 'Strategy'
    BusinessService: str = 'BusinessService'
    Application: str = 'Application'
    Technology: str = 'Technology'
    Motivation: str = 'Motivation'
    Implementation: str = 'Implementation'
    Other: str = 'Other'
    Relations: str = 'Relations'
    Views: str = 'Views'

    @classmethod
    def has_value(cls, value: str) -> bool:
        if not value:
            return False
        return value in cls._value2member_map_ 
