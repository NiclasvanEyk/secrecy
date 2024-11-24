"""
Information about first-party drivers.
"""

WELL_KNOWN_DRIVERS = {
    "aws-boto3": "secrecy_aws.drivers:boto3",
    "docker": "secrecy_docker.drivers:docker",
    "encrypted-file": "secrecy_file.drivers:encrypted_file",
    "environment": "secrecy_environment.drivers:environment",
    "google-cloud": "secrecy_google_cloud.drivers:secret_manager_sync",
    "onepassword-sdk": "secrecy_onepassword.drivers:sdk",
}


def is_well_known_driver(name: str) -> bool:
    return name in WELL_KNOWN_DRIVERS
