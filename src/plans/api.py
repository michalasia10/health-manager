from ninja.router import Router

router = Router(tags=['sth'])

@router.get('/')
def hello():
    return {'hello':1}