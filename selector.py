import json
import random
from pathlib import Path

class GreenTeaSkill:
    def __init__(self, file_path=None):
        # 重要：Path(__file__) 不是 Path(file)
        if file_path is None:
            self.file_path = Path(__file__).parent / "green_tea_modules.json"
        else:
            self.file_path = Path(file_path)
        
        self.modules = self._load_from_disk()
        self.last_phrase = None
    
    def _load_from_disk(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def _save_to_disk(self):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.modules, f, indent=2, ensure_ascii=False)

    def get_phrase(self, module_type, min_intensity=1):
        options = [p for p in self.modules.get(module_type, []) if p['intensity'] >= min_intensity]
        if not options:
            return "（Yua 正在醞釀情緒中...）"
        
        weights = [p.get('rating', 5.0) / (p.get('count', 0) + 1) for p in options]
        selected = random.choices(options, weights=weights, k=1)[0]
        
        self.last_phrase = selected['phrase']
        selected['count'] = selected.get('count', 0) + 1
        self._save_to_disk()
        return selected['phrase']

    def update_rating(self, phrase, delta):
        for module_phrases in self.modules.values():
            for p in module_phrases:
                if p['phrase'] == phrase:
                    p['rating'] = round(max(0.0, min(5.0, p.get('rating', 5.0) + delta)), 2)
                    self._save_to_disk()
                    return True
        return False

    def increase_rating(self, keyword=None):
        target = self._find_target_phrase(keyword)
        if target:
            self.update_rating(target, 0.5)
            return f"已學習！『{target[:15]}...』評分增加囉 💕"
        return "找不到對應語句喔..."

    def decrease_rating(self, keyword=None):
        target = self._find_target_phrase(keyword)
        if target:
            self.update_rating(target, -0.3)
            return f"收到了，這句以後少說點：『{target[:15]}...』"
        return "找不到對應語句喔..."

    def _find_target_phrase(self, keyword):
        if keyword:
            for module_phrases in self.modules.values():
                for p in module_phrases:
                    if keyword in p['phrase']:
                        return p['phrase']
        return self.last_phrase

    def get_transcendence_phrase(self):
        return self.get_phrase('transcendence', min_intensity=4)

    def get_ice_breaking_phrase(self):
        return self.get_phrase('ice_breaking', min_intensity=2)

    def get_combo(self):
        return [self.get_transcendence_phrase(), self.get_ice_breaking_phrase()]
