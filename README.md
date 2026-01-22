# FastAPI TODO App on Kubernetes

This project contains a production-grade FastAPI application containerized with Docker and ready for deployment on Kubernetes.

## Prerequisites
- Docker
- Kubectl
- A Kubernetes cluster (Minikube, Kind, Docker Desktop, or Cloud-based)

## Deployment Steps

1. **Build the Docker Image**
   ```bash
   docker build -t todo-api:latest .
   ```
   *Note: If using Minikube, run `eval $(minikube docker-env)` before building to build directly into the Minikube registry.*

2. **Apply Kubernetes Manifests**
   ```bash
   kubectl apply -f k8s/namespace.yaml
   kubectl apply -f k8s/deployment.yaml
   kubectl apply -f k8s/service.yaml
   kubectl apply -f k8s/hpa.yaml
   ```

3. **Verify Deployment**
   - Check pods: `kubectl get pods -n todo-app`
   - Check service: `kubectl get svc -n todo-app`
   - Check HPA: `kubectl get hpa -n todo-app`

## Testing the API

### Accessing the API
- **Local (Minikube):** `minikube service todo-service -n todo-app --url`
- **Cloud/Docker Desktop:** Use the External IP from `kubectl get svc -n todo-app`.

### CRUD Operations
- **Swagger UI:** Open `http://<API_URL>/docs` in your browser.
- **Health Check:** `curl http://<API_URL>/health`
- **Create Todo:**
  ```bash
  curl -X POST "http://<API_URL>/todos" -H "Content-Type: application/json" -d '{"title": "Test Todo", "description": "This is a test"}'
  ```
- **List Todos:** `curl http://<API_URL>/todos`

## Troubleshooting
- **Logs:** `kubectl logs -l app=todo-api -n todo-app`
- **Describe Pod:** `kubectl describe pod <pod-name> -n todo-app`

## For BG Run
nohup kubectl port-forward svc/todo-service 8080:80 -n todo-app > pf.log 2>&1 &

## To Stop BG Run
ps aux | grep "kubectl port-forward"
kill <PID>