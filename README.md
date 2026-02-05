# Student Result Management System (Flask + MySQL)

## Local run
1. Copy env file and edit as needed:
   - `cp .env.example .env`
2. Start services:
   - `docker compose up -d --build`
3. Test:
   - `curl http://localhost:8000/`

## API
- `GET /` health
- `GET /results` list results
- `POST /results` create result

Example (local):
```bash
curl http://localhost:8000/
curl -X POST http://localhost:8000/results \
  -H 'Content-Type: application/json' \
  -d '{"student_name":"Asha","subject":"Math","score":95}'
curl http://localhost:8000/results
```

Example (deployed VM):
```bash
# replace with your public IP
curl http://YOUR_VM_IP:8000/
curl http://YOUR_VM_IP:8000/results
```

## Jenkins CI/CD (separate VM)
This repo uses a `Jenkinsfile` pipeline that:
- runs tests
- deploys via SSH to a separate VM
- runs `docker compose up -d --build` on the VM

### Jenkins credentials
Create these credentials in Jenkins:
- `deploy-ssh-key`: SSH private key that can access the VM
- `deploy-host`: Secret text containing the VM hostname or IP
- `deploy-user`: Secret text containing the SSH username

### VM setup
On the deployment VM:
1. Install Docker and Docker Compose plugin
2. Create deploy directory (default in Jenkinsfile):
   - `/opt/student-results`
3. Place `.env` file in that directory (copy from `.env.example` and edit)
4. Ensure the deploy user has permissions to run `docker compose`

### Change deploy path
Edit `DEPLOY_PATH` in `Jenkinsfile` if you want a different location.
