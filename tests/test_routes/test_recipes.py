import json

from fastapi import status


def test_create_recipe(client, normal_user_token_headers):
    data = {
        "title": "SDE super",
        "company": "doogle",
        "company_url": "www.doogle.com",
        "location": "USA,NY",
        "description": "python",
        "date_posted": "2022-03-20",
    }
    response = client.post(
        "/recipes/create-recipe/", data=json.dumps(data), headers=normal_user_token_headers
    )
    assert response.status_code == 200
    assert response.json()["company"] == "doogle"
    assert response.json()["description"] == "python"


def test_read_recipe(client, normal_user_token_headers):
    data = {
        "title": "SDE super",
        "company": "doogle",
        "company_url": "www.doogle.com",
        "location": "USA,NY",
        "description": "python",
        "date_posted": "2022-03-20",
    }
    response = client.post(
        "/recipes/create-recipe/", json.dumps(data), headers=normal_user_token_headers
    )

    response = client.get("/recipes/get/1/")
    assert response.status_code == 200
    assert response.json()["title"] == "SDE super"


def test_read_recipes(client, normal_user_token_headers):
    data = {
        "title": "SDE super",
        "company": "doogle",
        "company_url": "www.doogle.com",
        "location": "USA,NY",
        "description": "python",
        "date_posted": "2022-03-20",
    }
    client.post(
        "/recipes/create-recipe/", json.dumps(data), headers=normal_user_token_headers
    )
    client.post(
        "/recipes/create-recipe/", json.dumps(data), headers=normal_user_token_headers
    )

    response = client.get("/recipes/all/")
    assert response.status_code == 200
    assert response.json()[0]
    assert response.json()[1]


def test_update_a_recipe(client, normal_user_token_headers):
    data = {
        "title": "New Recipe super",
        "company": "doogle",
        "company_url": "www.doogle.com",
        "location": "USA,NY",
        "description": "fastapi",
        "date_posted": "2022-03-20",
    }
    client.post(
        "/recipes/create-recipe/", json.dumps(data), headers=normal_user_token_headers
    )
    data["title"] = "test new title"
    response = client.put("/recipes/update/1", json.dumps(data))
    assert response.json()["msg"] == "Successfully updated data."


def test_delete_a_recipe(client, normal_user_token_headers):
    data = {
        "title": "New Recipe super",
        "company": "doogle",
        "company_url": "www.doogle.com",
        "location": "USA,NY",
        "description": "fastapi",
        "date_posted": "2022-03-20",
    }
    client.post(
        "/recipes/create-recipe/", json.dumps(data), headers=normal_user_token_headers
    )
    client.delete("/recipes/delete/1", headers=normal_user_token_headers)
    response = client.get("/recipes/get/1/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
