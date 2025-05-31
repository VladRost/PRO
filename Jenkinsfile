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
  volumes:
    - name: zap-workdir
      emptyDir: {}
  containers:
    - name: helm
      image: lachlanevenson/k8s-helm:latest
      command: ['cat']
      tty: true

    - name: semgrep
      image: returntocorp/semgrep
      command: ['cat']
      tty: true

    - name: trivy
      image: aquasec/trivy:latest
      command: ['cat']
      tty: true

    - name: zap
      image: zaproxy/zap-stable
      command: ['cat']
      tty: true
      volumeMounts:
        - name: zap-workdir
          mountPath: /zap/wrk
    
    - name: reportgen
      image: python:3.10
      command: ['cat']
      tty: true
"""
    }
  }

  environment {
    IMAGE_NAME = "bkimminich/juice-shop"
    IMAGE_TAG = "latest"
    FULL_IMAGE = "bkimminich/juice-shop"
    NAMESPACE = "juice"
    CHART_PATH = "./juice-shop"
    REPORT_DIR = "semgrep-report"
    REPORT_FILE = "semgrep.json"
    TRIVY_DIR = "trivy-report"
    TRIVY_FILE = "trivy.json"
    ZAP_DIR = "zap-report"
    ZAP_REPORT = "zap.html"
    TARGET_URL = "https://4ef2-2a02-a31a-c3b2-5500-ae6c-63f3-5bdc-26e7.ngrok-free.app/#/"
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
    stage('Image Scan (Trivy)') {
      steps {
        container('trivy') {
          sh """
          mkdir -p ${TRIVY_DIR}
          trivy image --severity CRITICAL,HIGH --format json -o ${TRIVY_DIR}/${TRIVY_FILE} ${FULL_IMAGE}
          """
        }
      }
    }

    stage('Archive Trivy Report') {
      steps {
        container('trivy') {
          archiveArtifacts artifacts: "${TRIVY_DIR}/${TRIVY_FILE}", allowEmptyArchive: true
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
    stage('DAST Scan (OWASP ZAP)') {
      steps {
        container('zap') {
          sh """
	  cd /zap/wrk
          mkdir -p ${ZAP_DIR}
          zap-full-scan.py -t ${TARGET_URL} -r ${ZAP_DIR}/${ZAP_REPORT} -m 100 || true
          """
        }
      }
    }
    stage('Collect ZAP Report') {
      steps {
        container('zap') {
         archiveArtifacts artifacts: "zap-report/zap.html", allowEmptyArchive: true
        }
      }
    }

    stage('Generate Combined Report') {
      steps {
        container('reportgen') {
	  sh '''
      pip install --quiet --no-cache-dir -U pip
      python3 generate_summary.py
      mkdir -p final-report
      mv summary.html final-report/
      '''
        }
      }
    }

    stage('Archive Final Report') {
      steps {
        container('reportgen') {
          archiveArtifacts artifacts: "final-report/summary.html", allowEmptyArchive: true
        }
      }
    }
  }
}

