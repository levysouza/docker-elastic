from fastapi import APIRouter
from apis.v1 import router_search


api_router = APIRouter()

api_router.include_router(router_search.router, prefix='/tjpe')