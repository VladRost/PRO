pipeline {
  agent {
    kubernetes {
      label 'jenkins-juice-deployer'
      defaultContainer 'helm'
      yaml """
apiVersion: v1
kind: Pod
metadata:
  labels:
    role: juice-shop-deployer
spec:
  serviceAccountName: jenkins
  containers:
    - name: helm
      image: lachlanevenson/k8s-helm:latest
      command:
        - cat
      tty: true
"""
    }
  }

  environment {
    IMAGE_NAME = "bkimminich/juice-shop"
    IMAGE_TAG = "latest"
    NAMESPACE = "juice"
    CHART_PATH = "./juice-shop"  // Replace with your chart path if different
  }

  stages {
    stage('Deploy Juice Shop') {
      steps {
        container('helm') {
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

