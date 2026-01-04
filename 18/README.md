<!-- LLM mostly -->
# Key Docker Compose Commands

### Start containers
```bash
docker compose up -d
```

### Run population script
```bash
docker compose exec app python populate_tables.py
```

###
```bash
docker exec -it tea-mysql mysql -u root -pNotSensitive
```

### Stop containers
```bash
docker compose down
```

### Stop and remove everything including data
```bash
docker compose down -v
```

### Rebuild
```bash
docker-compose build --no-cache
```







