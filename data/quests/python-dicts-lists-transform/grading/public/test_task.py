from task import transform_inventory

def test_transform_inventory():
    data = [
        {'category': 'fruit', 'qty': 10},
        {'category': 'veg', 'qty': 5},
        {'category': 'fruit', 'qty': 2}
    ]
    res = transform_inventory(data)
    assert res['fruit'] == 12
    assert res['veg'] == 5
    assert len(res) == 2

def test_empty():
    assert transform_inventory([]) == {}
