from dataclasses import dataclass


@dataclass
class ParseInput:
    object_key: str 

@dataclass
class ParseOutput:
    parsed_object_key: str 