import json

from shop.pagination import paginate


def main():
    with open("config.json") as f:
        cfg = json.load(f)
    print(f"shop started on port {cfg['port']}, page size {cfg['page_size']}")
    print(paginate(list(range(100)), 1, cfg["page_size"]))


if __name__ == "__main__":
    main()
