# Troubleshooting and failure drills

The diagnoses below are prepared from the project configuration and common failure modes. These failures have **not** been deliberately triggered in a live GitHub Actions run or on an EC2 server.

| Symptom | Likely root cause | Fix | Prevention |
| --- | --- | --- | --- |
| Unit test job fails | The assertion or application behavior does not match | Fix the route or expected response; keep the test job as a required deploy dependency | Run `python -m pytest -q` before pushing |
| Docker reports it cannot find `requirements.txt` | Incorrect `COPY` source or build context | Correct the path and build from the repository root | Keep the Docker build context explicit (`.`) |
| GHCR reports denied or unauthorized | Package is private, token permissions are insufficient, or the image name/tag is wrong | Check package visibility and `packages: write`/`packages: read`; confirm the repository image name | Keep the package public for unauthenticated EC2 pulls, or add a narrowly scoped registry credential on the server |
| SSH step cannot connect | Missing/wrong host or user secret, network rule blocks SSH, or the key is malformed | Verify `EC2_HOST`, `EC2_USER`, and the full private key value; confirm SSH access on the server | Store secrets in the production environment and use a dedicated deploy key |
| SSH reports `ssh: no key found` | Private key was truncated, reformatted, or pasted without its header/footer | Replace the secret with the complete private key in its original format | Never copy a public key into `EC2_SSH_KEY`; rotate a key if it was exposed |
| Docker reports port 80 is already allocated | Another process/container owns host port 80 | Stop or reconfigure the conflicting service before deployment | Check server port usage and keep only one app container bound to port 80 |
| Deployment health check fails | The new container did not start or `/health` returned a failure | Inspect container logs; the workflow removes the failed container and attempts to restart the prior image | Preserve immutable SHA tags and verify the prior image remains available |
| Deploy job is skipped on a pull request | Expected behavior: deploy is restricted to pushes on `main` | Merge through the protected main branch after required checks pass | Keep the `if` guard and configure branch protection |

To collect real evidence, reproduce one failure at a time on a disposable branch or non-production environment, record the run URL and observed log, then document the actual symptom, cause, fix, and prevention. Do not represent the likely diagnoses above as incidents that have already occurred.
