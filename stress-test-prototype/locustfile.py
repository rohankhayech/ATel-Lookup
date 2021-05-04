from locust import HttpUser, between, task


class WebsiteUser(HttpUser):
    @task
    def index(self):
        self.client.get("/")
