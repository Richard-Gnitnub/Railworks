from ninja import Router

router = Router()

@router.get("/test/")
def test_resources(request):
    return {"message": "Resources app is operational!"}
