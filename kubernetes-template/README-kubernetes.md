## Kubernetes Deployment

### Build and Push Images
```
docker build -t <your-registry>/rag-backend:latest -f docker/backend.Dockerfile .
docker build -t <your-registry>/rag-frontend:latest -f docker/frontend.Dockerfile .
docker push <your-registry>/rag-backend:latest
docker push <your-registry>/rag-frontend:latest
```

### Apply Kubernetes Manifests
```
kubectl apply -f backend-deployment.yaml
kubectl apply -f backend-service.yaml
kubectl apply -f frontend-deployment.yaml
kubectl apply -f frontend-service.yaml
kubectl apply -f persistent-volume.yaml
kubectl apply -f secrets.yaml
kubectl apply -f ingress.yaml
```

### Verify Deployments
```
kubectl get pods
kubectl get services
kubectl get ingress
```