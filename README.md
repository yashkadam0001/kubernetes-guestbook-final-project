# IBM Skills Network / Coursera Kubernetes Guestbook Final Project

[![Kubernetes](https://img.shields.io/badge/Kubernetes-v1.28%2B-blue?logo=kubernetes)](https://kubernetes.io/)
[![IBM Cloud](https://img.shields.io/badge/IBM%20Cloud-Container%20Registry-informational?logo=ibm)](https://cloud.ibm.com)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker)](https://www.docker.com/)
[![Nginx](https://img.shields.io/badge/Nginx-Alpine-009639?logo=nginx)](https://nginx.org/)

This repository contains the end-to-end implementation and grading deliverables for the **IBM Skills Network / Coursera Kubernetes Guestbook Final Project** (part of the Cloud Native / DevOps certification series).

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Repository Structure](#repository-structure)
3. [10 Grading Rubric Tasks & Evidence Mapping](#10-grading-rubric-tasks--evidence-mapping)
4. [Step-by-Step Lab Execution Guide](#step-by-step-lab-execution-guide)
   - [Phase 1: Environment Discovery & Registry Setup](#phase-1-environment-discovery--registry-setup)
   - [Phase 2: Build & Push Initial Guestbook (v1)](#phase-2-build--push-initial-guestbook-v1)
   - [Phase 3: Deploy to Kubernetes Cluster](#phase-3-deploy-to-kubernetes-cluster)
   - [Phase 4: Horizontal Pod Autoscaler (HPA) & Load Testing](#phase-4-horizontal-pod-autoscaler-hpa--load-testing)
   - [Phase 5: Update Application to v2 & Rolling Update](#phase-5-update-application-to-v2--rolling-update)
   - [Phase 6: Resource Management & Rollout History](#phase-6-resource-management--rollout-history)
   - [Phase 7: Rollback & ReplicaSet Inspection](#phase-7-rollback--replicaset-inspection)
5. [Automated Execution Script (`run_lab.sh`)](#automated-execution-script-run_labsh)
6. [Local Testing & Verification](#local-testing--verification)

---

## 🚀 Project Overview

The Guestbook application is a lightweight, responsive web application served via Nginx on Alpine Linux. The application lifecycle demonstrates essential Kubernetes operations:
- **Containerization**: Explicit Dockerfile construction using `nginx:alpine` with `COPY` and `EXPOSE 80`.
- **Registry Management**: Tagging and pushing multi-version images (`v1` and `v2`) to IBM Cloud Container Registry (`us.icr.io`).
- **Orchestration**: Declarative Kubernetes Deployments configured with resource requests (`50m` CPU) and limits (`100m` CPU) for dynamic scaling.
- **Autoscaling**: Horizontal Pod Autoscaler (HPA) targeting 50% CPU utilization, dynamically scaling from 1 to 10 replicas under load.
- **Rolling Updates**: Zero-downtime rolling update transition from v1 to v2.
- **Revision History & Rollback**: Auditing rollout revisions across CPU resource updates and executing atomic rollbacks with ReplicaSet verification.

---

## 📂 Repository Structure

```text
kubernetes-guestbook-final-project/
├── .gitignore                      # Git exclusion rules
├── Dockerfile                      # Production container image specification
├── index.html                      # Active application frontend (v1 initial / v2 updated)
├── deployment.yml                  # Kubernetes Deployment manifest with resource specs
├── hpa.yml                         # HorizontalPodAutoscaler and Service declarations
├── README.md                       # Comprehensive project documentation
├── run_lab.sh                      # Turnkey automation script for Coursera / SN Labs environment
├── test_project.py                 # Automated verification test suite
├── answers/
│   └── answers.txt                 # Formatted answers for all 10 grading questions
└── evidence/
    ├── app.html                    # Preserved initial Guestbook v1 source
    ├── up-app.html                 # Preserved updated Guestbook v2 source
    ├── crimages.txt                # Genuine output: ibmcloud cr images (v1)
    ├── deployment.txt              # Genuine output: kubectl apply -f deployment.yml
    ├── hpa.txt                     # Genuine output: kubectl get hpa (initial)
    ├── hpa2.txt                    # Genuine output: kubectl get hpa (scaled under load)
    ├── upguestbook.txt             # Genuine output: docker push v2 with digest
    ├── rev.txt                     # Genuine output: kubectl rollout history (CPU update)
    └── rs.txt                      # Genuine output: kubectl get rs (after rollback)
```

---

## 🎯 10 Grading Rubric Tasks & Evidence Mapping

| Question # | Task Description | Target File / Evidence | Points |
| :---: | :--- | :--- | :---: |
| **Q1** | Dockerfile with explicit `COPY` and `EXPOSE` | `Dockerfile` / `answers/answers.txt` | 1 pt |
| **Q2** | IBM Cloud Container Registry image listing | `evidence/crimages.txt` | 1 pt |
| **Q3** | Initial `index.html` with `<title>Guestbook - v1</title>` & `<h1>` | `evidence/app.html` | 1 pt |
| **Q4** | Initial HPA details table (`NAME`, `REFERENCE`, `TARGETS`, etc.) | `evidence/hpa.txt` | 1 pt |
| **Q5** | Autoscaling evidence showing increased replica count under load | `evidence/hpa2.txt` | 2 pts |
| **Q6** | Docker push output for updated v2 image with final digest | `evidence/upguestbook.txt` | 2 pts |
| **Q7** | Deployment applied / configured output | `evidence/deployment.txt` | 1 pt |
| **Q8** | Updated `index.html` with `<title>Guestbook - v2</title>` & `<h1>` | `evidence/up-app.html` | 2 pts |
| **Q9** | Deployment rollout history showing CPU-related revision details | `evidence/rev.txt` | 2 pts |
| **Q10**| ReplicaSet status after rollback showing replica states | `evidence/rs.txt` | 2 pts |
| **Total**| **All 10 Graded Items** | **`answers/answers.txt`** | **15 pts (100%)** |

---

## 🛠️ Step-by-Step Lab Execution Guide

Follow these steps directly inside the **IBM Skills Network Cloud IDE** terminal:

### Phase 1: Environment Discovery & Registry Setup

1. Check your assigned Container Registry namespace:
   ```bash
   echo $MY_NAMESPACE
   ```
   If empty, retrieve it from the active account:
   ```bash
   export MY_NAMESPACE=$(ibmcloud cr namespaces | grep -v "Listing" | grep -v "Namespace" | head -n 1 | awk '{print $1}')
   echo "Using namespace: $MY_NAMESPACE"
   ```

2. Log in to the IBM Cloud Container Registry:
   ```bash
   ibmcloud cr login
   ```

---

### Phase 2: Build & Push Initial Guestbook (v1)

1. Ensure `index.html` is using the v1 release:
   ```bash
   cp evidence/app.html index.html
   ```

2. Build the Docker container image:
   ```bash
   docker build -t us.icr.io/$MY_NAMESPACE/guestbook:v1 .
   ```

3. Push the v1 image to IBM Cloud Container Registry:
   ```bash
   docker push us.icr.io/$MY_NAMESPACE/guestbook:v1
   ```

4. Verify image in registry and save output (**Question 2**):
   ```bash
   ibmcloud cr images | tee evidence/crimages.txt
   ```

---

### Phase 3: Deploy to Kubernetes Cluster

1. Update `deployment.yml` with your actual namespace:
   ```bash
   sed -i "s|<sn-labs-namespace>|$MY_NAMESPACE|g" deployment.yml
   ```

2. Apply the deployment manifest to your Kubernetes cluster (**Question 7**):
   ```bash
   kubectl apply -f deployment.yml | tee evidence/deployment.txt
   ```

3. Verify pod rollout:
   ```bash
   kubectl rollout status deployment/guestbook
   kubectl get pods -l app=guestbook
   ```

---

### Phase 4: Horizontal Pod Autoscaler (HPA) & Load Testing

1. Apply the service definition to route traffic:
   ```bash
   kubectl apply -f hpa.yml
   ```

2. Create the Horizontal Pod Autoscaler targeting 50% CPU:
   ```bash
   kubectl autoscale deployment guestbook --cpu-percent=50 --min=1 --max=10
   ```

3. Capture the initial HPA table (**Question 4**):
   ```bash
   kubectl get hpa | tee evidence/hpa.txt
   ```

4. Generate synthetic CPU load to trigger autoscaling:
   ```bash
   kubectl run load-generator --image=busybox:latest --restart=Never -- /bin/sh -c "while true; do wget -q -O- http://guestbook:80 > /dev/null 2>&1; done"
   ```

5. Monitor scaling until replicas increase, then capture status (**Question 5**):
   ```bash
   {
     echo "=== Horizontal Pod Autoscaler (Scaled) ==="
     kubectl get hpa
     echo ""
     echo "=== Deployment Status ==="
     kubectl get deployment guestbook
     echo ""
     echo "=== Running Scaled Pods ==="
     kubectl get pods -l app=guestbook
   } | tee evidence/hpa2.txt
   ```

6. Clean up the load generator:
   ```bash
   kubectl delete pod load-generator --ignore-not-found=true
   ```

---

### Phase 5: Update Application to v2 & Rolling Update

1. Switch `index.html` to the v2 release:
   ```bash
   cp evidence/up-app.html index.html
   ```

2. Build and push the v2 image, capturing output with the final digest line (**Question 6**):
   ```bash
   docker build -t us.icr.io/$MY_NAMESPACE/guestbook:v2 .
   docker push us.icr.io/$MY_NAMESPACE/guestbook:v2 2>&1 | tee evidence/upguestbook.txt
   ```

3. Trigger rolling update on Kubernetes:
   ```bash
   kubectl set image deployment/guestbook guestbook=us.icr.io/$MY_NAMESPACE/guestbook:v2 | tee evidence/deployment.txt
   kubectl rollout status deployment/guestbook
   ```

---

### Phase 6: Resource Management & Rollout History

1. Update CPU resource requests and limits:
   ```bash
   kubectl set resources deployment guestbook -c=guestbook --limits=cpu=200m --requests=cpu=100m
   kubectl rollout status deployment/guestbook
   ```

2. Capture rollout history and revision details (**Question 9**):
   ```bash
   REV_NUM=$(kubectl rollout history deployment/guestbook | grep -oE "^[0-9]+" | tail -n 1)
   {
     echo "=== Deployment Rollout History ==="
     kubectl rollout history deployment/guestbook
     echo ""
     echo "=== Detailed Revision Info (Revision ${REV_NUM}) ==="
     kubectl rollout history deployment/guestbook --revision=${REV_NUM}
   } | tee evidence/rev.txt
   ```

---

### Phase 7: Rollback & ReplicaSet Inspection

1. Roll back the deployment to the previous revision:
   ```bash
   kubectl rollout undo deployment/guestbook
   kubectl rollout status deployment/guestbook
   ```

2. Inspect all ReplicaSets showing desired, current, and ready pods (**Question 10**):
   ```bash
   kubectl get rs | tee evidence/rs.txt
   ```

---

## ⚡ Automated Execution Script (`run_lab.sh`)

To execute all phases sequentially and populate `evidence/` and `answers/answers.txt` in a single run inside the Skills Network Lab terminal:

```bash
chmod +x run_lab.sh
./run_lab.sh
```

---

## 🧪 Local Testing & Verification

Run the Python verification test suite locally:

```bash
python test_project.py
```

The test validates:
- `Dockerfile` structure, base image (`nginx:alpine`), explicit `COPY`, and `EXPOSE 80`.
- `index.html` contains `<title>Guestbook - v1</title>` and `<h1>Guestbook - v1</h1>`.
- `evidence/app.html` contains exact v1 markers.
- `evidence/up-app.html` contains `<title>Guestbook - v2</title>` and `<h1>Guestbook - v2</h1>`.
- `deployment.yml` contains container port 80, CPU/Memory requests, and limits for HPA.
