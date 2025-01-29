from ninja import Router
from .tiles.generate_tile import create_flemish_tile, export_tile

router = Router()

@router.get("/test/")
def test_resources(request):
    return {"message": "Resources app is operational!"}

@router.post("/generate-flemish-tile/")
def generate_flemish_tile(request):
    tile = create_flemish_tile()
    export_tile(tile)
    return {"status": "Flemish bond tile generated and exported successfully."}