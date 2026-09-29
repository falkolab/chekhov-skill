from shop.pagination import paginate, page_count

ITEMS = list(range(25))


def test_first_page():
    assert paginate(ITEMS, 1) == list(range(10))


def test_last_page():
    assert paginate(ITEMS, 3) == [20, 21, 22, 23, 24]


def test_page_count():
    assert page_count(ITEMS) == 3
