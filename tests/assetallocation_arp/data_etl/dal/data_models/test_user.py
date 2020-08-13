from assetallocation_arp.data_etl.dal.data_models.app_user import AppUser


def test_user_initialization_sets_email_to_none():
    u = AppUser('a', 'b')
    assert None is u.email
