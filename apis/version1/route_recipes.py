from typing import List
from typing import Optional

from apis.version1.route_login import get_current_user_from_token
from db.models.users import User
from db.repository.recipes import create_new_recipe
from db.repository.recipes import delete_recipe_by_id
from db.repository.recipes import list_recipes
from db.repository.recipes import retreive_recipe
from db.repository.recipes import search_recipe
from db.repository.recipes import update_recipe_by_id
from db.session import get_db
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.templating import Jinja2Templates
from schemas.recipes import RecipeCreate
from schemas.recipes import ShowRecipe
from sqlalchemy.orm import Session


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.post("/create-recipe/", response_model=ShowRecipe)
def create_recipe(
    recipe: RecipeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    recipe = create_new_recipe(recipe=recipe, db=db, owner_id=current_user.id)
    return recipe


@router.get(
    "/get/{id}", response_model=ShowRecipe
)  # if we keep just "{id}" . it would stat catching all routes
def read_recipe(id: int, db: Session = Depends(get_db)):
    recipe = retreive_recipe(id=id, db=db)
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recipe with this id {id} does not exist",
        )
    return recipe


@router.get("/all", response_model=List[ShowRecipe])
def read_recipes(db: Session = Depends(get_db)):
    recipes = list_recipes(db=db)
    return recipes


@router.put("/update/{id}")
def update_recipe(id: int, recipe: RecipeCreate, db: Session = Depends(get_db)):
    current_user = 1
    message = update_recipe_by_id(id=id, recipe=recipe, db=db, owner_id=current_user)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Recipe with id {id} not found"
        )
    return {"msg": "Successfully updated data."}


@router.delete("/delete/{id}")
def delete_recipe(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    recipe = retreive_recipe(id=id, db=db)
    if not recipe:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recipe with id {id} does not exist",
        )
    print(recipe.owner_id, current_user.id, current_user.is_superuser)
    if recipe.owner_id == current_user.id or current_user.is_superuser:
        delete_recipe_by_id(id=id, db=db, owner_id=current_user.id)
        return {"detail": "Successfully deleted."}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not permitted!!!!"
    )


@router.get("/autocomplete")
def autocomplete(term: Optional[str] = None, db: Session = Depends(get_db)):
    recipes = search_recipe(term, db=db)
    recipe_titles = []
    for recipe in recipes:
        recipe_titles.append(recipe.title)
    return recipe_titles
