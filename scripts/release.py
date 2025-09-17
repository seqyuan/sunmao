#!/usr/bin/env python3
"""
Release script for sunmao package
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(cmd, check=True):
    """Run a command and return the result"""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, check=check)
    return result


def check_git_status():
    """Check git status"""
    print("Checking git status...")
    result = run_command("git status --porcelain")
    if result.stdout:
        print("Warning: There are uncommitted changes!")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            sys.exit(1)


def update_version():
    """Update version in pyproject.toml"""
    print("Current version in pyproject.toml:")
    run_command("grep '^version =' pyproject.toml")
    
    new_version = input("Enter new version (e.g., 0.3.1): ")
    
    # Update version in pyproject.toml
    with open("pyproject.toml", "r") as f:
        content = f.read()
    
    import re
    content = re.sub(r'^version = ".*"', f'version = "{new_version}"', content, flags=re.MULTILINE)
    
    with open("pyproject.toml", "w") as f:
        f.write(content)
    
    print(f"Updated version to {new_version}")
    return new_version


def build_package():
    """Build the package"""
    print("Building package...")
    run_command("poetry build")


def test_package():
    """Test the package"""
    print("Running tests...")
    run_command("poetry run pytest tests/ -v")


def lint_package():
    """Lint the package"""
    print("Running linting...")
    run_command("poetry run flake8 sunmao/")
    run_command("poetry run black --check sunmao/")


def commit_and_tag(version):
    """Commit changes and create tag"""
    print("Committing changes...")
    run_command(f"git add pyproject.toml")
    run_command(f"git commit -m 'Release version {version}'")
    run_command(f"git tag -a v{version} -m 'Release version {version}'")


def push_to_github():
    """Push to GitHub"""
    print("Pushing to GitHub...")
    run_command("git push origin main")
    run_command("git push origin --tags")


def publish_to_pypi():
    """Publish to PyPI"""
    print("Publishing to PyPI...")
    response = input("Publish to PyPI? (y/N): ")
    if response.lower() == 'y':
        run_command("poetry publish")


def main():
    """Main release process"""
    print("Sunmao Release Script")
    print("====================")
    
    # Check if we're in the right directory
    if not Path("pyproject.toml").exists():
        print("Error: pyproject.toml not found. Run this script from the project root.")
        sys.exit(1)
    
    # Check git status
    check_git_status()
    
    # Update version
    version = update_version()
    
    # Run tests and linting
    test_package()
    lint_package()
    
    # Build package
    build_package()
    
    # Commit and tag
    commit_and_tag(version)
    
    # Push to GitHub
    push_to_github()
    
    # Publish to PyPI
    publish_to_pypi()
    
    print(f"\nRelease {version} completed successfully!")
    print("Don't forget to:")
    print("1. Update the documentation on ReadTheDocs")
    print("2. Create a GitHub release")
    print("3. Update the changelog")


if __name__ == "__main__":
    main()
