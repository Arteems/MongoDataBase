from pydantic import BaseModel


class LanguageInfo(BaseModel):
    rank: int | None
    name: str | None
    color: str | None
    score: int | None


Languages = dict[str, LanguageInfo]


class UserStats(BaseModel):
    username: str
    ranks: dict[str, LanguageInfo | Languages]


class User(BaseModel):
    id: int
    username: str
