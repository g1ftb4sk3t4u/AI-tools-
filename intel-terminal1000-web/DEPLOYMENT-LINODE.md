# Linode Deployment Instructions for intel-terminal1000-web (Frontend)

1. **Upload your project to your Linode server**
   - Use `scp`, `rsync`, or upload via Git.

2. **Install Docker and Docker Compose**
   ```sh
   sudo apt update
   sudo apt install -y docker.io docker-compose
   sudo systemctl enable --now docker
   ```

3. **Build and run the container**
   ```sh
   cd /path/to/intel-terminal1000-web
   sudo docker-compose up --build -d
   ```
   - The frontend will be available on port 8081 (http://your-linode-ip:8081)

4. **(Optional) Set up a domain and HTTPS**
   - Use Linode DNS to point your domain to your server IP.
   - Use a reverse proxy (e.g., Caddy, Nginx, or Traefik) with Let's Encrypt for HTTPS.

5. **Update/Restart**
   ```sh
   sudo docker-compose down
   sudo docker-compose up --build -d
   ```

6. **Logs and troubleshooting**
   ```sh
   sudo docker-compose logs -f
   sudo docker ps
   sudo docker-compose exec frontend sh
   ```

---

**Backend/API**: If you want to connect to a backend API, update `frontend/nginx.conf` to point to your backend's address.

**Support**: For further help, contact your project maintainer.
