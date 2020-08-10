from assetallocation_arp.data_etl.dal.data_models.user import User


def test_user_initialization_sets_email_to_none():
    u = User('a', 'b')
    assert None is u.email
