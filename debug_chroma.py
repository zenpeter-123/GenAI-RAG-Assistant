from app.services.rag_service import rag_service

# Az összes chunk listázása
collection = rag_service.vectorstore._collection
results = collection.get()

print(f"Összes chunk: {len(results['ids'])}")
print()

# Csoportosítás forrás szerint
sources = {}
for metadata in results['metadatas']:
    source = metadata.get('source', 'unknown')
    sources[source] = sources.get(source, 0) + 1

print("Források szerinti bontás:")
for source, count in sources.items():
    print(f"  {source}: {count} chunk")