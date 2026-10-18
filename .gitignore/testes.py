client = OpenAI(
        api_key = os.environ["MODEL_API_KEY"],
        base_url="https://api.meta.ai/v1",
        )