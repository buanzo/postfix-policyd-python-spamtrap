# Spamtrap Policy Daemon for Postfix

## Overview
This system implements a spamtrap policy daemon for Postfix, allowing for the dynamic blocklisting of email senders based on emails sent to designated spamtrap addresses. It supports Redis and SQLite backends for flexibility in deployment.

## Features

- **Redis and SQLite Support**: Configurable to use either a Redis server or a local SQLite database for storing blocklisted senders.
- **Dynamic Blocklisting**: Automatically adds senders to a blocklist when they send mail to spamtrap addresses.
- **Flexible Integration**: Works with Postfix by integrating into the `smtpd_recipient_restrictions` and `smtpd_sender_restrictions`.

## Setup

1. **Clone the Repository**: Download the scripts to your server.
2. **Install Dependencies**: Ensure Python 3 is installed along with the `redis` and `sqlite3` Python libraries.
3. **Configure**: Edit `config.py` to set your backend type (`redis` or `sqlite`), connection details, and spamtrap addresses.

## Configuration

- **Backend Type**: Choose `redis` for networked solutions or `sqlite` for standalone deployments.
- **Connection Details**: Specify host, port, and DB for Redis; database file path for SQLite.
- **Spamtrap Addresses**: List email addresses used as spamtraps.

## Running

Start the `main_spamtrap_policy.py` and `sender_check_policy.py` scripts according to your Postfix configuration. Integrate the policy checks into Postfix's `main.cf`:

```plaintext
smtpd_sender_restrictions = check_policy_service inet:127.0.0.1:10667, ...
smtpd_recipient_restrictions = ..., check_policy_service inet:127.0.0.1:10666
```

## Maintenance

Update Spamtrap Addresses: Modify config.py as needed.
Convert Backend Data to Postfix Map: Use the conversion script to generate a map file for high-load scenarios, reducing direct backend queries.

## License

Distributed under the GPLv3 License. See LICENSE for more information.

