from fastapi.testclient import TestClient
from pyxor.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"alive": "true"}

def test_extract_yaml_string():

    response = client.post(
        "api/yaml_extract",
        json={
            "text": '''root:
    child1:
        list:
            - element1
            - element2
        listOfdicts:
            - key1: element1
              key2: element2
    child2:
        child2t: "text"''',
            "expr": "root.child2.child2t"
        }
    )
    assert response.json() == {"data": 'text'}
    assert response.status_code == 200

def test_extract_yaml_list_element():

    response = client.post(
        "api/yaml_extract",
        json={
            "text": '''root:
    child1:
        list:
            - element1
            - element2
        listOfdicts:
            - key1: element1
              key2: element2
    child2:
        child2t: "text"''',
            "expr": "root.child1.list[0]"
        }
    )
    assert response.json() == {"data": 'element1'}
    assert response.status_code == 200
    
def test_extract_yaml_list():

    response = client.post(
        "api/yaml_extract",
        json={
            "text": '''root:
    child1:
        list:
            - element1
            - element2
        listOfdicts:
            - key1: element1
              key2: element2
    child2:
        child2t: "text"''',
            "expr": "root.child1.list"
        }
    )
    assert response.json() == {"data": ['element1', 'element2']}
    assert response.status_code == 200

def test_extract_yaml_key_from_list_of_dicts():

    response = client.post(
        "api/yaml_extract",
        json={
            "text": '''root:
    child1:
        list:
            - element1
            - element2
        listOfdicts:
            - key1: element1
              key2: element2
    child2:
        child2t: "text"''',
            "expr": "root.child1.listOfdicts[0].key1"
        }
    )
    assert response.json() == {"data": 'element1'}
    assert response.status_code == 200

def test_extract_yaml_key():

    response = client.post(
        "api/yaml_extract",
        json={
            "text": '''root:
    child1:
        list:
            - element1
            - element2
        listOfdicts:
            - key1: element1
              key2: element2
    child2:
        child2t: "text"''',
            "expr": "root.child2"
        }
    )
    assert response.json() == {"data": {"child2t": "text"}}
    assert response.status_code == 200