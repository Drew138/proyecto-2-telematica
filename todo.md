
Orquestador
    Controller
    1. Crear nodo: 
    2. Borrar nodo: 
    3. Modificar nodo (?)
    4. ENV loader (Politicas de creacion y destruccion)
    5. [Concurrente] Decider


    Monitor S
    1. Heartbeat: None -> str 
       1. Itera por una lista de conexiones haciendo el heartbeat
       2. Si la instancia no responde es elimnada de la lista con `Desregistro`
    2. GetMetrics: None -> num 
       1.  Itera por la lista de conexiones solicitando datos, los guarda en un archivo
    3. Registro: None -> None
       1. Registra en la lista de conexiones la nueva instancia
    4. Desregistro: None -> None 
       1. Elimina la instancia que llama

Nodo
    Monitor C
    1. Heartbeat: str -> str # Retorna un mensaje para dar cuenta que esta vivo
    2. GetMetrics: None -> num # Retorna la informacion de su metrica
    3. Registro: None -> None # MonitorC llama para conectarse y qudar registrado en el monitor
    4. Desregistro: None -> None # MonitorC llama para desconectarse y ser eliminado del registro en el monitor


# EXTRAS
- DEFINIR API PARA CREAR Y BORRAR INSTANCIAS
- DEVOLVER CODIGOS DE OKAY O ERROR EN GRPC









