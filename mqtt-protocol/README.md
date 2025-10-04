# Codelab Introducción al protocolo MQTT

## Levantar Broker

Para levantar el broker mosquitto:
```bash
docker-compose up -d
```

## Detener Broker

Para detener el broker mosquitto:
```bash
docker-compose down
```

## Verificar

Verificar que esta corriendo correctamente:
```bash
docker ps
docker logs -f mosquitto
```

## Ejecutar con Maven

Para ejecutar el publisher y subscriber:
```bash
mvn compile exec:java -Dexec.mainClass="com.juanlopezaranzazu.mqtt.App"
```

## Resultados

### Levantar el broker
![Leventar Broker](/mqtt-protocol/images/levantar-broker.png)

### Verificar el broker
![Verificar Broker](/mqtt-protocol/images/verificar-broker.png)

### Ejecutar Publisher
![Ejecutar Pusblisher](/mqtt-protocol/images/ejecutar-publisher.png)

### Ejecutar Subscriber
![Ejecutar Subscriber](/mqtt-protocol/images/ejecutar-subscriber.png)

### Detener el broker
![Detener Broker](/mqtt-protocol/images/detener-broker.png)
