pipeline {
  agent {
    kubernetes {
      label 'jenkins-dind'
      defaultContainer 'main'
      yaml """
apiVersion: v1
kind: Pod
spec:
  containers:
    - name: main
      image: lachlanevenson/k8s-helm:latest
      command:
        - cat
      tty: true
      env:
        - name: DOCKER_HOST
          value: tcp://localhost:2375
    - name: dind
      image: docker:dind
      securityContext:
        privileged: true
      args:
        - dockerd
        - --host=tcp://0.0.0.0:2375
        - --host=unix:///var/run/docker.sock
"""
    }
  }

  environment {
    IMAGE_NAME = "s28288/projuiceshop"
    IMAGE_TAG = "custom-v1"
    NAMESPACE = "juice"
    CHART_PATH = "./juice-shop"
  }

  stages {
    stage('Install Docker CLI') {
      steps {
        container('main') {
          sh """
          apk add --no-cache docker-cli
          docker version
          """
        }
      }
    }

    stage('Docker Login') {
      steps {
        container('main') {
          withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
            sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
          }
        }
      }
    }

    stage('Build & Push Docker Image') {
      steps {
        container('main') {
          sh """
          docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
          docker push ${IMAGE_NAME}:${IMAGE_TAG}
          """
        }
      }
    }

    stage('Deploy with Helm') {
      steps {
        container('main') {
          sh """
          helm upgrade --install juice-shop ${CHART_PATH} \\
            --namespace ${NAMESPACE} \\
            --create-namespace \\
            --set image.repository=${IMAGE_NAME} \\
            --set image.tag=${IMAGE_TAG}
          """
        }
      }
    }
  }
}

