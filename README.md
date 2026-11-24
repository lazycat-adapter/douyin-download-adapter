# Douyin Download API LazyCat adapter

This repository packages stable releases of [Douyin_TikTok_Download_API](https://github.com/Evil0ctal/Douyin_TikTok_Download_API) for the official LazyCat application store.

- Stable GitHub release tags select the matching published application image.
- The API, worker, and migration services share the upstream application image.
- PostgreSQL and Redis are included as pinned runtime services in the application stack.
- Application data, media, PostgreSQL, Redis, and backups persist under `/lzcapp/var/douyin`.
- Installation generates the master key and database passwords. Keep all three parameters unchanged across upgrades.

Pushes and scheduled runs check only. Start a manual run with `dry-run` unchecked for image copy, LPK packaging, and review submission.
