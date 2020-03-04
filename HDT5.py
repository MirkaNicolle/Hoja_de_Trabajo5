#Hoja de trabajo 5
#Programa de uso de colas y simulacion DES
#Mirka Monzon 18139

import simpy
import random
import math
import statistics

#Caracteristicas a modificar
No_CPU = 1           #CPUS
RAM_Capacidad = 100  #capacidad de RAM
No_Procesos = 25     #numero de procesos
Intervalo = 1        #intervalos de procesos
instructions = 3     #numero de instruciones/t
Tiempo_IO = 1        #tiempo I/O 
Tiempo_Procesos = [] #tiempos
random.seed(15)

#RAM Y CPU
class Components:
    def __init__(self, env):
        self.CPU = simpy.Resource(env, capacity = No_CPU)
        self.RAM = simpy.Container(env, init = RAM_Capacidad, capacity = RAM_Capacidad)

#Clase de proceso
class Process:
    #atributos
    def __init__(self, id, env, components):
        self.id = id
        self.env = env
        self.components = components
        self.instructions = random.randint(1,10)
        self.required_RAM = random.randint(1,10)
        self.terminated = False
        self.initial_Time = 0
        self.end_Time = 0
        self.total_Time = 0
        self.proceso = env.process(self.procesar(env, components))

    #proceso
    def procesar(self, env, components):
        self.initial_Time = env.now
        print("Proceso: %s, creado: %d" % (self.id, self.initial_Time))
        with components.RAM.get(self.required_RAM) as ram:
            yield ram

            #proceso de RAM
            print('Proceso: %s: Ram: %d (Wait)' % (self.id, env.now))
            nxt = 0

            while not self.terminated:
                with components.CPU.request() as request:
                    print ('Proceso: %s: espera de CPU: %d (Wait)' % (self.id, env.now))
                    yield request

                    for i in range (instructions):
                        if self.instructions > 0:
                            self.instructions -= 1
                            nxt = random.randint(1, 2)

                    yield env.timeout(1) #tiempo de espera de CPU

                    #Proceso I/O
                    if nxt ==1:
                        print('Proceso: %s: interaccion I/O %d (I/O)' % (self.id, env.now))
                        yield env.timeout(Tiempo_IO)

                    #Ram done
                    if self.instructions == 0:
                        self.terminated = True

            print('Proceso: %s: finalizado en: %d (estado: terminated)' %(self.id, env.now))
            components.RAM.put(self.required_RAM) #regresa la RAM que se uso

        self.end_Time = env.now
        self.total_Time = int(self.end_Time - self.initial_Time)
        Tiempo_Procesos.insert(self.id, self.total_Time)

#Main
#Crea los procesos
def procesos(env, components):
    for i in range(No_Procesos):
        create_Time = random.expovariate(1.0/Intervalo)
        Process(i, env, components)
        yield env.timeout(create_Time) #tiempo en que tarda crearse cada proceso

env = simpy.Environment() 
components = Components(env)
env.process(procesos(env, components))
env.run()

prom = statistics.mean(Tiempo_Procesos)
desEst = statistics.stdev(Tiempo_Procesos) #promedio y desviacion estandar del tiempo

print("\nTiempo promedio: ", prom, ", Desviacion estandar: ", desEst, "\n\n")

            

        
        
        
