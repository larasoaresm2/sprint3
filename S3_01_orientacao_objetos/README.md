# S3_01 — Inheritance, polymorphism and abstraction

Card: *Orientação a Objetos: Herança, Polimorfismo e Abstração* (Sprint 3).

## How to run

```bash
cd S3_01_orientacao_objetos
python3 ativos.py
```

The program prints every asset, counts the servers, shows that the abstract class cannot be instantiated, saves the assets to `assets.json` and loads them back.

## Exercises

| # | Exercise | Where |
| --- | --- | --- |
| 1 | Base class `Ativo` | `Asset`, an abstract class (`ABC`) |
| 2 | Subclasses Notebook, Servidor and Roteador | `Notebook`, `Server`, `Router`, each with one attribute of its own set after `super().__init__()` |
| 3 | `exibir_detalhes()` overridden in the subclasses | `display_details()`: each subclass calls `super().display_details()` and adds its own field |
| 4 | Polymorphism over a list of different types | The `for` loop calls `display_details()` on every asset; each type answers in its own way |
| 5 | `isinstance()` to identify the type | Counts how many assets are `Server` |
| 6 | Persist to JSON with a type field | `to_dict()` writes `"type"` with the class name; `save_assets()` writes a JSON array of objects |
| 7 | Rebuild from JSON keeping IDs and links | `asset_from_dict()` reads `"type"` and creates the right subclass; `load_assets()` reloads the file, and the program checks that types, IDs and `linked_ids` were preserved |

## Concepts

- **Abstraction:** `Asset` is abstract. `display_details()` is an `@abstractmethod`, so `Asset(...)` raises `TypeError` and every subclass must implement it. The abstract method still has a body that the subclasses reuse through `super()`.
- **Inheritance and `super()`:** the subclasses reuse the common fields and methods of `Asset`, and only add what is specific to them. The same happens in `to_dict()`: the subclass takes the dictionary from `super().to_dict()` and adds one field.
- **Polymorphism:** the same call, `asset.display_details()` or `asset.to_dict()`, gives a different result for each type.
- **Inheritance versus composition:** a `Server` *is an* `Asset` (inheritance); an asset *has* a list of linked asset IDs (composition by reference).

## Evidence

`assets.json` is the file written by the program: a JSON array with one object per asset, each with its `"type"`.

Output of `python3 ativos.py`:

```
=== All assets ===
[1] File Server | owner: João | links: [] | OS: Linux
[2] Core Router | owner: Maria | links: [1] | model: Cisco ISR 4331
[3] NB-Finance-01 | owner: Ana | links: [1, 2] | brand: Dell

Total servers: 1

Cannot create a generic Asset: Can't instantiate abstract class Asset with abstract method display_details

Saved to assets.json
=== Reloaded from assets.json ===
[1] File Server | owner: João | links: [] | OS: Linux
[2] Core Router | owner: Maria | links: [1] | model: Cisco ISR 4331
[3] NB-Finance-01 | owner: Ana | links: [1, 2] | brand: Dell

Types, IDs and links preserved after reload: True
```

## Applied in the main project

The same ideas are used in [Asset-Inventory](https://github.com/larasoaresm2/Asset-Inventory): the `Equipment` class hierarchy with the polymorphic `exposure_factor()`, and, in the JSON stage, `to_dict()` and `from_dict()` with a `"type"` field.
