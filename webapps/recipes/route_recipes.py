from typing import Optional

from apis.version1.route_login import get_current_user_from_token
from db.models.users import User
from db.repository.recipes import create_new_recipe
from db.repository.recipes import list_recipes
from db.repository.recipes import retreive_recipe
from db.repository.recipes import search_recipe
from db.session import get_db
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from fastapi import responses
from fastapi import status
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.templating import Jinja2Templates
from schemas.recipes import RecipeCreate
from sqlalchemy.orm import Session
from webapps.recipes.forms import RecipeCreateForm


templates = Jinja2Templates(directory="templates")
router = APIRouter(include_in_schema=False)


@router.get("/")
async def home(request: Request, db: Session = Depends(get_db), msg: str = None):
    recipes = list_recipes(db=db)
    return templates.TemplateResponse(
        "general_pages/homepage.html", {"request": request, "recipes": recipes, "msg": msg}
    )


@router.get("/details/{id}")
def recipe_detail(id: int, request: Request, db: Session = Depends(get_db)):
    recipe = retreive_recipe(id=id, db=db)
    return templates.TemplateResponse(
        "recipes/detail.html", {"request": request, "recipe": recipe}
    )


@router.get("/post-a-recipe/")
def create_recipe(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("recipes/create_recipe.html", {"request": request})


@router.post("/post-a-recipe/")
async def create_recipe(request: Request, db: Session = Depends(get_db)):
    form = RecipeCreateForm(request)
    await form.load_data()
    if form.is_valid():
        try:
            token = request.cookies.get("access_token")
            scheme, param = get_authorization_scheme_param(
                token
            )  # scheme will hold "Bearer" and param will hold actual token value
            current_user: User = get_current_user_from_token(token=param, db=db)
            recipe = RecipeCreate(**form.__dict__)
            recipe = create_new_recipe(recipe=recipe, db=db, owner_id=current_user.id)
            return responses.RedirectResponse(
                f"/details/{recipe.id}", status_code=status.HTTP_302_FOUND
            )
        except Exception as e:
            print(e)
            form.__dict__.get("errors").append(
                "You might not be logged in, In case problem persists please contact us."
            )
            return templates.TemplateResponse("recipes/create_recipe.html", form.__dict__)
    return templates.TemplateResponse("recipes/create_recipe.html", form.__dict__)


@router.get("/delete-recipe/")
def show_recipes_to_delete(request: Request, db: Session = Depends(get_db)):
    recipes = list_recipes(db=db)
    return templates.TemplateResponse(
        "recipes/show_recipes_to_delete.html", {"request": request, "recipes": recipes}
    )


@router.get("/search/")
def search(
    request: Request, db: Session = Depends(get_db), query: Optional[str] = None
):
    recipes = search_recipe(query, db=db)
    return templates.TemplateResponse(
        "general_pages/homepage.html", {"request": request, "recipes": recipes}
    )
