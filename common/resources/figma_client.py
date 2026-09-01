import os
import re
import json
import requests
from dotenv import load_dotenv

# .env 로드
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))
env_path = os.path.join(ROOT_DIR, "common", "auth", ".env")
load_dotenv(env_path)

FIGMA_TOKEN = os.getenv("FIGMA_ACCESS_TOKEN")

class FigmaClient:
    def __init__(self, token=None):
        self.token = token or FIGMA_TOKEN
        if not self.token:
            raise ValueError("FIGMA_ACCESS_TOKEN is not set in .env")
        self.headers = {"X-Figma-Token": self.token}

    def parse_url(self, figma_url: str):
        """Figma URL에서 file_key와 node_id를 파싱합니다."""
        file_key_match = re.search(r"/(?:design|file)/([a-zA-Z0-9]+)", figma_url)
        file_key = file_key_match.group(1) if file_key_match else None

        node_id_match = re.search(r"node-id=([a-zA-Z0-9%_\-]+)", figma_url)
        node_id = node_id_match.group(1) if node_id_match else None
        if node_id:
            node_id = requests.utils.unquote(node_id).replace("-", ":")

        return file_key, node_id

    def get_file(self, file_key: str, depth: int = 3):
        """Figma 파일 전체 또는 지정한 depth까지의 노드 트리를 가져옵니다."""
        url = f"https://api.figma.com/v1/files/{file_key}?depth={depth}"
        res = requests.get(url, headers=self.headers)
        res.raise_for_status()
        return res.json()

    def get_nodes(self, file_key: str, node_ids: list):
        """특정 노드(프레임/컴포넌트)들의 상세 데이터를 가져옵니다."""
        ids_param = ",".join(node_ids)
        url = f"https://api.figma.com/v1/files/{file_key}/nodes?ids={ids_param}"
        res = requests.get(url, headers=self.headers)
        res.raise_for_status()
        return res.json()

    def get_image_urls(self, file_key: str, node_ids: list, format="png", scale=2):
        """특정 노드들의 렌더링된 고화질 이미지 URL을 가져옵니다."""
        ids_param = ",".join(node_ids)
        url = f"https://api.figma.com/v1/images/{file_key}?ids={ids_param}&format={format}&scale={scale}"
        res = requests.get(url, headers=self.headers)
        res.raise_for_status()
        return res.json().get("images", {})

    def extract_texts_and_flows(self, node: dict, results=None):
        """노드 트리에서 모든 UI 텍스트 및 라벨, 노트를 재귀적으로 추출합니다."""
        if results is None:
            results = []
        
        name = node.get("name", "")
        n_type = node.get("type", "")
        characters = node.get("characters", "")

        if characters:
            results.append({"name": name, "type": n_type, "text": characters})
        elif name:
            results.append({"name": name, "type": n_type, "text": ""})

        for child in node.get("children", []):
            self.extract_texts_and_flows(child, results)

        return results


if __name__ == "__main__":
    print(f"Figma Token Loaded: {FIGMA_TOKEN[:10]}... (Total {len(FIGMA_TOKEN)} chars)")
