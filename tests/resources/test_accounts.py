import uuid
import pytest
from speckle.SpeckleClient import SpeckleApiClient


# EMAIL_UUID = str(uuid.uuid4())

@pytest.fixture(scope='module')
def account():
    return {
        'name': 'Test_1',
        'surname': 'McTestyFace_1',
        'company': 'Test Inc_1',
        # Can't delete users on TearDown so have to create new on each time for local development
        'email': '{}@test_1.com'.format(str(uuid.uuid4())),
        'password': 'supersecretpassword'
    }


@pytest.fixture()
def new_profile_payload():
    return {
        'name': 'name_test',
        'surname': 'surname_test',
        'company': 'company_test',
        'role': 'not-a-user'
    }


@pytest.fixture(scope='module')
def created_item(host, transfer_protocol):
    client = SpeckleApiClient(
            host=host, transfer_protocol=transfer_protocol)
    account = {
        'name': 'Test_1',
        'surname': 'McTestyFace_1',
        'company': 'Test Inc_1',
        # Can't delete users on TearDown so have to create new on each time for local development
        'email': '{}@test_1.com'.format(str(uuid.uuid4())),
        'password': 'supersecretpassword'
    }
    client.register(**account)
    return client.me

@pytest.fixture
def get_user(host, transfer_protocol, created_item):
    def get_me():
        client = SpeckleApiClient(
            host=host, transfer_protocol=transfer_protocol)
        client.login(email=created_item['email'], password='supersecretpassword')
        return client.me
    return get_me


def test_register(host, transfer_protocol, account):
    test_client = SpeckleApiClient(host=host, transfer_protocol=transfer_protocol)
    assert test_client.me == None
    test_client.register(**account)
    assert test_client.me['email'] == account['email']
    assert test_client.me['apitoken'] is not None
    assert test_client.me['token'] is not None


@pytest.mark.dependency(depends=['test_register'])
def test_login(host, transfer_protocol, account):
    client = SpeckleApiClient(host=host, transfer_protocol=transfer_protocol)
    assert client.me == None
    client.login(email=account['email'], password=account['password'])
    assert client.me['email'] == account['email']
    assert client.me['apitoken'] is not None
    assert client.me['token'] is not None


@pytest.mark.dependency(depends=['test_login'])
def test_list(host, transfer_protocol, account):
    client = SpeckleApiClient(host=host, transfer_protocol=transfer_protocol)
    client.login(email=account['email'], password=account['password'])
    try:
        client.accounts.list()
    except AssertionError as e:
        assert str(e) == 'method list not supported for accounts calls'


@pytest.mark.dependency(depends=['test_login'])
def test_create(host, transfer_protocol, account):
    client = SpeckleApiClient(host=host, transfer_protocol=transfer_protocol)
    client.login(email=account['email'], password=account['password'])
    try:
        client.accounts.create(data=account)
    except AssertionError as e:
        assert str(e) == 'method create not supported for accounts calls'


@pytest.mark.dependency(depends=['test_login'])
def test_delete(host, transfer_protocol, account):
    client = SpeckleApiClient(host=host, transfer_protocol=transfer_protocol)
    client.login(email=account['email'], password=account['password'])
    try:
        client.accounts.delete(id='some-made-up-id')
    except AssertionError as e:
        assert str(e) == 'method delete not supported for accounts calls'


def test_get(client, created_item):
    account = client.accounts.get(created_item['_id'])

    assert account['_id'] == created_item['_id']


@pytest.mark.dependency(depends=['test_login'])
def test_get_profile(host, transfer_protocol, account):
    client = SpeckleApiClient(host=host, transfer_protocol=transfer_protocol)
    assert client.me == None
    client.login(email=account['email'], password=account['password'])
    profile = client.accounts.get_profile()

    assert profile['email'] == account['email']
    assert profile['name'] == account['name']
    assert profile['surname'] == account['surname']
    assert profile['company'] == account['company']
    assert profile['private'] == True
    assert profile['role'] == 'admin'
    assert profile['_id'] is not None


@pytest.mark.dependency(depends=['test_get_profile'])
def test_update_profile(host, transfer_protocol, account, new_profile_payload):
    client = SpeckleApiClient(host=host, transfer_protocol=transfer_protocol)
    assert client.me == None
    client.login(email=account['email'], password=account['password'])
    
    client.accounts.update_profile(new_profile_payload)
    profile = client.accounts.get_profile()

    assert profile['name'] != account['name']
    assert profile['surname'] != account['surname']
    assert profile['company'] != account['company']

    assert profile['name'] == new_profile_payload['name']
    assert profile['surname'] == new_profile_payload['surname']
    assert profile['company'] == new_profile_payload['company']

    assert profile['role'] == 'admin'
    assert profile['role'] != new_profile_payload['role']


@pytest.mark.dependency(depends=['test_get'])
def test_set_role(client, get_user):
    # account = get_user()
    # assert client.accounts.get_profile() == {}
    # assert account['role'] == 'user'

    # client.accounts.set_role(account['_id'], 'admin')
    # account = get_user()
    # assert account['role'] == 'admin'

    # client.accounts.set_role(account['_id'], 'user')
    # account = get_user()
    # assert account['role'] == 'user'
    # TODO(): Fix this mess...
    pass


