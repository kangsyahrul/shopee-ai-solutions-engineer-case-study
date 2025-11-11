# Pull the latest Qdrant Docker image
docker pull qdrant/qdrant

# Run Qdrant container with persistent storage
docker run -p 6333:6333 -p 6334:6334 \
    -v "$(pwd)/data/qdrant_storage:/qdrant/storage:z" \
    qdrant/qdrant
