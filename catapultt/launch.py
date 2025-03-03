#!/usr/bin/env python3

import re
import os
import sys
import shutil
import subprocess
import time
from pathlib import Path

from catapultt.config import CONFIG

import questionary
from questionary import Style
from rich.console import Console
from rich.panel import Panel

import pkg_resources

class LAUNCHER:
    def __init__(self):
        config_path = pkg_resources.resource_filename('catapultt', 'config/config.yaml')
        self.config = CONFIG(config_path)
        self.console = Console()

        # Custom questionary style
        self.custom_style = Style([
            ('qmark', 'fg:cyan bold'),
            ('question', 'fg:white bold'),
            ('answer', 'fg:green bold'),
            ('pointer', 'fg:cyan bold'),
            ('highlighted', 'fg:cyan bold'),
            ('selected', 'fg:green bold'),
            ('separator', 'fg:cyan'),
            ('instruction', 'fg:white'),
            ('text', 'fg:white'),
        ])

    def sanitize_name(self, name):
        """Sanitize the project name for use in Docker and file names"""
        # Replace spaces and special characters with underscores
        sanitized = re.sub(r'[^a-zA-Z0-9_-]', '_', name)
        # Convert to lowercase for Docker compatibility
        sanitized = sanitized.lower()
        # Ensure it starts with a letter or underscore (for Docker)
        if sanitized and not sanitized[0].isalpha() and sanitized[0] != '_':
            sanitized = 'project_' + sanitized
        return sanitized

    def get_project_name(self):
        """Get the project name from the user"""
        project_name = questionary.text(
            "Enter project name:",
            default="New_project",
            style=self.custom_style
        ).ask()
        
        if not project_name:
            project_name = "New_project"
        
        # Sanitize the name for use in Docker and file names
        sanitized_name = self.sanitize_name(project_name)
        
        if sanitized_name != project_name:
            self.console.print(f"[yellow]Project name sanitized to '[bold]{sanitized_name}[/]' for compatibility[/]")
        
        return project_name, sanitized_name

    def get_project_directory(self, project_name):

        """Get the target directory for the project"""
        # Ask if user wants to use current directory or specify another
        use_current = questionary.confirm(
            "Create project in current directory?", 
            default=True,
            style=self.custom_style
        ).ask()
        
        if use_current:
            return os.getcwd()
        
        # Ask for custom directory path with project name as the default subdirectory
        default_path = os.path.join(os.getcwd(), project_name)
        custom_dir = questionary.text(
            "Enter the path for the project directory:",
            default=default_path,
            style=self.custom_style
        ).ask()
        
        # Expand user path (e.g., ~ to /home/username)
        custom_dir = os.path.join(os.path.expanduser(custom_dir), project_name)
        
        # Check if directory exists
        if not os.path.exists(custom_dir):
            create_dir = questionary.confirm(
                f"Directory '{custom_dir}' does not exist. Create it?",
                default=True,
                style=self.custom_style
            ).ask()
            
            if create_dir:
                try:
                    os.makedirs(custom_dir, exist_ok=True)
                    self.console.print(f"[green]Created directory: {custom_dir}[/]")
                except Exception as e:
                    self.console.print(f"[bold red]Error creating directory: {e}[/]")
                    sys.exit(1)
            else:
                self.console.print("[yellow]Operation cancelled.[/]")
                sys.exit(0)
        
        return custom_dir


    def setup_environment(self, sanitized_name, project_dir):
        """Set up Docker environment files"""

        # Format the compose file with project-specific names
        service_name = sanitized_name
        image_name = f"{sanitized_name}-{self.env_type}"
        
        # Backup existing files
        current_time = str(int(time.time()))
        if os.path.exists(f"{project_dir}/Dockerfile"):
            shutil.move(f"{project_dir}/Dockerfile", f"{project_dir}/Dockerfile.backup.{current_time}")
            print("Backed up existing Dockerfile")
        if os.path.exists(f"{project_dir}/docker-compose.yml"):
            shutil.move(f"{project_dir}/docker-compose.yml", f"{project_dir}/docker-compose.yml.backup.{current_time}")
            print("Backed up existing docker-compose.yml")

        dockerfile_path = pkg_resources.resource_filename('catapultt', f'base_images/{self.config.dockerfiles[self.env_type]}')
        composefile_path = pkg_resources.resource_filename('catapultt', f'compose_files/{self.config.compose_files[self.env_type]}')
        # Create new files
        with open(f"{project_dir}/Dockerfile", "w") as f:
            with open(dockerfile_path, "r") as dockerfile:
                f.write(dockerfile.read())
        
        with open(f"{project_dir}/docker-compose.yml", "w") as f:
            with open(composefile_path, "r") as compose:
                f.write(compose.read().format(
                    service_name=service_name,
                    image_name=image_name
                )
            )
        
        self.console.print(f"[green]Created Dockerfile and docker-compose.yml for {sanitized_name} environment[/]")
        
        # Return project directory and image name for future operations
        return project_dir, image_name

    def create_template_files(self, project_dir, sanitized_name):
        """Create template files for the selected environment"""
        if self.env_type == "cpp":
            temp_path = pkg_resources.resource_filename('catapultt', f'templates/{self.config.template_files.cpp}')
            shutil.copytree(temp_path, project_dir, dirs_exist_ok=True)
        elif self.env_type == "node":
            temp_path = pkg_resources.resource_filename('catapultt', f'templates/{self.config.template_files.node}')
            shutil.copytree(temp_path, project_dir, dirs_exist_ok=True)
        elif self.env_type == "python":
            temp_path = pkg_resources.resource_filename('catapultt', f'templates/{self.config.template_files.python}')
            shutil.copytree(temp_path, project_dir, dirs_exist_ok=True)
        elif self.env_type == "deeplearning":
            temp_path = pkg_resources.resource_filename('catapultt', f'templates/{self.config.template_files.deeplearning}')
            shutil.copytree(temp_path, project_dir, dirs_exist_ok=True)
        else:
            self.console.print(f"[bold red]Unsupported environment: {self.env_type}[/]")
            sys.exit(1)

    def launch_environment(self, project_dir):
        """Launch Docker environment"""
        try:
            self.console.print("\n[bold cyan]Launching Docker environment...[/]")
            # Show spinner while running
            with self.console.status("[bold green]Building and starting containers...", spinner="dots"):
                subprocess.run(["docker", "compose", "-f", f"{project_dir}/docker-compose.yml", "up", "--build"], check=True)
        except subprocess.CalledProcessError as e:
            self.console.print(f"[bold red]Error launching Docker environment: {e}[/]")
            sys.exit(1)
        except KeyboardInterrupt:
            self.console.print("\n[bold yellow]Shutting down Docker environment...[/]")
            subprocess.run(["docker", "compose", "down"])

    def prompt_launch(self):
        self.console.print(Panel.fit(
            "[bold cyan]Docker Development Environment Launcher[/]",
            border_style="cyan"
        ))
        
        # Environment selection
        self.env_type = questionary.select(
            "Select an environment to launch:",
            choices=[
                {"name": "C++ Development", "value": "cpp"},
                {"name": "Node.js Development", "value": "node"},
                {"name": "Python Development", "value": "python"},
                {"name": "Deep Learning Development", "value": "deeplearning"},
            ],
            style=self.custom_style
        ).ask()
        
        if not self.env_type:
            sys.exit(0)

        use_existing = questionary.confirm(
            "Do you want to use the current directory as your project?",
            default=False,
            style=self.custom_style
        ).ask()

        if use_existing:
            project_dir = os.getcwd()
            sanitized_name = self.sanitize_name(os.path.basename(project_dir))
        else:
            # Get project name
            project_name, sanitized_name = self.get_project_name()
            
            # Get project directory
            project_dir = self.get_project_directory(sanitized_name)

        self.console.print(f"\n[bold]Setting up [cyan]{self.env_type}[/] development environment for project : {sanitized_name}...[/]")
        # Get the docker files
        project_dir, image_name = self.setup_environment(sanitized_name, project_dir)
        
        if not use_existing:
            # Create template files if needed
            self.create_template_files(project_dir, sanitized_name)
        
        # Launch confirmation
        launch = questionary.confirm(
            "Launch the environment now?", 
            default=True,
            style=self.custom_style
        ).ask()
        
        if launch:
            self.launch_environment(project_dir)
        else:
            self.console.print("\n[green]Environment files created. You can launch it later with 'docker compose up'[/]")

def main():
    launcher = LAUNCHER()
    launcher.prompt_launch()

if __name__ == "__main__":
    main()