MODELS = {
    "llama3.1": {"name": "llama3.1", "endpoint": "http://localhost:11434/api/generate"}
}


def get_model(model_name):
    if model_name in MODELS:
        return MODELS[model_name]
    else:
        return None
