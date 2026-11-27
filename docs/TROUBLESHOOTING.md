# Troubleshooting and evidence log

The table gives likely causes and checks. These are not a record of incidents: no GitHub Actions workflow, GHCR push, or EC2 deployment has been run for this project yet.

## Common failure patterns

| Stage | Symptom | Likely cause | How to investigate / fix |
| --- | --- | --- | --- |
| Unit test | pytest assertion fails | Route behavior and expected response differ | Read the failing assertion; run `python -m pytest -q` locally and correct the implementation or expected contract |
| Build | Docker cannot find a copied file | Build context or `COPY` path is wrong | Build from the repository root; verify file spelling and `.dockerignore` rules |
| GHCR push | `denied` or `unauthorized` | Package permission or image name is wrong | Confirm `packages: write`, the `GITHUB_TOKEN` login, and the SHA-tagged image name |
| GHCR pull | `pull access denied` on EC2 | Package is private or host has no registry credentials | Make the package public or configure a narrowly scoped read credential on the host |
| SSH | `ssh: no key found` | Key secret is truncated, malformed, or contains the wrong key | Replace the secret with the complete private key, including its header and footer; never use the public key as the secret |
| SSH | Connection timeout/refused | Host, user, SSH service, or network ingress is wrong | Check `EC2_HOST`, `EC2_USER`, server SSH status, and ingress policy without exposing SSH broadly by default |
| Container start | `port is already allocated` | Port 80 is already occupied | Inspect server port usage and stop or reconfigure the conflicting service |
| Deploy health check | `/health` does not become healthy | App failed to start, wrong port mapping, or health route is unavailable | Inspect `docker logs app` on the host; workflow attempts to restart the prior image if one exists |
| Deploy skipped | PR does not deploy | Expected: deploy is restricted to pushes on `main` | Merge after required checks; do not remove the deployment guard just to test a PR |

## Failure drills

Use a disposable branch and make one change at a time. A local failing test or intentionally bad Dockerfile can demonstrate diagnosis without changing a live server. Do not run a broken health check against production. Record only what you actually observe; do not infer that rollback worked from reading the workflow.

## Run evidence

Add an entry after a real run or local drill. Keep logs free of secrets.

| Date | Run URL or local command | Observed symptom | Root cause | Fix and prevention |
| --- | --- | --- | --- | --- |
| _No runs recorded yet._ | — | — | — | — |
