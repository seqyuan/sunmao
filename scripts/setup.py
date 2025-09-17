#!/usr/bin/env python3
"""
Quick setup script for sunmao project
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


def check_requirements():
    """Check if required tools are installed"""
    print("Checking requirements...")
    
    # Check Poetry
    try:
        run_command("poetry --version")
    except subprocess.CalledProcessError:
        print("Poetry not found. Please install Poetry first:")
        print("curl -sSL https://install.python-poetry.org | python3 -")
        sys.exit(1)
    
    # Check Git
    try:
        run_command("git --version")
    except subprocess.CalledProcessError:
        print("Git not found. Please install Git first.")
        sys.exit(1)


def setup_project():
    """Setup the project"""
    print("Setting up sunmao project...")
    
    # Install dependencies
    print("Installing dependencies...")
    run_command("poetry install")
    
    # Run tests
    print("Running tests...")
    run_command("poetry run pytest tests/ -v")
    
    # Run linting
    print("Running linting...")
    run_command("poetry run flake8 sunmao/")
    run_command("poetry run black --check sunmao/")
    
    print("Project setup completed successfully!")


def setup_git():
    """Setup Git repository"""
    print("Setting up Git repository...")
    
    # Check if already a git repository
    if Path(".git").exists():
        print("Git repository already exists.")
        return
    
    # Initialize git repository
    run_command("git init")
    run_command("git add .")
    run_command("git commit -m 'Initial commit'")
    
    print("Git repository initialized.")


def setup_github():
    """Setup GitHub repository"""
    print("Setting up GitHub repository...")
    
    # Check if GitHub CLI is installed
    try:
        run_command("gh --version")
    except subprocess.CalledProcessError:
        print("GitHub CLI not found. Please install it first:")
        print("https://cli.github.com/")
        print("Or manually create a repository on GitHub and run:")
        print("git remote add origin https://github.com/seqyuan/sunmao.git")
        print("git push -u origin main")
        return
    
    # Create GitHub repository
    run_command("gh repo create seqyuan/sunmao --public --description 'A flexible subplot layout library for matplotlib'")
    run_command("git remote add origin https://github.com/seqyuan/sunmao.git")
    run_command("git push -u origin main")
    
    print("GitHub repository created and pushed.")


def main():
    """Main setup process"""
    print("Sunmao Project Setup")
    print("===================")
    
    # Check if we're in the right directory
    if not Path("pyproject.toml").exists():
        print("Error: pyproject.toml not found. Run this script from the project root.")
        sys.exit(1)
    
    # Check requirements
    check_requirements()
    
    # Setup project
    setup_project()
    
    # Setup Git
    response = input("Setup Git repository? (y/N): ")
    if response.lower() == 'y':
        setup_git()
    
    # Setup GitHub
    response = input("Setup GitHub repository? (y/N): ")
    if response.lower() == 'y':
        setup_github()
    
    print("\nSetup completed!")
    print("\nNext steps:")
    print("1. Configure PyPI token: poetry config pypi-token.pypi your-token")
    print("2. Build package: make build")
    print("3. Publish to PyPI: make publish")
    print("4. Setup ReadTheDocs: https://readthedocs.org/dashboard/")
    print("5. See RELEASE_GUIDE.md for detailed instructions")


if __name__ == "__main__":
    main()
