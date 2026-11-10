
import unittest
from datetime import datetime

from app import create_app
from app.extensions import db
from app.posts.models import Post


class PostsTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def create_post(self):
        return self.client.post(
            "/post/create",
            data={
                "title": "Тестова публікація",
                "content": "Це текст тестової публікації для перевірки.",
                "category": "news",
                "author": "Julianna",
                "is_active": "y",
                "posted": datetime.now().strftime("%Y-%m-%dT%H:%M"),
                "submit": "Зберегти"
            },
            follow_redirects=True
        )

    def test_posts_list(self):
        response = self.client.get("/post/")
        self.assertEqual(response.status_code, 200)

    def test_create_post(self):
        response = self.create_post()
        self.assertEqual(response.status_code, 200)

        with self.app.app_context():
            post = Post.query.filter_by(
                title="Тестова публікація"
            ).first()
            self.assertIsNotNone(post)

    def test_view_post(self):
        self.create_post()

        with self.app.app_context():
            post = Post.query.first()
            post_id = post.id

        response = self.client.get(f"/post/{post_id}")
        self.assertEqual(response.status_code, 200)

    def test_update_post(self):
        self.create_post()

        with self.app.app_context():
            post = Post.query.first()
            post_id = post.id

        response = self.client.post(
            f"/post/{post_id}/update",
            data={
                "title": "Оновлена публікація",
                "content": "Оновлений текст публікації для тесту.",
                "category": "tech",
                "author": "Julianna",
                "is_active": "y",
                "posted": datetime.now().strftime("%Y-%m-%dT%H:%M"),
                "submit": "Зберегти"
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)

        with self.app.app_context():
            post = db.session.get(Post, post_id)
            self.assertEqual(post.title, "Оновлена публікація")

    def test_delete_post(self):
        self.create_post()

        with self.app.app_context():
            post = Post.query.first()
            post_id = post.id

        response = self.client.post(
            f"/post/{post_id}/delete",
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)

        with self.app.app_context():
            post = db.session.get(Post, post_id)
            self.assertIsNone(post)


if __name__ == "__main__":
    unittest.main()
