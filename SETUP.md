# Setup and Architecture Guide

## System Architecture

```
┌─────────────┐
│   HTTP      │
│ Endpoint    │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────┐
│       Logstash Pipeline         │
├─────────────────────────────────┤
│ Input: HTTP                     │
│ Filter: MySQL Query Processing  │
│ Output: Elasticsearch/Stdout    │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────┐      ┌──────────────┐
│  MySQL DB   │      │ Elasticsearch│
│             │      │              │
└─────────────┘      └──────────────┘
```

## Prerequisites

### System Requirements
- **OS**: Linux, macOS, or Windows
- **RAM**: Minimum 2GB (4GB+ recommended)
- **Storage**: 10GB free disk space
- **Network**: Open ports for HTTP (5044) and MySQL (3306)

### Software Requirements
- Java 8+ (OpenJDK or Oracle JDK)
- Logstash 7.x or higher
- MySQL Server 5.7+
- Python 3.6+ (optional, for client examples)

## Installation Steps

### 1. Install Java

**macOS:**
```bash
brew install java
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install default-jdk
```

**Windows:**
Download from [java.com](https://www.java.com)

### 2. Install Logstash

**macOS:**
```bash
brew install logstash
```

**Linux:**
```bash
wget https://artifacts.elastic.co/downloads/logstash/logstash-8.0.0-linux-x86_64.tar.gz
tar -xzf logstash-8.0.0-linux-x86_64.tar.gz
cd logstash-8.0.0
```

### 3. Install MySQL

**macOS:**
```bash
brew install mysql
```

**Linux:**
```bash
sudo apt-get install mysql-server
```

### 4. Clone Repository

```bash
git clone https://github.com/rohitboghara/logstash-input-http-mysql.git
cd logstash-input-http-mysql
```

## Configuration

### Step 1: Create Logstash Configuration

```conf
input {
  http {
    port => 5044
    codec => json
  }
}

filter {
  # Your filter logic here
}

output {
  elasticsearch {
    hosts => ["localhost:9200"]
    index => "logs-%{+YYYY.MM.dd}"
  }
  stdout { codec => rubydebug }
}
```

### Step 2: Configure MySQL Connection

```conf
filter {
  mysql {
    host => "localhost"
    port => 3306
    username => "root"
    password => "your_password"
    database => "logstash_db"
    query => "SELECT * FROM events"
  }
}
```

### Step 3: Start Services

```bash
# Terminal 1: Start MySQL
mysql.server start

# Terminal 2: Start Logstash
logstash -f logstash.conf
```

## Docker Deployment

See `examples/docker-compose.yml` for a complete Docker setup.

### Quick Docker Start

```bash
cd examples
docker-compose up -d
```

This will start:
- Elasticsearch (port 9200)
- Logstash (port 5044)
- MySQL (port 3306)

## Testing

### 1. Verify Services are Running

```bash
# Check Elasticsearch
curl http://localhost:9200

# Check Logstash
curl -X POST http://localhost:5044 -d '{"test": "data"}'

# Check MySQL
mysql -u root -p -e "SELECT VERSION();"
```

### 2. Send Test Data

```bash
curl -X POST http://localhost:5044 \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Test message",
    "timestamp": "2026-03-27T12:00:00Z"
  }'
```

## Troubleshooting

### Issue: Port Already in Use

```bash
# Find process using port 5044
lsof -i :5044

# Kill the process
kill -9 <PID>
```

### Issue: MySQL Connection Failed

```bash
# Verify MySQL is running
mysql -u root -p -e "SELECT 1;"

# Check credentials in logstash.conf
```

### Issue: Logstash Won't Start

```bash
# Check Java version
java -version

# Check Logstash logs
tail -f logstash-plain.log
```

## Performance Optimization

### Recommended Settings

```conf
settings {
  pipeline.workers => 4
  pipeline.batch.size => 125
  pipeline.batch.delay => 50
}
```

### Tuning Guidelines

- **pipeline.workers**: Set to number of CPU cores
- **batch.size**: Increase for better throughput (higher memory usage)
- **batch.delay**: Lower for lower latency (higher CPU usage)

## Security Considerations

1. **Credentials**: Use environment variables instead of hardcoding passwords
2. **Firewall**: Restrict HTTP port (5044) access
3. **MySQL**: Use strong passwords and limited user privileges
4. **Elasticsearch**: Enable X-Pack security in production

## Next Steps

- Read [README.md](README.md) for feature overview
- Check [examples/](examples/) for configuration samples
- Open an issue for questions or issues
