# Key Docker Compose Commands

### Start containers
```bash
docker compose up -d
```

### Run population script
```bash
docker compose exec app python populate.py
```

### Stop containers
```bash
docker compose down
```

### Stop and remove everything including data
```bash
docker compose down -v
```
### Connect to MySQL from host
```bash
mysql -h 127.0.0.1 -P 3306 -u tea_user -p tea_db
```






