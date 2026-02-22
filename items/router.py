from fastapi import APIRouter
from items.schemas import ItemCreateRequest, ItemResponse
from config.exceptions import NotFoundException
from items.models import items

router = APIRouter(tags=["Items"])

@router.post("/items/", response_model=ItemResponse)
def create_item(item: ItemCreateRequest):
    item_id = len(items)
    item = ItemResponse(id=item_id, **item.model_dump())
    items.append(item)
    return item

@router.get("/items/", response_model=list[ItemResponse])
def get_all_items():
    return items


def get_item_by_id(item_id: int) -> ItemResponse | None:
    for item in items:
        if item.id == item_id:
            return item
    return None


@router.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int):
    item = get_item_by_id(item_id)
    if not item:
        raise NotFoundException(message=f"Item {item_id} not found")
    else:
        return item

