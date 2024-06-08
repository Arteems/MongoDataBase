from pydantic import BaseModel    



class LanguageInfo(BaseModel):
    rank: int
    name: str
    color: str
    score: int


Languages = dict[str, LanguageInfo]    


class UserStats(BaseModel):
    username: str
    ranks: dict[str, LanguageInfo | Languages]


class User(BaseModel):
    id: int
    username: str    

