pipeline {
    agent any
    environment {
        DOCKER_HUB_USER = 'your-dockerhub-username'
        IMAGE_NAME = 'my-app'
    }
    stages {
        stage('Clone Repository') {
            steps {
                checkout scm
            }
        }
        stage('Build Docker Image') {
            steps {
                sh "docker build -t $DOCKER_HUB_USER/$IMAGE_NAME:$BUILD_NUMBER ."
            }
        }
        stage('Push to Registry') {
            steps {
                echo "Pushing image to Docker Hub..."
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                echo "Updating K8s Deployment..."
            }
        }
    }
}
