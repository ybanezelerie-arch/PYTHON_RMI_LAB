# Python RMI Lab using Pyro5

This project translates the basic architecture of a Java RMI product example into a Python distributed application using **Pyro5 (Python Remote Objects)**.

## Project structure

```text
PYTHON_RMI_LAB/
├── product.py   # Product data model and sample data
├── server.py    # Exposes ProductService methods through Pyro5
├── client.py    # Connects to the server and calls remote methods
└── README.md    # Setup and run instructions
```

## Requirements

- Python 3.9 or newer
- pip
- Both terminals must be able to reach the server. For a same-computer demo, use `localhost`.

## 1. Install Pyro5

Open a terminal in the project folder and run:

```bash
python -m pip install Pyro5
```

On some systems, use `python3` instead of `python`.

## 2. Start the server

In **Terminal 1**, from the project folder, run:

```bash
python server.py
```

Keep the terminal open. The server listens on port `9090` and prints its Pyro URI. The client default URI for a same-computer demo is:

```text
PYRO:product.service@localhost:9090
```

## 3. Start the client

Open **Terminal 2**, also in the project folder, and run:

```bash
python client.py
```

Press Enter to use the default URI when the client asks for the server URI. Choose an operation from the menu:

- `1` — List all products
- `2` — Find a product by ID
- `3` — Add a product
- `4` — Update stock
- `0` — Exit

Sample products are loaded in memory when the server starts. Changes made through the client remain available while that server process is running; they are not saved to disk.

## Running on two different computers

1. Start `server.py` on the server computer.
2. Find the server computer's LAN IP address.
3. In the client terminal, enter `PYRO:product.service@SERVER_IP:9090`, replacing `SERVER_IP` with that address.
4. Ensure the server's firewall allows inbound TCP traffic on port `9090` and both computers are on a network that permits the connection.

Do not expose the server port to the public internet for this classroom demonstration. The sample project does not include authentication or transport encryption.

## How the Java RMI parts map to Python

| Java RMI concept/file | Python equivalent |
|---|---|
| `Product.java` | `product.py` data model |
| `ProductImpl.java` | `ProductService` implementation in `server.py` |
| `Server.java` / `ServerImpl.java` | Server setup and daemon registration in `server.py` |
| `Client.java` | `client.py` |
| Java RMI registry/stub lookup | Pyro5 URI and `Pyro5.api.Proxy` |

Pyro5 does not require a Java-style remote interface or separate `.class` files. The server exposes methods on a Python object, and the client invokes them through a Pyro5 proxy.

## Screenshots for submission

Capture real screenshots after running the project:

1. **Server terminal:** show `python server.py` running and the printed URI.
2. **Client terminal:** choose option `1` to show the product catalog, then optionally demonstrate a remote method such as finding a product or updating stock.

Keep both screenshots in the repository, for example under a `screenshots/` folder, before submitting. Do not use sample or fabricated terminal output as proof of execution.

## Troubleshooting

- `ModuleNotFoundError: No module named 'Pyro5'`: run `python -m pip install Pyro5` in the same Python environment used to run the scripts.
- Connection refused: confirm the server is running and that the client URI uses the correct host and port.
- Cross-computer connection fails: check the LAN IP, firewall, and network restrictions.
- If port `9090` is already in use, change the port in `server.py` and update `DEFAULT_URI` in `client.py` to match.
