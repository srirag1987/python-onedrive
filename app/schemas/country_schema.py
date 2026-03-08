from pydantic import BaseModel


class CountryCreate(BaseModel):
    country_name: str


class CountryResponse(BaseModel):
    id: int
    country_name: str

    class Config:
        from_attributes = True