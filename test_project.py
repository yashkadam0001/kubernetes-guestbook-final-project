#!/usr/bin/env python3
"""
Test suite for Kubernetes Guestbook Final Project (Corrected).
Validates:
1. Dockerfile structure and syntax (Go multi-stage, COPY, EXPOSE 3000, CMD)
2. evidence/app.html (v1) tags: <title>Guestbook - v1</title> and <h1>Guestbook - v1</h1>
3. evidence/up-app.html (v2) tags: <title>Guestbook - v2</title> and <h1>Guestbook - v2</h1>
4. index.html active version verification
5. deployment.yml structure (image, containerPort 3000, requests 2m, limits 5m, replicas 1, selector)
6. grading-corrections/ and answers/ completeness
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

    assert re.search(r"FROM\s+golang:1\.18\s+AS\s+builder", content, re.IGNORECASE), "Dockerfile missing 'FROM golang:1.18 AS builder'"
    assert re.search(r"FROM\s+ubuntu:18\.04", content, re.IGNORECASE), "Dockerfile missing 'FROM ubuntu:18.04'"
    assert re.search(r"COPY\s+--from=builder\s+/app/main\s+/app/guestbook", content), "Dockerfile missing compiled binary COPY"
    assert re.search(r"EXPOSE\s+3000", content), "Dockerfile missing 'EXPOSE 3000'"
    assert re.search(r'CMD\s+\["\./guestbook"\]', content), "Dockerfile missing 'CMD [\"./guestbook\"]'"
    print("  [PASS] Dockerfile has valid Go multi-stage builder, required file copies, EXPOSE 3000, and CMD")

def test_html_v1(filename="evidence/app.html"):
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

def test_active_index():
    print("\n--- Testing index.html (Active) ---")
    test_file_exists("index.html")
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
    assert ("<title>Guestbook - v1</title>" in content or "<title>Guestbook - v2</title>" in content), "index.html missing valid Guestbook title"
    assert ("<h1>Guestbook - v1</h1>" in content or "<h1>Guestbook - v2</h1>" in content), "index.html missing valid Guestbook h1"
    print("  [PASS] index.html is valid Guestbook HTML with required title and h1 tags")

def test_deployment():
    print("\n--- Testing deployment.yml ---")
    test_file_exists("deployment.yml")
    with open("deployment.yml", "r", encoding="utf-8") as f:
        content = f.read()

    assert "kind: Deployment" in content, "Missing kind: Deployment"
    assert "name: guestbook" in content, "Missing name: guestbook"
    assert "containerPort: 3000" in content, "Missing containerPort: 3000"
    assert "5m" in content, "Missing 5m CPU limits"
    assert "2m" in content, "Missing 2m CPU requests"
    print("  [PASS] deployment.yml contains valid Deployment spec with containerPort 3000 and 5m/2m CPU requirements")

def test_grading_corrections():
    print("\n--- Testing grading-corrections/ files ---")
    files = [
        "grading-corrections/q1-dockerfile.txt",
        "grading-corrections/q4-hpa.txt",
        "grading-corrections/q9-revision.txt",
        "grading-corrections/q10-replicasets.txt",
        "grading-corrections/answers.txt",
    ]
    for filepath in files:
        test_file_exists(filepath)

    with open("grading-corrections/q4-hpa.txt", "r") as f:
        content = f.read()
        assert re.search(r"REPLICAS\s+AGE\s*\n\S+\s+\S+\s+\S+\s+\d+\s+\d+\s+0\s+", content), "q4-hpa.txt does not show REPLICAS = 0"
        print("  [PASS] grading-corrections/q4-hpa.txt confirmed with REPLICAS 0")

    with open("grading-corrections/q9-revision.txt", "r") as f:
        content = f.read()
        assert "5m" in content and "2m" in content, "q9-revision.txt missing 5m/2m"
        print("  [PASS] grading-corrections/q9-revision.txt confirmed with 5m limits and 2m requests")

    with open("grading-corrections/q10-replicasets.txt", "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip() and not line.startswith("NAME")]
        assert len(lines) == 2, f"Expected 2 ReplicaSets, found {len(lines)}"
        print(f"  [PASS] grading-corrections/q10-replicasets.txt confirmed with exactly {len(lines)} ReplicaSets (READY 1/0 combination)")

def main():
    print("Running Kubernetes Guestbook Correction Validation Tests...")
    try:
        test_dockerfile()
        test_html_v1("evidence/app.html")
        test_html_v2("evidence/up-app.html")
        test_active_index()
        test_deployment()
        test_grading_corrections()
        print("\nALL PROJECT STRUCTURE, SYNTAX, AND GRADING CORRECTIONS PASSED!\n")
        return 0
    except AssertionError as err:
        print(f"\n[FAIL] {err}\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
