pipeline {
  agent any

  environment {
    IMAGE_NAME = "s28288/projuiceshop"
    IMAGE_TAG = "custom-v1"
    NAMESPACE = "juice"
    CHART_PATH = "./juice-shop"
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Docker Login') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
          sh "echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin"
        }
      }
    }

    stage('Build Docker Image') {
      steps {
        sh """
        docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
        docker push ${IMAGE_NAME}:${IMAGE_TAG}
        """
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

  post {
    always {
      echo "✅ Pipeline complete: image built, pushed, and deployed!"
    }
  }
}

