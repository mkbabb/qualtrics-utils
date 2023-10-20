from pathlib import Path
import subprocess

def generate_openapi_clients() -> None:
    base_url = "https://stoplight.io/api/v1/projects/qualtricsv2/publicapidocs/nodes/reference/"
    urls = [
        f"{base_url}surveyResponses.json?fromExportButton=true&snapshotType=http_service",
        f"{base_url}responseImportsExports.json?fromExportButton=true&snapshotType=http_service"
    ]

    for url in urls:
        print(f"Generating client for {url}")
        subprocess.run(["openapi-python-client", "generate", "--url", url])
        clean_directories(Path.cwd())

def clean_directories(root_dir: Path) -> None:
    for top_most_dir in root_dir.iterdir():
        if top_most_dir.is_dir():
            desired_sub_dir = top_most_dir.name.replace("-", "_")
            desired_sub_path = top_most_dir / desired_sub_dir

            if desired_sub_path.exists():
                for item in top_most_dir.iterdir():
                    if item != desired_sub_path:
                        if item.is_dir():
                            item.rmdir()
                        else:
                            item.unlink()

                # Move the desired_sub_dir out and remove the top_most_dir
                desired_sub_path.rename(root_dir / desired_sub_dir)
                top_most_dir.rmdir()

if __name__ == '__main__':
    generate_openapi_clients()
