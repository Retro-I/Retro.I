import json
import logging
import os
from copy import deepcopy

import jsonschema_default
from jsonschema import Draft7Validator

from helper.Constants import Constants

logger = logging.getLogger(__name__)
c = Constants()


class SettingsSyncHelper:
    def validate_by_path(self, path):
        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        for filename in files:
            full_path = f"{path}/{filename}"
            data = self.get_data_for_filename(full_path)
            schema = self.get_schema_for_filename(full_path)

            if not self.is_valid(data, schema):
                raise RuntimeError(f"File {filename} is not valid")

    def validate_all_settings(self):
        settings_path = Constants.settings_path()
        self.validate_by_path(settings_path)

        effects_path = Constants.effects_path()
        self.validate_by_path(effects_path)

    def validate_and_repair_all_settings(self):
        path = Constants.settings_path()
        default_path = Constants.default_settings_path()

        default_files = [
            f for f in os.listdir(default_path) if os.path.isfile(os.path.join(default_path, f))
        ]

        for default_file in default_files:
            default_settings_path = f"{default_path}/{default_file}"
            settings_path = f"{path}/{default_file}"

            # If default (source) doesn't exist → delete target
            if not os.path.exists(default_settings_path):
                if os.path.exists(settings_path):
                    os.remove(settings_path)
                continue

            # Read source JSON
            with open(default_settings_path, "r") as f:
                source = json.load(f)

            # Create target if missing
            if not os.path.exists(settings_path):
                with open(settings_path, "w") as f:
                    json.dump(source, f, indent=4)
                print(f"Created new settings file: {default_file}")
                continue

        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

        for filename in files:
            full_path = f"{path}/{filename}"
            default_settings_path = f"{default_path}/{filename}"

            if not os.path.exists(default_settings_path):
                os.remove(full_path)
                continue

            data = self.get_data_for_filename(full_path)
            schema = self.get_schema_for_filename(full_path)

            if not self.is_valid(data, schema):
                logger.info(f"Fixing settings file {filename}...")
                repaired_data = self.repair(data, schema)

                with open(full_path, "r+") as file:
                    file.seek(0)
                    json.dump(repaired_data, file, indent=4)
                    file.truncate()

                data = self.get_data_for_filename(full_path)
                schema = self.get_schema_for_filename(full_path)

                if not self.is_valid(data, schema):
                    raise RuntimeError(f"Fix not applied to {full_path}!")

    def is_valid(self, data: dict | list, schema: dict) -> bool:
        validator = Draft7Validator(schema)
        return validator.evolve(schema=schema).is_valid(data, schema)

    def repair(self, data, schema):
        if data is None:
            return None

        repaired = deepcopy(data)
        validator = Draft7Validator(schema)
        default_data = jsonschema_default.create_from(schema)

        # --- CASE 1: Object (dict) ---
        if isinstance(data, dict):
            for error in validator.iter_errors(data):

                # Missing required fields
                if error.validator == "required":
                    for missing in error.validator_value:
                        if missing not in repaired:
                            default_value = default_data.get(missing)

                            if default_value is not None:
                                repaired[missing] = deepcopy(default_value)

                # Remove additional properties
                if error.validator == "additionalProperties":
                    allowed = set(schema.get("properties", {}).keys())
                    for key in list(repaired.keys()):
                        if key not in allowed:
                            del repaired[key]

            # Recursively repair nested objects
            for key, subschema in schema.get("properties", {}).items():
                if key in repaired:
                    if subschema.get("type") == "object" and isinstance(repaired[key], dict):
                        repaired[key] = self.repair(repaired[key], subschema)

            return repaired

        # --- CASE 2: Array (list) ---
        if isinstance(data, list):
            item_schema = schema.get("items", {})
            repaired_list = []

            for item in data:
                # Repair each element recursively
                repaired_item = self.repair(item, item_schema)
                repaired_list.append(repaired_item)

            return repaired_list
        return data

    def get_data_for_filename(self, full_path):
        with open(full_path, "r") as f:
            data = json.load(f)

        return data

    def get_schema_for_filename(self, full_path):
        path, filename = os.path.split(full_path)
        schema_path = os.path.join(path, f"schemas/schema_{filename}")

        with open(schema_path, "r") as f:
            data = json.load(f)

        return data
