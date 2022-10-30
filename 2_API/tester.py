from urllib import response
import requests

class Tester:

    def __init__(self, url, image_path):
        self.url = url
        self.image_path = image_path

    def post(self):
        files = [("files", open(self.image_path, "rb"))]
        response = requests.post(self.url, files=files)
        return response.content.decode("utf-8")

    def show_output(self, response):
        print(response)

    def test(self):
        response = self.post()
        self.show_output(response)
        


if __name__   == "__main__":
    url = "http://127.0.0.1:8000/save"
    path = "images/0img_78.jpg"
    my_tester = Tester(url, path)
    my_tester.test()