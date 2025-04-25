pipeline {
  agent any

  stages {
    stage('Detect changed services') {
      steps {
        script {
          def changedDirs = sh(
            script: '''git diff --name-only HEAD~1 HEAD | awk -F/ '{print $1}' | sort -u''',
            returnStdout: true
          ).trim().split('\n')

          env.CHANGED_SERVICES = changedDirs.findAll {
            it == 'user-service' || it == 'scheduler-service'
          }.join(',')

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
          def BUILD_NUMBER = env.BUILD_NUMBER
          // Git commit SHA 또는 타임스탬프를 태그로 사용할 수도 있음
          def GIT_COMMIT_SHORT = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()

          withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
            for (svc in services) {
              dir(svc) {
                def imageName = "csct3434/${svc}"
                def imageTag = "${GIT_COMMIT_SHORT}-${BUILD_NUMBER}"
                echo "Building and pushing ${imageName}:${imageTag}"

                sh """
                  echo \$DOCKER_PASS | docker login -u \$DOCKER_USER --password-stdin
                  docker build -t ${imageName}:${imageTag} -t ${imageName}:latest .
                  docker push ${imageName}:${imageTag}
                  docker push ${imageName}:latest
                """

                // 이미지 태그 업데이트를 위한 Git 리포지토리 업데이트
                sh """
                  git config --global user.email "jenkins@example.com"
                  git config --global user.name "Jenkins"

                  # Helm 값 파일 업데이트
                  sed -i 's|tag: .*|tag: ${imageTag}|' helm-chart/${svc}/values.yaml

                  git add helm-chart/${svc}/values.yaml
                  git commit -m "Update ${svc} image tag to ${imageTag}"
                  git push origin HEAD:main
                """
              }
            }
          }
        }
      }
    }
  }
}
