# Troubleshooting and evidence log

The table gives likely causes and checks. Two failed GitHub Actions runs are recorded below. No EC2 host was configured, and the SSH action stopped before connecting to a server.

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
| Deploy skipped | Push or PR does not deploy | Expected: deploy requires a manual dispatch from `main` with `deploy` enabled | Leave deployment disabled to avoid EC2; enable it only after host secrets and infrastructure are ready |

## Observed run

On 2026-11-27, runs [46015721772](https://github.com/SAMSAROHA/CI-CD-Pipeline-For-Containerized-App-Deployment/actions/runs/46015721772) and [46017226240](https://github.com/SAMSAROHA/CI-CD-Pipeline-For-Containerized-App-Deployment/actions/runs/46017226240) both failed at the deploy step with `Error: missing server host`. `EC2_HOST` was absent, so the SSH action could not start a connection. Neither run reached an EC2 host. The workflow now skips deploy on pushes and requires a manual dispatch with `deploy` enabled; it also checks all three secrets before starting SSH.

## Failure drills

Use a disposable branch and make one change at a time. A local failing test or intentionally bad Dockerfile can demonstrate diagnosis without changing a live server. Do not run a broken health check against production. Record only what you actually observe; do not infer that rollback worked from reading the workflow.

## Run evidence

Add an entry after a real run or local drill. Keep logs free of secrets.

| Date | Run URL or local command | Observed symptom | Root cause | Fix and prevention |
| --- | --- | --- | --- | --- |
| 2026-11-27 | [Actions run 46015721772](https://github.com/SAMSAROHA/CI-CD-Pipeline-For-Containerized-App-Deployment/actions/runs/46015721772), [run 46017226240](https://github.com/SAMSAROHA/CI-CD-Pipeline-For-Containerized-App-Deployment/actions/runs/46017226240) | `Error: missing server host` | `EC2_HOST` was not configured; there is no deployment host in this project setup | Make deployment manual and opt-in; validate required secrets before SSH. Configure a real host only if deployment is intentionally enabled. |
