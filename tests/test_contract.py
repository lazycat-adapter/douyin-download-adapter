import pathlib
import unittest

import yaml
from PIL import Image


ROOT = pathlib.Path(__file__).resolve().parents[1]


class DouyinContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = yaml.safe_load((ROOT / "lzc-manifest.yml").read_text())
        cls.package = yaml.safe_load((ROOT / "package.yml").read_text())
        cls.action = yaml.safe_load((ROOT / "lazycat-action.yml").read_text())

    def test_package_and_release_source(self):
        self.assertEqual(self.package["package"], "cloud.lazycat.app.download.douyin")
        self.assertGreaterEqual(tuple(map(int, self.package["version"].split("."))), (5, 1, 13))
        self.assertEqual(self.action["source"]["select"]["strategy"], "release")
        self.assertRegex("v5.1.13", self.action["source"]["select"]["tag_regex"])
        self.assertEqual(
            self.action["images"][0]["source"],
            "docker.io/evil0ctal/douyin_tiktok_download_api:{source_version}",
        )

    def test_stack_has_migration_worker_and_persistence(self):
        services = self.manifest["services"]
        self.assertEqual(set(("douyin", "worker", "migrate", "postgres", "redis")), set(services))
        self.assertIn("/lzcapp/var/douyin/media:/var/lib/dtk/media", services["douyin"]["binds"])
        self.assertIn("/lzcapp/var/douyin/postgres:/home/postgres/pgdata/data", services["postgres"]["binds"])
        self.assertIn("/lzcapp/var/douyin/redis:/data", services["redis"]["binds"])
        self.assertEqual(services["douyin"]["command"], ["api"])
        self.assertEqual(services["worker"]["command"], ["worker"])
        self.assertEqual(services["migrate"]["command"], ["migrate"])

    def test_install_secrets_are_parameterized(self):
        params = {item["id"] for item in yaml.safe_load((ROOT / "lzc-deploy-params.yml").read_text())["params"]}
        self.assertEqual(params, {"secret_key", "postgres_password", "redis_password"})
        app_env = "\n".join(self.manifest["services"]["douyin"]["environment"])
        self.assertIn("DTK_SECRET_KEY={{ .U.secret_key }}", app_env)
        self.assertIn("DTK_DATABASE_URL=postgresql+asyncpg://dtk:{{ .U.postgres_password }}@postgres:5432/dtk", app_env)
        self.assertIn("DTK_REDIS_URL=redis://:{{ .U.redis_password }}@redis:6379/0", app_env)

    def test_icon_is_square_and_public_api_path_is_narrow(self):
        image = Image.open(ROOT / "icon.png")
        self.assertEqual(image.size, (512, 512))
        self.assertEqual(self.manifest["application"]["public_path"], ["/api"])


if __name__ == "__main__":
    unittest.main()
