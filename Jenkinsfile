pipeline {
  agent any

  environment {
    DOCKERHUB_CREDENTIALS = credentials('dockerhub') // 등록한 DockerHub 자격증명
  }

  stages {
    stage('Checkout') {
      steps {
        git 'https://github.com/csct3434/k3s.git'
      }
    }

    stage('Build user-service') {
      steps {
        dir('user-service') {
          sh 'docker build -t csct3434/user-service:latest .'
        }
      }
    }

    stage('Push to DockerHub') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
          sh '''
          echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
          docker push csct3434/user-service:latest
          '''
        }
      }
    }
  }
}

