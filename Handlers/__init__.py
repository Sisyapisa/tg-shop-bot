from Handlers.start import router as start_router
from Handlers.info import router as info_router
from Handlers.Catalog import router as catalog_router
from Handlers.profile import router as profile_router
from Handlers.admin import router as admin_router

def register_router(dispatcher):
    dispatcher.include_router(start_router)
    dispatcher.include_router(info_router)
    dispatcher.include_router(catalog_router)
    dispatcher.include_router(profile_router)
    dispatcher.include_router(admin_router)