import subprocess
from datetime import datetime


class RevisionHelper:
    def get_branches(self) -> list[dict]:
        # Update remote branches
        subprocess.run(["git", "fetch", "--prune"], check=True)

        # Get all remote branch names
        remote = subprocess.check_output(
            ["git", "branch", "-r", "--format=%(refname:short)"], text=True
        ).splitlines()

        branches = [
            r.split("/", 1)[1] for r in remote if "HEAD" not in r and r.startswith("origin/")
        ]

        results = []

        for branch in branches:
            date_str = subprocess.check_output(
                ["git", "log", "-1", "--format=%ci", f"origin/{branch}"], text=True
            ).strip()

            commit_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S %z")
            date = commit_date.strftime("%d.%m.%Y")

            results.append(
                {
                    "name": branch,
                    "date": date,
                }
            )

        def branch_sort_key(branch_obj: dict):
            name = branch_obj["name"]
            if name in ("main", "master"):
                return 0, name
            elif name.startswith("renovate/"):
                return 2, name
            else:
                return 1, name

        results.sort(key=branch_sort_key)

        return results

    def get_tags(self) -> list[dict]:
        # Update remote tags
        subprocess.run(["git", "fetch", "--prune"], check=True)

        # Get tag names and creation dates
        output = subprocess.check_output(
            [
                "git",
                "for-each-ref",
                "--sort=-creatordate",
                "--format=%(refname:short)|%(creatordate:iso8601)",
                "refs/tags",
            ],
            text=True,
        ).splitlines()

        tags = []
        for line in output:
            if "|" not in line:
                continue
            name, date_str = line.split("|", 1)
            date_result = datetime.strptime(date_str.strip(), "%Y-%m-%d %H:%M:%S %z")

            date = date_result.strftime("%d.%m.%Y")

            tags.append(
                {
                    "name": name,
                    "date": date,
                }
            )

        return tags

    def get_current_revision(self) -> str:
        try:
            # try with tag
            tag = subprocess.check_output(
                ["git", "describe", "--tags", "--exact-match"],
                text=True,
                stderr=subprocess.DEVNULL,
            ).strip()
            if tag:
                return tag
        except subprocess.CalledProcessError:
            pass

        # try with branch
        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"], text=True
        ).strip()
        if branch != "HEAD":
            return branch

        commit = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
        return commit
