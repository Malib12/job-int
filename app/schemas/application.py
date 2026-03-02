from pydantic import BaseModel, Field


class ApplicationCreate(BaseModel):
    company: str = Field(min_length=1, max_length=200)
    role: str = Field(min_length=1, max_length=200)
    status: str = Field(min_length=1, max_length=50)


class ApplicationRead(BaseModel):
    id: int
    company: str
    role: str
    status: str

    class Config:
        from_attributes = True