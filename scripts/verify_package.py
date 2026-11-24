from pathlib import Path

import yaml


root = Path(__file__).resolve().parents[1]
manifest = yaml.safe_load((root / "lzc-manifest.yml").read_text())
package = yaml.safe_load((root / "package.yml").read_text())
assert package["package"] == "cloud.lazycat.app.download.douyin"
assert set(manifest["services"]) == {"douyin", "worker", "migrate", "postgres", "redis"}
assert manifest["application"]["public_path"] == ["/api"]
print("Douyin adapter contract passed")
