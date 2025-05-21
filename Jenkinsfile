pipeline {
  agent {
    kubernetes {
      label 'jenkins-dind-agent'
      defaultContainer 'tools'
      yaml """
apiVersion: v1
kind: Pod
metadata:
  labels:
    some-label: jenkins-dind
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
    
    - name: tools
      image: alpine/helm:3.14.0
      command:
        - cat
      tty: true
      volumeMounts:
        - mountPath: /var/run/docker.sock
          name: docker-sock
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
  volumes:
    - name: docker-sock
      emptyDir: {}
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
	  docker pull s28288/projuiceshop:custom-v1
          """
        }
      }
    }

    stage('Deploy with Helm') {
      steps {
        container('tools') {
          sh """
          helm version
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

