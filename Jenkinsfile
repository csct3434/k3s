pipeline {
  agent any
  stages {
    stage('Detect changed services') {
      steps {
        script {
          def changedDirs = sh(
            script: "git diff --name-only HEAD~1 HEAD | awk -F/ '{print $1}' | sort -u",
            returnStdout: true
          ).trim().split('\n')

          env.CHANGED_SERVICES = changedDirs.findAll { it == 'user-service' || it == 'scheduler-service' }.join(',')
          echo "Changed services: ${env.CHANGED_SERVICES}"
        }
      }
    }

    stage('Build & Push Docker Images') {
      when {
        expression { return env.CHANGED_SERVICES }
      }
      steps {
        script {
          def services = env.CHANGED_SERVICES.split(',')
          for (svc in services) {
            dir(svc) {
              def imageName = "csct3434/${svc}"
              echo "Building and pushing ${imageName}"
              sh """
              docker build -t ${imageName}:latest .
              echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
              docker push ${imageName}:latest
              """
            }
          }
        }
      }
    }
  }
  environment {
    DOCKER_USER = credentials('dockerhub').username
    DOCKER_PASS = credentials('dockerhub').password
  }
}
