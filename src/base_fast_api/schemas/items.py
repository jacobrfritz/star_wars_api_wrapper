from pydantic import BaseModel, ConfigDict, Field


class ItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, examples=["Spanner"])
    description: str | None = Field(None, max_length=500, examples=["A useful tool"])
    price: float = Field(..., gt=0.0, examples=[12.99])
    tax: float | None = Field(None, ge=0.0, examples=[1.50])


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100, examples=["Wrench"])
    description: str | None = Field(None, max_length=500)
    price: float | None = Field(None, gt=0.0)
    tax: float | None = Field(None, ge=0.0)


class ItemResponse(ItemBase):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(..., examples=[1])
