pipeline {
  agent {
    kubernetes {
      label 'jenkins-dind-agent'
      defaultContainer 'docker'
      yaml """
apiVersion: v1
kind: Pod
metadata:
  labels:
    some-label: dind
spec:
  containers:
    - name: docker
      image: docker:24.0.2-cli
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
      ports:
        - containerPort: 2375
          name: dockerd
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
    stage('Docker Login') {
      steps {
        container('docker') {
          withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
            sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
          }
        }
      }
    }

    stage('Build & Push Image') {
      steps {
        container('docker') {
          sh """
          docker version
          docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
          docker push ${IMAGE_NAME}:${IMAGE_TAG}
          """
        }
      }
    }

    stage('Deploy with Helm') {
      steps {
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

