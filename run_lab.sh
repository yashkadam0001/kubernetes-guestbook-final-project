#!/bin/bash
# ==============================================================================
# IBM Skills Network / Coursera Kubernetes Guestbook Final Project
# Automated End-to-End Execution & Evidence Capture Script
# ==============================================================================
set -e

echo "=========================================================="
echo " Starting Kubernetes Guestbook Lab Execution & Evidence Collection"
echo "=========================================================="

# 1. Discover or set namespace
if [ -z "$MY_NAMESPACE" ]; then
    if command -v ibmcloud &> /dev/null; then
        MY_NAMESPACE=$(ibmcloud cr namespaces | grep -v "Listing" | grep -v "Namespace" | head -n 1 | awk '{print $1}')
    fi
fi

if [ -z "$MY_NAMESPACE" ]; then
    echo "ERROR: MY_NAMESPACE is not defined and could not be detected."
    echo "Please set it with: export MY_NAMESPACE=<your-sn-labs-namespace>"
    exit 1
fi

echo "[INFO] Using Container Registry Namespace: $MY_NAMESPACE"

# Ensure evidence and answers directories exist
mkdir -p evidence answers

# Ensure index.html is v1 initially
cp evidence/app.html index.html
echo "[INFO] Verified index.html is set to v1."

# ------------------------------------------------------------------------------
# STEP 1: Question 1 & 2 - Build and push v1, capture ibmcloud cr images
# ------------------------------------------------------------------------------
echo "--- Step 1: Building and pushing Guestbook v1 ---"
docker build -t "us.icr.io/${MY_NAMESPACE}/guestbook:v1" .
docker push "us.icr.io/${MY_NAMESPACE}/guestbook:v1"

echo "--- Step 2: Capturing ibmcloud cr images (Question 2) ---"
ibmcloud cr images | tee evidence/crimages.txt

# ------------------------------------------------------------------------------
# STEP 2: Question 7 (Initial) - Apply Deployment
# ------------------------------------------------------------------------------
echo "--- Step 3: Preparing and applying deployment.yml ---"
sed -i "s|image: us.icr.io/[^/]*/guestbook:v[0-9]|image: us.icr.io/${MY_NAMESPACE}/guestbook:v1|g" deployment.yml
kubectl apply -f deployment.yml | tee evidence/deployment.txt

echo "[INFO] Waiting for deployment rollout to complete..."
kubectl rollout status deployment/guestbook --timeout=120s
kubectl get pods -l app=guestbook

# ------------------------------------------------------------------------------
# STEP 3: Question 4 - Configure HPA and capture initial status
# ------------------------------------------------------------------------------
echo "--- Step 4: Configuring Horizontal Pod Autoscaler (Question 4) ---"
# Remove any existing HPA to start cleanly
kubectl delete hpa guestbook --ignore-not-found=true
kubectl autoscale deployment guestbook --cpu-percent=50 --min=1 --max=10

echo "[INFO] Waiting for HPA table to initialize..."
sleep 5
kubectl get hpa | tee evidence/hpa.txt

# ------------------------------------------------------------------------------
# STEP 4: Question 5 - Generate load to trigger autoscaling
# ------------------------------------------------------------------------------
echo "--- Step 5: Generating load for autoscaling (Question 5) ---"
# Expose service if not already exposed
kubectl apply -f hpa.yml || true

# Start load generator in background
echo "[INFO] Launching load generator pod..."
kubectl run load-generator --image=busybox:latest --restart=Never -- /bin/sh -c "while true; do wget -q -O- http://guestbook:80 > /dev/null 2>&1; done" || true

echo "[INFO] Generating load for 60 seconds to observe scaling..."
for i in {1..12}; do
    echo "  Checking scaling progress ($((i*5))s)..."
    kubectl get hpa
    sleep 5
done

echo "--- Capturing autoscaling evidence (Question 5) ---"
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

# Clean up load generator
kubectl delete pod load-generator --ignore-not-found=true

# ------------------------------------------------------------------------------
# STEP 5: Question 6 - Update to v2, build, push, capture output with digest
# ------------------------------------------------------------------------------
echo "--- Step 6: Updating to Guestbook v2 and pushing image (Question 6) ---"
cp evidence/up-app.html index.html
docker build -t "us.icr.io/${MY_NAMESPACE}/guestbook:v2" .
docker push "us.icr.io/${MY_NAMESPACE}/guestbook:v2" 2>&1 | tee evidence/upguestbook.txt

# ------------------------------------------------------------------------------
# STEP 6: Question 7 (Updated) - Apply updated Deployment with v2
# ------------------------------------------------------------------------------
echo "--- Step 7: Applying updated Deployment with v2 (Question 7) ---"
sed -i "s|image: us.icr.io/[^/]*/guestbook:v[0-9]|image: us.icr.io/${MY_NAMESPACE}/guestbook:v2|g" deployment.yml
kubectl apply -f deployment.yml | tee evidence/deployment.txt
kubectl rollout status deployment/guestbook --timeout=120s

# ------------------------------------------------------------------------------
# STEP 7: Question 9 - CPU change & rollout history
# ------------------------------------------------------------------------------
echo "--- Step 8: Updating CPU resources and capturing rollout history (Question 9) ---"
kubectl set resources deployment guestbook -c=guestbook --limits=cpu=200m --requests=cpu=100m
kubectl rollout status deployment/guestbook --timeout=120s

REV_NUM=$(kubectl rollout history deployment/guestbook | grep -oE "^[0-9]+" | tail -n 1)

{
    echo "=== Deployment Rollout History ==="
    kubectl rollout history deployment/guestbook
    echo ""
    echo "=== Detailed Revision Info (Revision ${REV_NUM}) ==="
    kubectl rollout history deployment/guestbook --revision=${REV_NUM}
} | tee evidence/rev.txt

# ------------------------------------------------------------------------------
# STEP 8: Question 10 - Rollback and ReplicaSets
# ------------------------------------------------------------------------------
echo "--- Step 9: Performing Rollback and capturing ReplicaSets (Question 10) ---"
kubectl rollout undo deployment/guestbook
kubectl rollout status deployment/guestbook --timeout=120s

kubectl get rs | tee evidence/rs.txt

# ------------------------------------------------------------------------------
# STEP 9: Generate final answers/answers.txt
# ------------------------------------------------------------------------------
echo "--- Step 10: Compiling final answers/answers.txt ---"
python3 -c "
with open('Dockerfile', 'r') as f:
    q1 = f.read().strip()
with open('evidence/crimages.txt', 'r') as f:
    q2 = f.read().strip()
with open('evidence/app.html', 'r') as f:
    q3 = f.read().strip()
with open('evidence/hpa.txt', 'r') as f:
    q4 = f.read().strip()
with open('evidence/hpa2.txt', 'r') as f:
    q5 = f.read().strip()
with open('evidence/upguestbook.txt', 'r') as f:
    q6 = f.read().strip()
with open('evidence/deployment.txt', 'r') as f:
    q7 = f.read().strip()
with open('evidence/up-app.html', 'r') as f:
    q8 = f.read().strip()
with open('evidence/rev.txt', 'r') as f:
    q9 = f.read().strip()
with open('evidence/rs.txt', 'r') as f:
    q10 = f.read().strip()

answers = f'''================================================================================
IBM SKILLS NETWORK / COURSERA KUBERNETES GUESTBOOK FINAL PROJECT - ANSWERS
================================================================================

Question 1 — Dockerfile (1 point)
--------------------------------------------------------------------------------
{q1}

Question 2 — Container Registry image (1 point)
--------------------------------------------------------------------------------
{q2}

Question 3 — Initial index.html (1 point)
--------------------------------------------------------------------------------
{q3}

Question 4 — HPA details (1 point)
--------------------------------------------------------------------------------
{q4}

Question 5 — Autoscaling (2 points)
--------------------------------------------------------------------------------
{q5}

Question 6 — Updated Docker image push (2 points)
--------------------------------------------------------------------------------
{q6}

Question 7 — Deployment applied (1 point)
--------------------------------------------------------------------------------
{q7}

Question 8 — Updated index.html (2 points)
--------------------------------------------------------------------------------
{q8}

Question 9 — CPU rollout history (2 points)
--------------------------------------------------------------------------------
{q9}

Question 10 — ReplicaSets after rollback (2 points)
--------------------------------------------------------------------------------
{q10}
'''

with open('answers/answers.txt', 'w') as out:
    out.write(answers)
print('[SUCCESS] Compiled answers/answers.txt with all 10 responses.')
"

echo "=========================================================="
echo " All 10 Lab Tasks Completed Successfully!"
echo " Evidence saved in: evidence/"
echo " Answers compiled in: answers/answers.txt"
echo "=========================================================="
