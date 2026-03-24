# 🐳 Docker RAG Assistant - Microservicio de IA


El objetivo de este proyecto es desplegar un microservicio utilizando Inteligencia Artificial Generativa y técnicas **RAG (Retrieval-Augmented Generation)**, todo ello contenerizado con Docker y orquestado con Docker Compose.

## 💡 Sobre el Proyecto

Para aportar valor y originalidad al ejercicio, he decidido crear un **"Asistente Experto en Docker"**. 

El sistema RAG se alimenta de una base de conocimiento privada (`knowledge.txt`) que contiene documentación técnica avanzada sobre contenedores, volúmenes, redes y buenas prácticas. De esta forma, el chatbot no "alucina" con información de internet, sino que responde estrictamente basándose en los apuntes proporcionados.

## 🛠️ Tecnologías Utilizadas


* **Backend:** Python 3.10+ y FastAPI
* **Inteligencia Artificial:** Google Gemini 2.5 Flash API (Google AI Studio)
* **Frontend:** Interfaz web tipo Chatbot (HTML/CSS/JS)
* **Contenedores:** Docker y Docker Compose
* **Orquestación:** Kubernetes (`kind`)
* **Control de Versiones:** Git y GitHub
* **Infraestructura como Código (IaC):** Terraform
* **GitOps & CI/CD:** ArgoCD y GitHub Actions
* **Observabilidad (SRE):** Helm, Prometheus y Grafana

## 🚀 Cómo ejecutar el proyecto en local

Sigue estos pasos para arrancar el microservicio en tu máquina usando Docker:

### 1. Clonar el repositorio
```bash
git clone [https://github.com/frxngv/rag-docker-microservice.git](https://github.com/frxngv/rag-docker-microservice.git)
cd rag-docker-microservice
```

### 2. Configurar la API Key
Por motivos de seguridad, la clave de la API de Gemini no está incluida en el repositorio.
1. Crea un archivo llamado `.env` en la raíz del proyecto.
2. Añade tu clave de Google AI Studio con el siguiente formato:
   ```text
   GEMINI_API_KEY=tu_clave_secreta_aqui
   ```

### 3. Levantar la infraestructura con Docker Compose
Asegúrate de tener Docker ejecutándose en tu equipo y lanza el siguiente comando:
```bash
docker-compose up -d --build
```
*Este comando descargará la imagen base de Python, instalará las dependencias necesarias (`fastapi`, `google-generativeai`, etc.), montará el volumen con la base de conocimiento y expondrá el puerto 8000.*

### 4. Acceder al Chatbot
Una vez que el contenedor esté en ejecución, abre tu navegador web y visita:
👉 **http://localhost:8000**

## 🏗️ Arquitectura y Volúmenes

El archivo `docker-compose.yml` está configurado para manejar:
* **Variables de Entorno:** Inyecta de forma segura el archivo `.env`.
* **Volúmenes (Bind Mounts):** El archivo `knowledge.txt` está montado como un volumen (`./knowledge.txt:/app/knowledge.txt`). Esto permite actualizar la base de conocimiento del chatbot en tiempo real sin necesidad de reconstruir la imagen de Docker.

## 🚀 Bonus: Migración a Kubernetes (Alta Disponibilidad)

Para ampliar el proyecto y garantizar la alta disponibilidad y la gestión segura de credenciales, el proyecto ha sido migrado de Docker Compose a **Kubernetes**.

### Arquitectura K8s implementada:
* **Deployment (`deployment.yaml`):** Configurado con 2 réplicas para garantizar Alta Disponibilidad (HA). Utiliza una imagen auto-construida mediante CI/CD (GitHub Actions) y alojada en GHCR.
* **Service (`service.yaml`):** Actúa como balanceador de carga interno y expone la aplicación mediante un NodePort (30000).
* **ConfigMap (`configmap.yaml`):** Inyecta la base de conocimiento (`knowledge.txt`) de forma distribuida a todos los pods, permitiendo que la aplicación sea *stateless*.
* **Secret (`secret.yaml`):** Protege la API Key de Gemini. (secret-sample.yaml es un ejemplo de como se debería de ver)

### Instrucciones de despliegue en entorno local (usando `kind`)

Este proyecto está preparado para desplegarse fácilmente en un clúster local utilizando [kind](https://kind.sigs.k8s.io/) (Kubernetes IN Docker).

1. **Levantar el clúster local:**
   ```bash
   kind create cluster
   ```
2. **Configurar credenciales:** Por seguridad, el repositorio no incluye el secreto real. Copia la plantilla y añade tu API Key:
   ```bash
   cp k8s/secret-template.yaml k8s/secret.yaml
   # Edita k8s/secret.yaml y pon tu clave real de Google Gemini
   ```
3. **Aplicar los manifiestos:**
   ```bash
   kubectl apply -f k8s/
   ```
   *(Puedes verificar que los pods están listos ejecutando **kubectl get pods**).*
4. **Exponer el servicio (Port-Forwarding):**
   Abre un túnel seguro para acceder al servicio desde tu navegador:
   ```bash
   kubectl port-forward service/rag-bot-service 30000:8000
   ```
5. **Acceder a la aplicación:**
   Abre tu navegador y entra en: 👉 http://localhost:30000


## 🏗️ Evolución a Arquitectura Cloud y GitOps

Para garantizar Alta Disponibilidad (HA), un despliegue 100% automatizado y monitorización en tiempo real, la infraestructura base en Kubernetes ha evolucionado hacia un ecosistema gobernado por herramientas estándar de la industria SRE/DevOps.

### 1️⃣ Infraestructura como Código (Terraform)
En lugar de crear el clúster local a mano, utilizamos Terraform para provisionarlo de forma reproducible.
```powershell
cd infra
terraform init
terraform apply
```

### 2️⃣ El Piloto Automático: GitOps (ArgoCD)
Una vez creado el clúster, instalamos ArgoCD. A partir de este momento, GitHub es la única fuente de la verdad. Cualquier cambio en los manifiestos YAML (k8s/) se sincroniza automáticamente en el clúster (Self-Healing).

```powershell
# Crear namespace e instalar ArgoCD
kubectl create namespace argocd
kubectl apply -n argocd -f [https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml](https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml)

# Aplicar el contrato GitOps (Conecta el clúster con GitHub)
kubectl apply -f infra/bot-gitops.yaml
```

*Obtener contraseña de ArgoCD y abrir panel:*
```powershell
$SEC = kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}"; [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($SEC))

kubectl port-forward svc/argocd-server -n argocd 8080:443
```

👉 **Acceso ArgoCD:** https://localhost:8080 (Usuario: admin)

🔐 Inyección de Secretos (Resolución del CreateContainerConfigError)
Por seguridad y cumplimiento del paradigma GitOps, los secretos reales no se suben a GitHub. Para que los pods arranquen, inyectamos la API Key de Gemini manualmente en el clúster vivo:

```powershell
kubectl create secret generic gemini-api-secret --from-literal=GEMINI_API_KEY="TU_API_KEY_REAL"
```

### 3️⃣ Observabilidad (Prometheus + Grafana)
Para monitorizar el consumo de CPU, RAM y Red de la IA, desplegamos el ecosistema completo de Prometheus usando Helm.

```powershell
helm repo add prometheus-community [https://prometheus-community.github.io/helm-charts](https://prometheus-community.github.io/helm-charts)
helm repo update
helm install monitorizacion prometheus-community/kube-prometheus-stack --namespace monitorizacion --create-namespace
```

*Obtener contraseña de Grafana y abrir panel:*

```powershell
$SEC = kubectl get secret --namespace monitorizacion monitorizacion-grafana -o jsonpath="{.data.admin-password}"; [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($SEC))

kubectl port-forward svc/monitorizacion-grafana -n monitorizacion 8081:80
```

👉 **Acceso Grafana:** http://localhost:8081 (Usuario: admin)

🤖 **Acceso a la IA en Kubernetes**
Para chatear con los pods orquestados por Kubernetes y gobernados por ArgoCD:

```powershell
kubectl port-forward service/rag-bot-service 30000:8000
```

👉 **Acceso Aplicación:** http://localhost:30000