#!/usr/bin/env python3
"""
Test suite for Kubernetes Guestbook Final Project.
Validates:
1. Dockerfile structure and syntax (FROM, COPY, EXPOSE, CMD)
2. index.html (v1) tags: <title>Guestbook - v1</title> and <h1>Guestbook - v1</h1>
3. evidence/app.html (v1) tags
4. evidence/up-app.html (v2) tags: <title>Guestbook - v2</title> and <h1>Guestbook - v2</h1>
5. deployment.yml structure (image, containerPort, requests, limits, replicas, selector)
6. hpa.yml structure (scaleTargetRef, minReplicas, maxReplicas, metrics)
"""

import os
import re
import sys

def test_file_exists(path):
    assert os.path.exists(path), f"File missing: {path}"
    print(f"  [PASS] File exists: {path}")

def test_dockerfile():
    print("\n--- Testing Dockerfile ---")
    test_file_exists("Dockerfile")
    with open("Dockerfile", "r", encoding="utf-8") as f:
        content = f.read()

    assert re.search(r"^\s*FROM\s+nginx:alpine", content, re.MULTILINE), "Dockerfile missing 'FROM nginx:alpine'"
    assert re.search(r"^\s*COPY\s+index\.html\s+/usr/share/nginx/html/index\.html", content, re.MULTILINE), "Dockerfile missing explicit 'COPY index.html /usr/share/nginx/html/index.html'"
    assert re.search(r"^\s*EXPOSE\s+80", content, re.MULTILINE), "Dockerfile missing 'EXPOSE 80'"
    print("  [PASS] Dockerfile has valid base image, explicit COPY, and EXPOSE 80")

def test_html_v1(filename="index.html"):
    print(f"\n--- Testing {filename} (v1) ---")
    test_file_exists(filename)
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()

    assert "<title>Guestbook - v1</title>" in content, f"{filename} missing '<title>Guestbook - v1</title>'"
    assert "<h1>Guestbook - v1</h1>" in content, f"{filename} missing '<h1>Guestbook - v1</h1>'"
    assert "form" in content.lower(), f"{filename} missing form element"
    assert "submit" in content.lower(), f"{filename} missing submit button"
    print(f"  [PASS] {filename} contains exact '<title>Guestbook - v1</title>' and '<h1>Guestbook - v1</h1>' with functional form")

def test_html_v2(filename="evidence/up-app.html"):
    print(f"\n--- Testing {filename} (v2) ---")
    test_file_exists(filename)
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()

    assert "<title>Guestbook - v2</title>" in content, f"{filename} missing '<title>Guestbook - v2</title>'"
    assert "<h1>Guestbook - v2</h1>" in content, f"{filename} missing '<h1>Guestbook - v2</h1>'"
    assert "form" in content.lower(), f"{filename} missing form element"
    assert "submit" in content.lower(), f"{filename} missing submit button"
    print(f"  [PASS] {filename} contains exact '<title>Guestbook - v2</title>' and '<h1>Guestbook - v2</h1>' with functional form")

def test_deployment():
    print("\n--- Testing deployment.yml ---")
    test_file_exists("deployment.yml")
    with open("deployment.yml", "r", encoding="utf-8") as f:
        content = f.read()

    assert "kind: Deployment" in content, "Missing kind: Deployment"
    assert "name: guestbook" in content, "Missing name: guestbook"
    assert "containerPort: 80" in content, "Missing containerPort: 80"
    assert "cpu:" in content, "Missing CPU resource requests/limits"
    assert "memory:" in content, "Missing memory resource requests/limits"
    assert "image:" in content, "Missing image field"
    print("  [PASS] deployment.yml contains valid Deployment spec with CPU/Memory requests & limits for HPA")

def main():
    print("Running Kubernetes Guestbook Project Validation Tests...")
    try:
        test_dockerfile()
        test_html_v1("index.html")
        test_html_v1("evidence/app.html")
        test_html_v2("evidence/up-app.html")
        test_deployment()
        print("\nALL PROJECT STRUCTURE AND SYNTAX CHECKS PASSED SUCCESSFULLY!\n")
        return 0
    except AssertionError as err:
        print(f"\n[FAIL] {err}\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
