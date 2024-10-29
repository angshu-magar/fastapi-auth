from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from app.core.config import EXCLUDED_PATHS
from app.core.security import decode_token
from app.models.permissionModel import PermissionModel
from app.models.userModel import UserModel
from app.models.resourceModel import ResourceModel
from app.models.roleModel import RoleModel
from app.db.session import get_db

class RBACMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        method_mapping = {
            'POST' : 1,
            'GET' : 2,
            'PUT' : 3,
            'DELETE' : 4
        }

        db = next(get_db())

        token = request.headers.get("Authorization")

        resource_name = request.url.path[1:]
        forbiddenResponse = JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"message" : "Forbidden by middleware"})

        if resource_name in EXCLUDED_PATHS:
            return await call_next(request)

        if not token:
            return forbiddenResponse

        perm_index = method_mapping[request.method.upper()]
        token = token.split(" ")[1]

        try:
            userInfo = decode_token(token)
        except:
            return forbiddenResponse

        role_data = db.query(
            UserModel.id,
            RoleModel.label,
            PermissionModel.permission,
            ResourceModel.resourceName
        ).\
            join(RoleModel, UserModel.role_id == RoleModel.id).\
            join(PermissionModel, RoleModel.id == PermissionModel.role_id).\
            join(ResourceModel, PermissionModel.resource_id == ResourceModel.id).\
            filter(
                UserModel.id == userInfo.get("user_id"),
                ResourceModel.resourceName == resource_name,
                PermissionModel.permission[perm_index] == 1
            ).all()

        if not role_data:
            return forbiddenResponse

        return await call_next(request)
