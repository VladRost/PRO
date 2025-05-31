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

    - name: semgrep
      image: returntocorp/semgrep
      command: ['cat']
      tty: true
"""
    }
  }

  environment {
    IMAGE_NAME = "bkimminich/juice-shop"
    IMAGE_TAG = "latest"
    NAMESPACE = "juice"
    CHART_PATH = "./juice-shop"
    REPORT_DIR = "semgrep-report"
    REPORT_FILE = "semgrep.json"  // Replace with your chart path if different
  }

  stages {
   stage('Checkout') {
      steps {
        container('helm') {
          checkout scm
        }
      }
    }

   stage('SAST Scan (Semgrep)') {
      steps {
        container('semgrep') {
          sh """
          mkdir -p ${REPORT_DIR}
          semgrep scan --config auto . --json > ${REPORT_DIR}/${REPORT_FILE}
          """
        }
      }
    }

    stage('Archive Semgrep Report') {
      steps {
        container('semgrep') {
          archiveArtifacts artifacts: "${REPORT_DIR}/${REPORT_FILE}", allowEmptyArchive: true
        }
      }
    }

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

