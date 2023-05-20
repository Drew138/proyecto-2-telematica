# info de la materia: ST0263 - TOPICOS ESPECIALES DE TELEMATICA
#
# Estudiante(s): Andres Salazar Galeano, asalaza5@eafit.edu.co
# Estudiante(s): Julian David Ramirez, jdramirezl@eafit.edu.co
#
# Profesor: Edwin Montoya, emontoya@eafit.edu.co


# Proyecto 2
#
# 1. breve descripción de la actividad

En este proyecto se desarrollo una aplicacion capaz de crear infraestructura a traves de codigo (infraestructure as code). 


## 1.1. Que aspectos cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)

### Requisitos funcionales

- Comunicarse con MonitorC a traves de gRPC.
- Crear sistema de heartbeat para detectar vivacidad
- Obtener metricas como la carga de la maquina.
- Registro y Desregistro del MonitorS.
- Comunicarse con el API SDK de la nube para ejecutar funciones de IaaC.
- Acceder al servicio de gestion de instancias EC2.
- Definir un mecanismo de configuracion de la IP o URL o un servicio de localizacion del MonitorS.
- Crear una imagen AMI personalizada a partir de la instancia inicial.
- Configurar parametros de las nuevas instancias, como hardware, disco duro, VPC, Security Group y Key pair.
- Definir minInstances, maxInstance y politicas de creacion y destruccion de instancias.
- Almacenar la informacion de configuracion en el ControllerASG.
- Utilizar instancias de tipo t2.micro para el hardware.


## 1.2. Que aspectos NO cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)

N/A

# 2. información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.

![Arquitectura Topico Tele](https://github.com/Drew138/proyecto-2-telematica/assets/65835577/b4809d3d-a327-456d-8b76-343dd07eb418)

# 3. Descripción del ambiente de desarrollo y técnico: lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.

## como se compila y ejecuta.

Debido a que el orquestrador esta encargado de iniciar las instancias de aws, el unico entry point de la aplicacion es este.

Para inicar el proceso del orquestrador solo basta con correr el siguiente comando que inicia el contenedor del mismo.

`sudo docker-compose up -f docker-compose.orchestrator.yml up --build`

## detalles del desarrollo.

Tanto el orquestrador como la instancia corren sobre contenedor de docker que a su vez soportan python3.9.
Debido a esto, ambas aplicaciones estan desarrolladas en python y subdividias por modulos encargados del monitoreo, control de instancias de aws, clientes, y servidores grpc, entre otros.

Ambos componentes (orquestrador e instancia) se comunican mediante el marco de referencia gRPC, y estan definidas de manera que si la metrica de carga sobre una instancia excede un umbral, se crean nuevas instancias.

De igual manera, si se reduce la carga (o metrica) sobre una instancia, se elimina dicha instancia.


## detalles técnicos

Para el desarrollo de la aplicacion se utilizo la libreria boto3 para interacturas con aws y crear, o borrar instancias EC2 sobre esta de manera automatica.

## descripción y como se configura los parámetros del proyecto (ej: ip, puertos, conexión a bases de datos, variables de ambiente, parámetros, etc)

Los parametros del proyecto son configurables a traves de un archivo llamado `config.json` el cual esta ubicado en la carpeta orchestrator.

Este archivo cuenta con la siguiente estructura:

```json
{
  "policy_config": {
    "max_instances": 5,
    "min_instances": 2,
    "delete_policy": 10,
    "create_policy": 80
  },
  "auth_config": {
    "aws_access_key_id": "ASIAXYCIHBMER5UNUXG7",
    "aws_secret_access_key": "VZLmt57FfFUmzoFsYLYQGwyZTBGkLWmv+UAM5ye3",
    "aws_session_token": "FwoGZXIvYXdzEF0aDD/OBzgjlPwmwOvk9yLGAehL0Z59pBvVkO5FGEqcQODXoAdxUXm/xVGXSmW41k9e8MI57pfsa6I2fgj9mGA859QUnNM4qioX6Ug2vDaPvF15af4hvE2nOoFb9tHghUoEfCek1dFPJFRObGXB5HgfsTp9Wa8CbLrPg856iTuhqZEt0CUMqM1IWMoFXOxcAL87wcVw83cqMCpjGX9Oj2CdfjgbYCl+/t5p9e5RGBRzJdztjaYA0nz/pdK+E2hXKYkdlK0oYrikmTt6Qk3jWYtsEumrFNQf8yj9sJ2jBjItGi+UnJj+oOOkkzpuGX2RzlQ7RXt9acWUnNBBiKVK85A5ol5TCeotRRbGSvTO",
    "region_name": "us-east-1"
  },
  "instance_config": {
    "ami_id": "ami-0c5f9f30125ee0151",
    "security_group_ids": ["sg-094b94a7efca37fe8"],
    "instance_type": "t2.micro",
    "key_pair_name": "vockey"
  },
  "orchestrator_config": {
    "ip_address": "172.31.88.166"
  }
}
```

en este se configuran destalles de la creacion de instancias (segmento `policy_config`), autenticacion (`auth_config`), configuracin de instancias (`instance_config`) y orquestrador (`orchestrator_config`).

## opcional - detalles de la organización del código por carpetas o descripción de algún archivo. (ESTRUCTURA DE DIRECTORIOS Y ARCHIVOS IMPORTANTE DEL PROYECTO, comando 'tree' de linux)
## 
## opcionalmente - si quiere mostrar resultados o pantallazos 

# 4. Descripción del ambiente de EJECUCIÓN (en producción) lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.

Lenguajes de programacion:
- Python

Requisitos:
```requirements.txt
blinker==1.6.2
boto3==1.26.129
botocore==1.29.129
click==8.1.3
Flask==2.3.2
grpcio==1.54.0
grpcio-tools==1.54.0
itsdangerous==2.1.2
Jinja2==3.1.2
jmespath==1.0.1
MarkupSafe==2.1.2
protobuf==4.22.4
python-dateutil==2.8.2
s3transfer==0.6.1
six==1.16.0
termcolor==2.3.0
urllib3==1.26.15
Werkzeug==2.3.4
```

## descripción y como se configura los parámetros del proyecto (ej: ip, puertos, conexión a bases de datos, variables de ambiente, parámetros, etc)

Los puertos del orquestrador y de la instancia son configurables a traves de variables de entorno que a su vez se pueden definir por los archivos de docker-compose que tiene cada uno.

```docker
version: "3.8"

services:
  instance:
    build:
      context: ./instance
    command: python3 ./src/main.py
    environment:
      - API_PORT=80
      - GRPC_PORT=443
    env_file: .env
    ports:
      - 80:80
      - 443:443
```

## una mini guia de como un usuario utilizaría el software o la aplicación

Usuarios de la aplicaciones pueden interactuar tanto con el orquestrador como con la instancias a traves de API REST definidas en ambos.

Las rutas del orquestrador son las siguientes:

`/create` - crea nuevas instancias.

`/kill/<id>` - borra instancias.

Las rutas de instancia son las siguientes:

`/set-metric` - cambia la metrica en la instancia.

`/unregister` - envia una senal para remover la instancia del cluster.

## Video Explicacion

https://youtu.be/4Ubf06xnur4
