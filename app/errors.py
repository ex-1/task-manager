from fastapi import HTTPException


def get_error_task_auth_for_update():
    return HTTPException(status_code=403, detail="Not authorized to update this task")


def get_error_task_not_found():
    return HTTPException(status_code=403, detail="Task not found")


def get_error_auth_for_update():
    return HTTPException(status_code=403, detail="Not authorized to update this project")


def get_error_project_not_found() -> HTTPException:
    return HTTPException(status_code=404, detail="Project not found")


def get_error_user_in_db() -> HTTPException:
    return HTTPException(status_code=401, detail="User actually created")


def get_error_user_not_create() -> HTTPException:
    return HTTPException(status_code=401, detail="Same User data in service")


def get_error_user_not_authenticate() -> HTTPException:
    return HTTPException(status_code=401, detail="Login User failed")


def get_404_user_not_found() -> HTTPException:
    return HTTPException(status_code=404, detail="User not found")


def get_error_not_valid() -> HTTPException:
    return HTTPException(status_code=401, detail="Not Valid input")

