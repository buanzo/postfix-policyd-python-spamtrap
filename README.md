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
3. **Configure**: Edit `config.py` to set your backend type (`redis` or `sqlite`), connection details, spamtrap addresses and (optionally) domain whitelisting.

## Configuration

- **Backend Type**: Choose `redis` for networked solutions or `sqlite` for standalone deployments.
- **Connection Details**: Specify host, port, and DB for Redis; database file path for SQLite.
- **Spamtrap Addresses**: List email addresses used as spamtraps.
- **Whitelisting**: You can configure a list of domains to whitelist, and optionally enable wildcard subdomain whitelisting for those. See below for more details

## Domain-based Whitelisting

The Spamtrap Policy Daemon now supports domain-based whitelisting, allowing you to specify entire domains (and optionally their subdomains) that should
be exempt from spamtrap-based blocking.  This feature simplifies managing trusted senders, especially for organizations or domains where multiple
valid senders are present.

- **Whitelist Domains**: Specify trusted domains in config.py under WHITELIST_DOMAINS. Emails sent from these domains will not be added to the blocklist, even if they hit a spamtrap address.
- **Subdomain Support**: By default, the daemon treats each domain literally, not including subdomains. If you wish to include all subdomains of a whitelisted domain, set INCLUDE_SUBDOMAINS to True in config.py. This ensures that emails from any subdomain of the specified domains are also whitelisted.

To configure this feature, update the WHITELIST_DOMAINS and INCLUDE_SUBDOMAINS settings in config.py.  This approach is ideal for
whitelisting trusted partners, organizations, or your own domains to prevent legitimate emails from being inadvertently blocked.

## Running

Start the `main_spamtrap_policy.py` and `sender_check_policy.py` scripts according to your Postfix configuration. Integrate the policy checks into Postfix's `main.cf`:

```plaintext
smtpd_sender_restrictions = check_policy_service inet:127.0.0.1:10667, ...
smtpd_recipient_restrictions = ..., check_policy_service inet:127.0.0.1:10666
```

## Maintenance

- **Update Spamtrap Addresses**: Modify config.py as needed.
- **Convert Backend Data to Postfix Map**: Use the conversion script to generate a map file for high-load scenarios, reducing direct backend queries.

## License

Distributed under the GPLv3 License. See LICENSE for more information.

