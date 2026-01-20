from app.auth.roles import ROLE_PERMISSIONS


def has_permission(role: str, permission: str) -> bool:
    return permission in ROLE_PERMISSIONS.get(role, set())
