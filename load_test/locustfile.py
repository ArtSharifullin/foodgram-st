from locust import HttpUser, task


class FoodgramUser(HttpUser):
    def on_start(self):
        self.client.verify = False

    @task
    def recipes_list(self):
        self.client.get("/api/recipes/")