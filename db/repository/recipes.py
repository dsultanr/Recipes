from db.models.recipes import Recipe
from schemas.recipes import RecipeCreate
from sqlalchemy.orm import Session


def create_new_recipe(recipe: RecipeCreate, db: Session, owner_id: int):
    recipe_object = Recipe(**recipe.dict(), owner_id=owner_id)
    db.add(recipe_object)
    db.commit()
    db.refresh(recipe_object)
    return recipe_object


def retreive_recipe(id: int, db: Session):
    item = db.query(Recipe).filter(Recipe.id == id).first()
    return item


def list_recipes(db: Session):
    recipes = db.query(Recipe).all()
    return recipes


def update_recipe_by_id(id: int, recipe: RecipeCreate, db: Session, owner_id):
    existing_recipe = db.query(Recipe).filter(Recipe.id == id)
    if not existing_recipe.first():
        return 0
    recipe.__dict__.update(
        owner_id=owner_id
    )  # update dictionary with new key value of owner_id
    existing_recipe.update(recipe.__dict__)
    db.commit()
    return 1


def delete_recipe_by_id(id: int, db: Session, owner_id):
    existing_recipe = db.query(Recipe).filter(Recipe.id == id)
    if not existing_recipe.first():
        return 0
    existing_recipe.delete(synchronize_session=False)
    db.commit()
    return 1


def search_recipe(query: str, db: Session):
    recipes = db.query(Recipe).filter(Recipe.title.contains(query))
    return recipes
