"""
FastAPI applications.
"""
from typing import Any, Dict, List, Optional, Sequence, Tuple, Type, Union

from fastapi import routing
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.params import Depends


class FastAPI:
    """
    The main FastAPI class.
    """

    def __init__(
        self,
        *,
        debug: bool = False,
        routes: Optional[List[routing.BaseRoute]] = None,
        title: str = "FastAPI",
        description: str = "",
        version: str = "0.1.0",
        openapi_url: Optional[str] = "/openapi.json",
        openapi_tags: Optional[List[Dict[str, Any]]] = None,
        servers: Optional[List[Dict[str, Union[str, Any]]]] = None,
        dependencies: Optional[Sequence[Depends]] = None,
        default_response_class: Type = None,
        docs_url: Optional[str] = "/docs",
        redoc_url: Optional[str] = "/redoc",
        swagger_ui_oauth2_redirect_url: Optional[str] = "/docs/oauth2-redirect",
        swagger_ui_init_oauth: Optional[Dict[str, Any]] = None,
        middleware: Optional[List[Any]] = None,
        exception_handlers: Optional[Dict[Union[int, Type[Exception]], Any]] = None,
        on_startup: Optional[Sequence[Callable]] = None,
        on_shutdown: Optional[Sequence[Callable]] = None,
        **extra: Any,
    ) -> None:
        self.debug: bool = debug
        self.routes: List[routing.BaseRoute] = routes or []
        self.title: str = title
        self.description: str = description
        self.version: str = version
        self.openapi_url: Optional[str] = openapi_url
        self.openapi_tags: Optional[List[Dict[str, Any]]] = openapi_tags
        self.servers: Optional[List[Dict[str, Union[str, Any]]]] = servers
        self.dependencies: List[Depends] = list(dependencies or [])
        self.default_response_class: Type = default_response_class
        self.docs_url: Optional[str] = docs_url
        self.redoc_url: Optional[str] = redoc_url
        self.swagger_ui_oauth2_redirect_url: Optional[str] = swagger_ui_oauth2_redirect_url
        self.swagger_ui_init_oauth: Optional[Dict[str, Any]] = swagger_ui_init_oauth
        self.middleware: List[Any] = list(middleware or [])
        self.exception_handlers: Dict[Union[int, Type[Exception]], Any] = dict(
            exception_handlers or {}
        )
        self.on_startup: List[Callable] = list(on_startup or [])
        self.on_shutdown: List[Callable] = list(on_shutdown or [])
        self.extra: Dict[str, Any] = extra
        self.router: routing.APIRouter = routing.APIRouter(
            routes=self.routes,
            dependency_overrides_provider=self,
            on_startup=self.on_startup,
            on_shutdown=self.on_shutdown,
        )

    def add_route(
        self,
        path: str,
        route: routing.BaseRoute,
    ) -> None:
        self.router.routes.append(route)

    def include_router(
        self,
        router: routing.APIRouter,
        *,
        prefix: str = "",
        tags: Optional[List[str]] = None,
        dependencies: Optional[Sequence[Depends]] = None,
        responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
        default_response_class: Optional[Type] = None,
        callbacks: Optional[List[routing.BaseRoute]] = None,
    ) -> None:
        self.router.include_router(
            router,
            prefix=prefix,
            tags=tags,
            dependencies=dependencies,
            responses=responses,
            default_response_class=default_response_class,
            callbacks=callbacks,
        )

    def openapi(self) -> Dict[str, Any]:
        if not self.openapi_url:
            raise Exception("openapi_url was not set")
        return get_openapi(
            title=self.title,
            version=self.version,
            description=self.description,
            routes=self.routes,
            tags=self.openapi_tags,
            servers=self.servers,
        )

    def docs(self, request: Any) -> Any:
        return get_swagger_ui_html(
            openapi_url=self.openapi_url,
            title=self.title + " - Swagger UI",
            oauth2_redirect_url=self.swagger_ui_oauth2_redirect_url,
            init_oauth=self.swagger_ui_init_oauth,
        )

    def redoc(self, request: Any) -> Any:
        return get_redoc_html(
            openapi_url=self.openapi_url,
            title=self.title + " - ReDoc",
        )
