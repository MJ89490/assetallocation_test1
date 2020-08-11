import mock

from pytest import fixture, raises

from assetallocation_arp.data_etl.dal.db import Db


@fixture(autouse=True)
def mock_engine():
    with mock.patch('assetallocation_arp.data_etl.dal.db.create_engine') as _mock_engine:
        yield _mock_engine


def test_call_proc_invalid_proc_name_raises_value_error():
    d = Db('a')

    with raises(ValueError):
        d.call_proc('invalid_proc_name', [])



def test_call_proc_returns_data_as_dict(mock_engine):
    with mock.patch.object(Db, 'procs', ['fake_proc']):
        d = Db('a')

        mock_engine.raw_connection().cursor().description = ['a', 'c']
        d.call_proc('fake_proc', [])
