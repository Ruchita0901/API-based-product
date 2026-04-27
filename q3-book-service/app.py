from fastapi import FastAPI
from .rest_api import router as rest_router
from .rpc_api import router as rpc_router
from .graphql_api import graphql_app

app = FastAPI(
    title="Book Info Service",
    description="REST, RPC, and GraphQL book APIs sharing the same data store.",
    version="1.0.0",
)

app.include_router(rest_router)
app.include_router(rpc_router)
app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)
