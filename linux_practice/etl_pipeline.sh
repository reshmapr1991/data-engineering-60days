#!/bin/bash

echo "================================"
echo "  ETL Pipeline Starting"
echo "  Date: $(date)"
echo "================================"

log() {
    echo "[$(date '+%H:%M:%S')] $1"
}

log "Checking source directory..."

if [ -d "data" ]; then
    log "Data folder found!"
else
    log "Data folder not found - creating it..."
    mkdir data
fi

log "Starting extraction..."
python -c "print('Extracting data...')"
log "Extraction complete"

log "Starting transformation..."
python -c "print('Transforming data...')"
log "Transformation complete"

log "Starting load..."
python -c "print('Loading data...')"
log "Load complete"

echo "================================"
echo "  Pipeline Complete!"
echo "================================"
