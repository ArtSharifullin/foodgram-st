from locust import HttpUser, between, tag, task


class FoodgramUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        self.client.verify = False

    @tag("nginx")
    @task(3)
    def nginx_root(self):
        self.client.get("/recipes", name="nginx:/")

    @tag("api")
    @task(5)
    def recipes_list(self):
        self.client.get("/api/recipes/", name="api:/api/recipes/")

    @tag("api")
    @task(2)
    def ingredients_search(self):
        self.client.get(
            "/api/ingredients/?name=%D1%81%D0%B0%D1%85",
            name="api:/api/ingredients/",
        )

    @tag("api")
    @task(1)
    def recipe_card(self):
        self.client.get("/api/recipes/1/", name="api:/api/recipes/:id")

    @tag("celery")
    @task(1)
    def celery_enqueue(self):
        self.client.post(
            "/internal/run_external_fetch/",
            json={"alias": "news", "params": {}},
            name="celery:/internal/run_external_fetch/",
        )

    @tag("celery")
    @task(1)
    def celery_batch_enqueue(self):
        self.client.post(
            "/internal/run_external_batch/",
            json={"messages": [{"alias": "news", "params": {}}]},
            name="celery:/internal/run_external_batch/",
        )

    @tag("flower")
    @task(1)
    def flower_ui(self):
        self.client.get("/flower", name="flower:/flower")
