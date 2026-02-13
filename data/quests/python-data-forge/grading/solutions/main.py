def forge_data(users):
    return {u['id']: u['name'] for u in users if u.get('active')}