#!/usr/bin/env bash
set -e

BASE_URL="https://raw.githubusercontent.com/Parcels-code/virtualship/main/docs/user-guide/tutorials"
TARGET_DIR="tutorials"

FILES=(
  Drifter_data_tutorial.ipynb
  Argo_data_tutorial.ipynb
  CTD_transects.ipynb
  ADCP_transects.ipynb
  xbt_plotting.ipynb
  Ship_underwater_ST_plotting.ipynb
)

mkdir -p "$TARGET_DIR"

for f in "${FILES[@]}"; do
  echo "Fetching $f ..."
  curl -fsSL "$BASE_URL/$f" -o "$TARGET_DIR/$f" || echo "WARNING: could not download $f"
done
