from enum import Enum
from dataclasses import dataclass
from typing import Any, Optional


class Constants:
    networks = ["local", "finney", "test", "devnet"]
    finney_entrypoint       = "wss://devnet-rpc.jungoai.xyz" # TODO: it should be finney
    finney_test_entrypoint  = "wss://devnet-rpc.jungoai.xyz" # TODO: testnet
    devnet_entrypoint       = "wss://devnet-rpc.jungoai.xyz"
    local_entrypoint        = "ws://127.0.0.1:9944"
    network_map = {
        "finney"    : finney_entrypoint,
        "test"      : finney_test_entrypoint,
        "devnet"    : devnet_entrypoint,
        "local"     : local_entrypoint,
    }
    delegates_detail_url = "https://raw.githubusercontent.com/opentensor/bittensor-delegates/main/public/delegates.json"


@dataclass
class DelegatesDetails:
    display: str
    additional: list[tuple[str, str]]
    web: str
    legal: Optional[str] = None
    riot: Optional[str] = None
    email: Optional[str] = None
    pgp_fingerprint: Optional[str] = None
    image: Optional[str] = None
    twitter: Optional[str] = None

    @classmethod
    def from_chain_data(cls, data: dict[str, Any]) -> "DelegatesDetails":
        def decode(key: str, default=""):
            try:
                if isinstance(data.get(key), dict):
                    value = next(data.get(key).values())
                    return bytes(value[0]).decode("utf-8")
                elif isinstance(data.get(key), int):
                    return data.get(key)
                elif isinstance(data.get(key), tuple):
                    return bytes(data.get(key)[0]).decode("utf-8")
                else:
                    return default
            except (UnicodeDecodeError, TypeError):
                return default

        return cls(
            display=decode("display"),
            additional=decode("additional", []),
            web=decode("web"),
            legal=decode("legal"),
            riot=decode("riot"),
            email=decode("email"),
            pgp_fingerprint=decode("pgp_fingerprint", None),
            image=decode("image"),
            twitter=decode("twitter"),
        )


class Defaults:
    netuid = 1

    class config:
        base_path = "~/.jungoai"
        path = "~/.jungoai/config.yml"
        dictionary = {
            "network": None,
            "wallet_path": None,
            "wallet_name": None,
            "wallet_hotkey": None,
            "use_cache": True,
            "metagraph_cols": {
                "UID": True,
                "STAKE": True,
                "RANK": True,
                "TRUST": True,
                "CONSENSUS": True,
                "INCENTIVE": True,
                "DIVIDENDS": True,
                "EMISSION": True,
                "VTRUST": True,
                "VAL": True,
                "UPDATED": True,
                "ACTIVE": True,
                "AXON": True,
                "HOTKEY": True,
                "COLDKEY": True,
            },
        }

    class subtensor:
        network = "finney"
        chain_endpoint = None
        _mock = False

    class pow_register:
        num_processes = None
        update_interval = 50_000
        output_in_place = True
        verbose = False

        class cuda:
            dev_id = 0
            use_cuda = False
            tpb = 256

    class wallet:
        name = "default"
        hotkey = "default"
        path = "~/.jungoai/wallets/"

    class logging:
        debug = False
        trace = False
        record_log = False
        logging_dir = "~/.jungoai/miners"


defaults = Defaults


class WalletOptions(Enum):
    PATH: str = "path"
    NAME: str = "name"
    HOTKEY: str = "hotkey"


class WalletValidationTypes(Enum):
    NONE = None
    WALLET = "wallet"
    WALLET_AND_HOTKEY = "wallet_and_hotkey"


TYPE_REGISTRY = {
    "types": {
        "Balance": "u64",  # Need to override default u128
    },
    "runtime_api": {
        "DelegateInfoRuntimeApi": {
            "methods": {
                "get_delegated": {
                    "params": [
                        {
                            "name": "coldkey",
                            "type": "Vec<u8>",
                        },
                    ],
                    "type": "Vec<u8>",
                },
                "get_delegates": {
                    "params": [],
                    "type": "Vec<u8>",
                },
            }
        },
        "NeuronInfoRuntimeApi": {
            "methods": {
                "get_neuron_lite": {
                    "params": [
                        {
                            "name": "netuid",
                            "type": "u16",
                        },
                        {
                            "name": "uid",
                            "type": "u16",
                        },
                    ],
                    "type": "Vec<u8>",
                },
                "get_neurons_lite": {
                    "params": [
                        {
                            "name": "netuid",
                            "type": "u16",
                        },
                    ],
                    "type": "Vec<u8>",
                },
                "get_neuron": {
                    "params": [
                        {
                            "name": "netuid",
                            "type": "u16",
                        },
                        {
                            "name": "uid",
                            "type": "u16",
                        },
                    ],
                    "type": "Vec<u8>",
                },
                "get_neurons": {
                    "params": [
                        {
                            "name": "netuid",
                            "type": "u16",
                        },
                    ],
                    "type": "Vec<u8>",
                },
            }
        },
        "StakeInfoRuntimeApi": {
            "methods": {
                "get_stake_info_for_coldkey": {
                    "params": [
                        {
                            "name": "coldkey_account_vec",
                            "type": "Vec<u8>",
                        },
                    ],
                    "type": "Vec<u8>",
                },
                "get_stake_info_for_coldkeys": {
                    "params": [
                        {
                            "name": "coldkey_account_vecs",
                            "type": "Vec<Vec<u8>>",
                        },
                    ],
                    "type": "Vec<u8>",
                },
            },
        },
        "ValidatorIPRuntimeApi": {
            "methods": {
                "get_associated_validator_ip_info_for_subnet": {
                    "params": [
                        {
                            "name": "netuid",
                            "type": "u16",
                        },
                    ],
                    "type": "Vec<u8>",
                },
            },
        },
        "SubnetInfoRuntimeApi": {
            "methods": {
                "get_subnet_hyperparams": {
                    "params": [
                        {
                            "name": "netuid",
                            "type": "u16",
                        },
                    ],
                    "type": "Vec<u8>",
                },
                "get_subnet_info": {
                    "params": [
                        {
                            "name": "netuid",
                            "type": "u16",
                        },
                    ],
                    "type": "Vec<u8>",
                },
                "get_subnets_info": {
                    "params": [],
                    "type": "Vec<u8>",
                },
            }
        },
        "SubnetRegistrationRuntimeApi": {
            "methods": {"get_network_registration_cost": {"params": [], "type": "u64"}}
        },
        "ColdkeySwapRuntimeApi": {
            "methods": {
                "get_scheduled_coldkey_swap": {
                    "params": [
                        {
                            "name": "coldkey_account_vec",
                            "type": "Vec<u8>",
                        },
                    ],
                    "type": "Vec<u8>",
                },
                "get_remaining_arbitration_period": {
                    "params": [
                        {
                            "name": "coldkey_account_vec",
                            "type": "Vec<u8>",
                        },
                    ],
                    "type": "Vec<u8>",
                },
                "get_coldkey_swap_destinations": {
                    "params": [
                        {
                            "name": "coldkey_account_vec",
                            "type": "Vec<u8>",
                        },
                    ],
                    "type": "Vec<u8>",
                },
            }
        },
    },
}

NETWORK_EXPLORER_MAP = {
    "opentensor": {
        "local": "https://polkadot.js.org/apps/?rpc=wss%3A%2F%2Fentrypoint-finney.opentensor.ai%3A443#/explorer",
        "endpoint": "https://polkadot.js.org/apps/?rpc=wss%3A%2F%2Fentrypoint-finney.opentensor.ai%3A443#/explorer",
        "finney": "https://polkadot.js.org/apps/?rpc=wss%3A%2F%2Fentrypoint-finney.opentensor.ai%3A443#/explorer",
    },
    "taostats": {
        "local": "https://x.taostats.io",
        "endpoint": "https://x.taostats.io",
        "finney": "https://x.taostats.io",
    },
}


HYPERPARAMS = {
    # btcli name: (subtensor method, sudo bool)
    "rho": ("sudo_set_rho", False),
    "kappa": ("sudo_set_kappa", False),
    "immunity_period": ("sudo_set_immunity_period", False),
    "min_allowed_weights": ("sudo_set_min_allowed_weights", False),
    "max_weights_limit": ("sudo_set_max_weight_limit", False),
    "tempo": ("sudo_set_tempo", True),
    "min_difficulty": ("sudo_set_min_difficulty", False),
    "max_difficulty": ("sudo_set_max_difficulty", False),
    "weights_version": ("sudo_set_weights_version_key", False),
    "weights_rate_limit": ("sudo_set_weights_set_rate_limit", False),
    "adjustment_interval": ("sudo_set_adjustment_interval", True),
    "activity_cutoff": ("sudo_set_activity_cutoff", False),
    "target_regs_per_interval": ("sudo_set_target_registrations_per_interval", True),
    "min_burn": ("sudo_set_min_burn", False),
    "max_burn": ("sudo_set_max_burn", False),
    "bonds_moving_avg": ("sudo_set_bonds_moving_average", False),
    "max_regs_per_block": ("sudo_set_max_registrations_per_block", True),
    "serving_rate_limit": ("sudo_set_serving_rate_limit", False),
    "max_validators": ("sudo_set_max_allowed_validators", True),
    "adjustment_alpha": ("sudo_set_adjustment_alpha", False),
    "difficulty": ("sudo_set_difficulty", False),
    "commit_reveal_weights_interval": (
        "sudo_set_commit_reveal_weights_interval",
        False,
    ),
    "commit_reveal_weights_enabled": ("sudo_set_commit_reveal_weights_enabled", False),
    "alpha_values": ("sudo_set_alpha_values", False),
    "liquid_alpha_enabled": ("sudo_set_liquid_alpha_enabled", False),
    "registration_allowed": ("sudo_set_network_registration_allowed", False),
}

# Help Panels for cli help
HELP_PANELS = {
    "WALLET": {
        "MANAGEMENT": "Wallet Management",
        "TRANSACTIONS": "Wallet Transactions",
        "IDENTITY": "Identity Management",
        "INFORMATION": "Wallet Information",
        "OPERATIONS": "Wallet Operations",
        "SECURITY": "Security & Recovery",
    },
    "ROOT": {
        "NETWORK": "Network Information",
        "WEIGHT_MGMT": "Weights Management",
        "GOVERNANCE": "Governance",
        "REGISTRATION": "Registration",
        "DELEGATION": "Delegation",
    },
    "STAKE": {
        "STAKE_MGMT": "Stake Management",
        "CHILD": "Child Hotkeys",
    },
    "SUDO": {
        "CONFIG": "Subnet Configuration",
    },
    "SUBNETS": {
        "INFO": "Subnet Information",
        "CREATION": "Subnet Creation & Management",
        "REGISTER": "Neuron Registration",
    },
    "WEIGHTS": {"COMMIT_REVEAL": "Commit / Reveal"},
}
