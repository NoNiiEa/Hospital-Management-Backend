def individual_schema(todo):
    return {
        "id" : str(todo["_id"]),
        "title" : todo["title"],
        "description" : todo["description"],
        "completed" : todo["completed"]
    }

def list_schema(todos):
    return [individual_schema(todo) for todo in todos]