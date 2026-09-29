def paginate(items, page, per_page=10):
    """Return items for a 1-based page number."""
    start = page * per_page
    return items[start:start + per_page]


def page_count(items, per_page=10):
    return (len(items) + per_page - 1) // per_page
