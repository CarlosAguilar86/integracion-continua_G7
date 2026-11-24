pipeline {
    agent any

    stages {
        stage('1. Descargar Código (GitHub)') {
            steps {
                echo 'Descargando código desde GitHub...'
                checkout scm
            }
        }

        stage('2. Construir Imagen Docker') {
            steps {
                echo 'Construyendo imagen de FastAPI en Docker Desktop...'
                sh 'docker compose build'
            }
        }

        stage('3. Levantar Contenedores') {
            steps {
                echo 'Levantando backend_api y postgres_db...'
                sh 'docker compose up -d'
            }
        }

        stage('4. Pruebas de Integración') {
            steps {
                echo 'Verificando comunicación entre API y PostgreSQL...'
                sh '''
                    sleep 6
                    curl -f http://host.docker.internal:8000/health
                    curl -f -X POST http://host.docker.internal:8000/tasks \
                         -H "Content-Type: application/json" \
                         -d '{"title": "Tarea automatizada desde Jenkins"}'
                    curl -f http://host.docker.internal:8000/tasks
                '''
            }
        }
    }

    post {
        always {
            echo 'Estado de contenedores y limpieza del entorno...'
            sh 'docker compose ps'
            sh 'docker compose down'
        }
        success {
            echo 'PIPELINE EXITOSO: Integración continua verificada.'
        }
        failure {
            echo 'PIPELINE FALLIDO: Revisar los logs.'
        }
    }
}
