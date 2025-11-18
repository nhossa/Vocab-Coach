from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime

class PartOfSpeech(Enum):
    NOUN = "noun"
    VERB = "verb"
    ADJECTIVE = "adjective"
    ADVERB = "adverb"
    PRONOUN = "pronoun"

class Difficulty(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class UserRegister(BaseModel):
    email: str
    password: str

class WordRequest(BaseModel):
    word: str = Field(min_length=1, max_length=50)

class WordSuggestionRequest(BaseModel):
    part_of_speech: PartOfSpeech
    difficulty: Difficulty  # lowercase field name

class WordDefinition(BaseModel):
    word: str
    formal_definition: str
    simple_definition: str
    example: str


class VocabularySaveRequest(BaseModel):
    user_id: str
    word: str

class WordSuggestion(BaseModel):
    word: str
    part_of_speech: PartOfSpeech  # Use your Enum!
    difficulty: Difficulty         # Use your Enum!
    simple_definition: str
    example: str

class VocabularyItem(BaseModel):
    word: str
    part_of_speech: PartOfSpeech
    saved_at: datetime
    review_count: int = 0

class VocabularyListResponse(BaseModel):
    user_id: str  # ← The connection is here
    words: list[VocabularyItem]  # ← List of items for this user
    total: int
