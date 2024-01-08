CREATE_USER_RESPONSES = {
    204: {"description": "User successfully created"},
    400: {"description": "Username or email already exists"},
}

LOGIN_RESPONSES = {
    200: {"description": "Successfully logged in"},
    401: {"description": "Incorrect username or password"},
}

FETCH_USER_RESPONSES = {
    400: {"description": "Inactive user"},
    401: {"description": "Not authenticated or unable to validate credentials"},
}

CREATE_TODO_RESPONSES = {201: {"description": "Todo successfully created"}}

LIST_TODOS_RESPONSES = {200: {"description": "List of todos created by the user"}}

GET_TODO_RESPONSES = {
    200: {"description": "The returned todo"},
    404: {"description": "Todo not found"},
}

UPDATE_TODO_RESPONSES = {
    204: {"description": "Todo successfully updated"},
    404: {"description": "Todo not found"},
}

DELETE_TODO_RESPONSES = {
    204: {"description": "Todo successfully deleted"},
    404: {"description": "Todo not found"},
}
