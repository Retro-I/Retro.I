import json
import logging
import os

from helper.Constants import Constants

logger = logging.getLogger(__name__)
c = Constants()


class SettingsSyncHelper:
    def sync_values(self, source, target, template_source: dict) -> dict | list:
        # --- Case 1: both are dicts ---
        if isinstance(source, dict) and isinstance(target, dict):

            # Add missing keys
            for key, src_val in source.items():
                if key not in target:
                    target[key] = src_val
                else:
                    target[key] = self.sync_values(src_val, target[key], template_source)

            # Remove keys that no longer exist in source
            for key in list(target.keys()):
                if key not in source:
                    del target[key]

            return target

        # --- Case 2: both are lists ---
        elif isinstance(target, list):

            # Remove keys that no longer exist in source
            for item in target:
                for key in list(item.keys()):
                    if key not in template_source:
                        del item[key]

            for item in target:
                for key, src_val in template_source.items():
                    if key not in item:
                        item[key] = src_val
                    else:
                        item[key] = self.sync_values(src_val, item[key], template_source)

            return target

            # --- Case 3: primitives (str, int, bool, etc.) ---
        else:
            # DO NOT overwrite existing target value
            return target

    def repair_settings_file(self, filename: str):
        default_settings_path = f"{c.default_settings_path()}/{filename}"
        settings_path = f"{c.settings_path()}/{filename}"

        # If default (source) doesn't exist → delete target
        if not os.path.exists(default_settings_path):
            if os.path.exists(settings_path):
                os.remove(settings_path)
            return

        # Read source JSON
        with open(default_settings_path, "r") as f:
            source = json.load(f)

        # Create target if missing
        if not os.path.exists(settings_path):
            with open(settings_path, "w") as f:
                json.dump(source, f, indent=4)
            print(f"Created new settings file: {filename}")
            return

        # Read existing target JSON
        with open(settings_path, "r") as f:
            target = json.load(f)

        template_source = ""
        # Read if template path exists
        if os.path.exists(f"{c.default_settings_path()}/templates/template_{filename}"):
            with open(f"{c.default_settings_path()}/templates/template_{filename}", "r") as f:
                template_source = json.load(f)

        # Sync source → target
        target = self.sync_values(source, target, template_source)

        # Save updated target
        with open(settings_path, "w") as f:
            json.dump(target, f, indent=4)

    def repair_all_settings_files(self):
        path = c.default_settings_path()
        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        for filename in files:
            logger.info(f"Fixing file {filename}...")
            self.repair_settings_file(filename)
