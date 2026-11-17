import pytest
from backend import create_app


@pytest.fixture(name='client')
def create_client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as current_client:
        yield current_client


def test_get_animals(client):
    response = client.get('/api/animals')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)


def test_get_animal_not_found(client):
    response = client.get('/api/animals/unknown')
    assert response.status_code == 404


def test_add_animal_success(client):
    new_animal = {"name": "Tiger",
                  "species": "Panthera tigris", "habitat": "Forest"}
    response = client.post('/api/animals', json=new_animal)
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Tiger"


def test_add_animal_missing_field(client):
    incomplete_animal = {"name": "Giraffe",
                         "species": "Giraffa camelopardalis"}
    response = client.post('/api/animals', json=incomplete_animal)
    assert response.status_code == 400


def test_get_animals_by_habitat(client):
    response = client.get('/api/animals?habitat=Savannah')

    assert response.status_code == 200

    animals = response.get_json()

    assert len(animals) >= 2

    for animal in animals:
        assert animal['habitat'] == 'Savannah'


def test_get_animals_no_matching_habitat(client):
    response = client.get('/api/animals?habitat=Ocean')

    assert response.status_code == 200
    assert response.get_json() == []


def test_get_animals_without_habitat(client):
    response = client.get('/api/animals')

    assert response.status_code == 200

    animals = response.get_json()

    assert len(animals) >= 2

