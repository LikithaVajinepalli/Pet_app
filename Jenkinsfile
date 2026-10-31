pipeline {
    agent any

    environment {
        DOCKERHUB_USER  = "likithavajinepalli"      // change here AND in deployment.yaml if you use another Docker Hub account
        IMAGE_NAME      = "pet-rescue-app"
        IMAGE_TAG       = "latest"
        DOCKERHUB_IMAGE = "likithavajinepalli/pet-rescue-app:latest"
    }

    stages {
        stage('Selenium Tests with pytest') {
            steps {
                echo "Running Selenium tests with pytest"
                bat 'pip install -r requirements.txt'
                bat 'start /B python app.py'
                bat 'ping 127.0.0.1 -n 5 > nul'
                bat 'python -m pytest -v test/test_pets.py'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image ${IMAGE_NAME}:${IMAGE_TAG}"
                bat "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }

        stage('Tag Docker Image') {
            steps {
                echo "Tagging ${IMAGE_NAME}:${IMAGE_TAG} as ${DOCKERHUB_IMAGE}"
                bat "docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${DOCKERHUB_IMAGE}"
            }
        }

        stage('Docker Login') {
            steps {
                echo "Logging in to Docker Hub..."
                // Jenkins > Manage Jenkins > Credentials > add "Username with password", ID: dockerhub-creds
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds',
                                                  usernameVariable: 'DOCKER_USER',
                                                  passwordVariable: 'DOCKER_PASS')]) {
                    bat 'echo %DOCKER_PASS%| docker login -u %DOCKER_USER% --password-stdin'
                }
            }
        }

        stage('Push Docker Image to Docker Hub') {
            steps {
                echo "Pushing ${DOCKERHUB_IMAGE} to Docker Hub..."
                bat "docker push ${DOCKERHUB_IMAGE}"
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo "Deploying application to Kubernetes..."
                bat "kubectl apply -f deployment.yaml --validate=false"
                bat "kubectl apply -f service.yaml"
                bat "kubectl rollout restart deployment/petrescue-deployment"
            }
        }
    }

    post {
        always {
            // Stop the test copy of the app (port 5001) so the next build tests fresh code
            bat '''
@echo off
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5001 ^| findstr LISTENING') do taskkill /F /PID %%a
exit /b 0
'''
        }
        success {
            echo "Pipeline completed successfully! Deployed ${DOCKERHUB_IMAGE}"
        }
        failure {
            echo 'Pipeline failed. Please check the logs.'
        }
    }
}
