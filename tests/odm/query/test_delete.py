import pytest
from tests.odm.models import Sample
from beanie.odm.queries.delete import DeleteMany


async def test_delete_many(preset_documents):
    count_before = await Sample.count()
    count_find = (
        await Sample.find_many(Sample.integer > 1)
        .find_many(Sample.nested.optional is None)
        .count()
    )

    delete_result = (
        await Sample.find_many(Sample.integer > 1)
        .find_many(Sample.nested.optional is None)
        .delete()
    )

    count_deleted = delete_result.deleted_count
    count_after = await Sample.count()
    assert count_before - count_find == count_after
    assert count_after + count_deleted == count_before
    assert isinstance(
        Sample.find_many(Sample.integer > 1)
        .find_many(Sample.nested.optional is None)
        .delete_many(),
        DeleteMany,
    )


async def test_delete_all(preset_documents):
    count_before = await Sample.count()
    delete_result = await Sample.delete_all()
    count_deleted = delete_result.deleted_count
    count_after = await Sample.count()
    assert count_after == 0
    assert count_after + count_deleted == count_before


async def test_delete_self(preset_documents):
    count_before = await Sample.count()
    result = (
        await Sample.find_many(Sample.integer > 1)
        .find_many(Sample.nested.optional is None)
        .to_list()
    )

    a = result[0]
    delete_result = await a.delete()
    count_deleted = delete_result.deleted_count
    count_after = await Sample.count()
    assert count_before == count_after + 1
    assert count_deleted == 1


async def test_delete_one(preset_documents):
    count_before = await Sample.count()
    delete_result = (
        await Sample.find_one(Sample.integer > 1)
        .find_one(Sample.nested.optional is None)
        .delete()
    )

    count_after = await Sample.count()
    count_deleted = delete_result.deleted_count
    assert count_before == count_after + 1
    assert count_deleted == 1

    count_before = await Sample.count()
    delete_result = (
        await Sample.find_one(Sample.integer > 1)
        .find_one(Sample.nested.optional is None)
        .delete_one()
    )

    count_deleted = delete_result.deleted_count
    count_after = await Sample.count()
    assert count_before == count_after + 1
    assert count_deleted == 1


async def test_delete_many_with_session(preset_documents, session):
    count_before = await Sample.count()
    count_find = (
        await Sample.find_many(Sample.integer > 1)
        .find_many(Sample.nested.optional is None)
        .count()
    )

    q = (
        Sample.find_many(Sample.integer > 1)
        .find_many(Sample.nested.optional is None)
        .delete(session=session)
    )

    assert q.session == session

    q = (
        Sample.find_many(Sample.integer > 1)
        .find_many(Sample.nested.optional is None)
        .delete()
        .set_session(session=session)
    )

    assert q.session == session

    delete_result = await q
    count_deleted = delete_result.deleted_count
    count_after = await Sample.count()
    assert count_before - count_find == count_after
    assert count_after + count_deleted == count_before


async def test_delete_pymongo_kwargs(preset_documents):
    with pytest.raises(TypeError):
        await Sample.find_many(Sample.increment > 4).delete(wrong="integer_1")

    delete_result = await Sample.find_many(Sample.increment > 4).delete(
        hint="integer_1"
    )
    assert delete_result is not None

    delete_result = await Sample.find_one(Sample.increment > 4).delete(
        hint="integer_1"
    )
    assert delete_result is not None
