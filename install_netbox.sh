#!/bin/bash

## Configuration variables
VERSION="2.1.0"
VERSION_SHA256_SUM="16379ff5d436fea1d4f4b7e85a207edb1efb8812d1898f6b3723b34d2a62a854"

# Where items are downloaded and unpacked
WORK_DIR="/tmp/netbox"

# Where to install netbox
INSTALL_DIR="/opt/netbox"


## Script Start
if [[ $(id -u) -ne 0 ]]; then
    echo "This script expects to be run as root!"
    exit 1
fi

# Make our working dir
if [[ ! -d "${WORK_DIR}" ]]; then
    mkdir -p "${WORK_DIR}"
fi

# Make our install dir
if [[ ! -d "${INSTALL_DIR}" ]]; then
    mkdir -p "${INSTALL_DIR}"
fi

# Move into the working dir
pushd "${WORK_DIR}" >> /dev/null 2>&1

# Make sure our required packages are present
apt-get install -y python3 python3-dev python3-pip libxml2-dev \
                   libxslt1-dev libffi-dev graphviz libpq-dev \
                   libssl-dev zlib1g-dev

# Path to where we keep the release archive
UNPACK_NAME="netbox-${VERSION}"
DOWNLOAD_PATH="${WORK_DIR}/${ARCHIVE_NAME}"
INSTALL_PATH="${INSTALL_DIR}/${UNPACK_NAME}"
CURRENT_INSTALL_PATH="${INSTALL_DIR}/current"

# Install only if we need to
if [[ ! -d "${INSTALL_PATH}" ]]; then
    echo "Installing a new version of netbox..."

    ARCHIVE_NAME="${VERSION}.tar.gz"
    UNPACK_PATH="${WORK_DIR}/netbox-${VERSION}"

    # Check for the archive - if it's missing download it
    if [[ ! -e "${DOWNLOAD_PATH}" ]]; then
        curl -sL "https://github.com/digitalocean/netbox/archive/v${VERSION}.tar.gz" -o "${ARCHIVE_NAME}"
    fi

    # Get the SHA256 of the archive and compare it to make sure it matches what's expected
    ARCHIVE_SHA256_SUM="$(sha256sum ${ARCHIVE_NAME} | awk '{print $1}')"

    if [[ "${VERSION_SHA256_SUM}" != "${ARCHIVE_SHA256_SUM}" ]]; then
        echo "Archive SHA256 sum does not match expected!"
        echo "Got ${ARCHIVE_SHA256_SUM} but expected ${VERSION_SHA256_SUM}"
        exit 2
    fi

    # Unpack the archive and move it into place
    tar -xzf "${ARCHIVE_NAME}"
    mv "${UNPACK_PATH}" "${INSTALL_PATH}"

    # Make sure the requirements are met
    pip3 install --system -r "${INSTALL_PATH}/requirements.txt"
fi

# Link the new installation
if [[ -e "${CURRENT_INSTALL_PATH}" ]]; then
    rm -f "${CURRENT_INSTALL_PATH}"
fi

ln -s "${INSTALL_PATH}" "${CURRENT_INSTALL_PATH}"
