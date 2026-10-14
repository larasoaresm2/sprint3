import json
from abc import ABC, abstractmethod


class Asset(ABC):
    """Abstract base class: represents any IT asset."""

    def __init__(self, asset_id, name, owner, linked_ids=None):
        self.id = asset_id
        self.name = name
        self.owner = owner
        # IDs of other assets this one is connected to (the "links")
        if linked_ids is None:
            linked_ids = []
        self.linked_ids = linked_ids

    @abstractmethod
    def display_details(self):
        """Every asset type must define how it presents itself."""
        return f"[{self.id}] {self.name} | owner: {self.owner} | links: {self.linked_ids}"

    def to_dict(self):
        """Fields shared by every asset, plus the "type" used to rebuild it."""
        return {
            "type": type(self).__name__,
            "id": self.id,
            "name": self.name,
            "owner": self.owner,
            "linked_ids": self.linked_ids,
        }


class Server(Asset):
    def __init__(self, asset_id, name, owner, operating_system, linked_ids=None):
        super().__init__(asset_id, name, owner, linked_ids)
        self.operating_system = operating_system

    def display_details(self):
        base = super().display_details()
        return f"{base} | OS: {self.operating_system}"

    def to_dict(self):
        data = super().to_dict()
        data["operating_system"] = self.operating_system
        return data


class Router(Asset):
    def __init__(self, asset_id, name, owner, model, linked_ids=None):
        super().__init__(asset_id, name, owner, linked_ids)
        self.model = model

    def display_details(self):
        base = super().display_details()
        return f"{base} | model: {self.model}"

    def to_dict(self):
        data = super().to_dict()
        data["model"] = self.model
        return data


class Notebook(Asset):
    def __init__(self, asset_id, name, owner, brand, linked_ids=None):
        super().__init__(asset_id, name, owner, linked_ids)
        self.brand = brand

    def display_details(self):
        base = super().display_details()
        return f"{base} | brand: {self.brand}"

    def to_dict(self):
        data = super().to_dict()
        data["brand"] = self.brand
        return data


def asset_from_dict(data):
    """Rebuild the right subclass from a dictionary read from JSON."""
    asset_type = data["type"]
    if asset_type == "Server":
        return Server(data["id"], data["name"], data["owner"],
                      data["operating_system"], data["linked_ids"])
    if asset_type == "Router":
        return Router(data["id"], data["name"], data["owner"],
                      data["model"], data["linked_ids"])
    if asset_type == "Notebook":
        return Notebook(data["id"], data["name"], data["owner"],
                        data["brand"], data["linked_ids"])
    raise ValueError(f"Unknown asset type: {asset_type}")


def save_assets(assets, path):
    """Write the assets as a JSON array of objects."""
    with open(path, "w", encoding="utf-8") as file:
        json.dump([asset.to_dict() for asset in assets], file, indent=2, ensure_ascii=False)


def load_assets(path):
    """Read the JSON array and rebuild one object per item."""
    with open(path, "r", encoding="utf-8") as file:
        return [asset_from_dict(item) for item in json.load(file)]


if __name__ == "__main__":
    # Exercise 4: polymorphism - same call, different behavior per type
    server = Server(1, "File Server", "João", "Linux")
    router = Router(2, "Core Router", "Maria", "Cisco ISR 4331", linked_ids=[1])
    notebook = Notebook(3, "NB-Finance-01", "Ana", "Dell", linked_ids=[1, 2])

    assets = [server, router, notebook]

    print("=== All assets ===")
    for asset in assets:
        print(asset.display_details())

    # Exercise 5: isinstance() - identify the type of each object
    server_count = 0
    for asset in assets:
        if isinstance(asset, Server):
            server_count += 1
    print(f"\nTotal servers: {server_count}")

    # Abstraction: the abstract base class cannot be instantiated
    try:
        Asset(99, "x", "y")
    except TypeError as error:
        print(f"\nCannot create a generic Asset: {error}")

    # Exercises 6 and 7: save to JSON with a "type" field and load it back
    save_assets(assets, "assets.json")
    print("\nSaved to assets.json")

    reloaded = load_assets("assets.json")
    print("=== Reloaded from assets.json ===")
    for asset in reloaded:
        print(asset.display_details())

    same = all(
        type(a) is type(b) and a.id == b.id and a.linked_ids == b.linked_ids
        for a, b in zip(assets, reloaded)
    )
    print(f"\nTypes, IDs and links preserved after reload: {same}")
